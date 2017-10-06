#!/usr/bin/env python
# encoding: utf-8
#
# maps.py
#
# Created by José Sánchez-Gallego on 20 Jun 2016.


from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import distutils.version
import warnings
import itertools
import copy

import astropy.io.fits
import astropy.wcs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import marvin
import marvin.api.api
import marvin.core.core
import marvin.core.exceptions
import marvin.tools.cube
import marvin.tools.map
import marvin.tools.spaxel
import marvin.utils.general.general
import marvin.utils.dap.bpt
import six

from marvin.utils.dap import datamodel
from marvin.utils.dap.datamodel.base import Property, Channel

try:
    import sqlalchemy
except ImportError:
    sqlalchemy = None


__all__ = ('Maps')


def _is_MPL4(dapver):
    """Returns True if the dapver version is <= MPL-4."""

    assert isinstance(dapver, six.string_types), 'dapver must be a string'

    if 'v' in dapver:
        dapver = dapver.strip('v').replace('_', '.')

    dap_version = distutils.version.StrictVersion(dapver)
    MPL4_version = distutils.version.StrictVersion('1.1.1')

    return dap_version <= MPL4_version


class Maps(marvin.core.core.MarvinToolsClass):
    """Returns an object representing a DAP Maps file.

    Parameters:
        data (``HDUList``, SQLAlchemy object, or None):
            An astropy ``HDUList`` or a SQLAlchemy object of a maps, to
            be used for initialisation. If ``None``, the normal mode will
            be used (see :ref:`mode-decision-tree`).
        filename (str):
            The path of the data cube file containing the spaxel to load.
        mangaid (str):
            The mangaid of the spaxel to load.
        plateifu (str):
            The plate-ifu of the spaxel to load (either ``mangaid`` or
            ``plateifu`` can be used, but not both).
        mode ({'local', 'remote', 'auto'}):
            The load mode to use. See :ref:`mode-decision-tree`.
        bintype (str or None):
            The binning type. For MPL-4, one of the following: ``'NONE',
            'RADIAL', 'STON'`` (if ``None`` defaults to ``'NONE'``).
            For MPL-5 and successive, one of, ``'ALL', 'NRE', 'SPX', 'VOR10'``
            (defaults to ``'SPX'``).
        template (str or None):
            The template use for kinematics. For MPL-4, one of
            ``'M11-STELIB-ZSOL', 'MILES-THIN', 'MIUSCAT-THIN'`` (if ``None``,
            defaults to ``'MIUSCAT-THIN'``). For MPL-5 and successive, the only
            option in ``'GAU-MILESHC'`` (``None`` defaults to it).
        nsa_source ({'auto', 'drpall', 'nsa'}):
            Defines how the NSA data for this object should loaded when
            ``Maps.nsa`` is first called. If ``drpall``, the drpall file will
            be used (note that this will only contain a subset of all the NSA
            information); if ``nsa``, the full set of data from the DB will be
            retrieved. If the drpall file or a database are not available, a
            remote API call will be attempted. If ``nsa_source='auto'``, the
            source will depend on how the ``Maps`` object has been
            instantiated. If the cube has ``Maps.data_origin='file'``,
            the drpall file will be used (as it is more likely that the user
            has that file in their system). Otherwise, ``nsa_source='nsa'``
            will be assumed. This behaviour can be modified during runtime by
            modifying the ``Maps.nsa_mode`` with one of the valid values.
        release (str):
            The MPL/DR version of the data to use.

    """

    def __init__(self, *args, **kwargs):

        valid_kwargs = [
            'data', 'filename', 'mangaid', 'plateifu', 'mode', 'release',
            'bintype', 'template_kin', 'template', 'nsa_source']

        assert len(args) == 0, 'Maps does not accept arguments, only keywords.'
        for kw in kwargs:
            assert kw in valid_kwargs, 'keyword {0} is not valid'.format(kw)

        super(Maps, self).__init__(*args, **kwargs)

        self.header = None
        self.wcs = None
        self.shape = None
        self._cube = None

        if self.data_origin == 'file':
            self._load_maps_from_file(data=self.data)
        elif self.data_origin == 'db':
            self._load_maps_from_db(data=self.data)
        elif self.data_origin == 'api':
            self._load_maps_from_api()
        else:
            raise marvin.core.exceptions.MarvinError(
                'data_origin={0} is not valid'.format(self.data_origin))

        self.properties = self._datamodel.properties

        self._check_versions(self)

    def __repr__(self):
        return ('<Marvin Maps (plateifu={0.plateifu!r}, mode={0.mode!r}, '
                'data_origin={0.data_origin!r}, bintype={0.bintype.name!r}, '
                'template={0.template.name!r})>'.format(self))

    def __getitem__(self, value):
        """Gets either a spaxel or a map depending on the type on input."""

        if isinstance(value, tuple):
            assert len(value) == 2, 'slice must have two elements.'
            y, x = value
            return self.getSpaxel(x=x, y=y, xyorig='lower')
        elif isinstance(value, six.string_types):
            return self.getMap(value)
        else:
            raise marvin.core.exceptions.MarvinError('invalid type for getitem.')

    def _set_datamodel(self, **kwargs):
        """Sets the datamodel, template, and bintype."""

        if 'template_kin' in kwargs:
            warnings.warn('template_kin has been deprecated and will be removed '
                          'in a future version. Use template.',
                          marvin.core.exceptions.MarvinDeprecationWarning)
            if 'template' not in kwargs:
                kwargs['template'] = kwargs['template_kin']

        self._datamodel = datamodel[self.release]

        # We set the bintype  and template_kin again, now using the DAP version
        self.bintype = self._datamodel.get_bintype(kwargs.pop('bintype', None))
        self.template = self._datamodel.get_template(kwargs.pop('template', None))

    def __deepcopy__(self, memo):
        return Maps(plateifu=copy.deepcopy(self.plateifu, memo),
                    release=copy.deepcopy(self.release, memo),
                    bintype=copy.deepcopy(self.bintype, memo),
                    template=copy.deepcopy(self.template, memo),
                    nsa_source=copy.deepcopy(self.nsa_source, memo))

    @staticmethod
    def _check_versions(instance):
        """Confirm that drpver and dapver match the ones from the header.

        This is written as a staticmethod because we'll also use if for
        ModelCube.

        """

        header_drpver = instance.header['VERSDRP3']
        isMPL4 = False
        if instance._release == 'MPL-4' and header_drpver == 'v1_5_0':
            header_drpver = 'v1_5_1'
            isMPL4 = True
        assert header_drpver == instance._drpver, ('mismatch between maps._drpver={0} '
                                                   'and header drpver={1}'
                                                   .format(instance._drpver, header_drpver))

        # MPL-4 does not have VERSDAP
        if isMPL4:
            assert 'VERSDAP' not in instance.header, 'mismatch between maps._dapver and header'
        else:
            header_dapver = instance.header['VERSDAP']
            assert header_dapver == instance._dapver, 'mismatch between maps._dapver and header'

    def _getFullPath(self):
        """Returns the full path of the file in the tree."""

        params = self._getPathParams()
        path_type = params.pop('path_type')

        return super(Maps, self)._getFullPath(path_type, **params)

    def download(self):
        """Downloads the maps using sdss_access - Rsync"""

        if not self.plateifu:
            return None

        params = self._getPathParams()
        path_type = params.pop('path_type')

        return super(Maps, self).download(path_type, **params)

    def _getPathParams(self):
        """Returns a dictionary with the paramters of the Maps file.

        The output of this class is mostly intended to be used by
        :func:`Maps._getFullPath` and :func:`Maps.download`.

        """

        plate, ifu = self.plateifu.split('-')

        if _is_MPL4(self._dapver):
            niter = int('{0}{1}'.format(self.template.n, self.bintype.n))
            params = dict(drpver=self._drpver, dapver=self._dapver,
                          plate=plate, ifu=ifu, bintype=self.bintype.name,
                          n=niter, path_type='mangamap')
        else:
            daptype = '{0}-{1}'.format(self.bintype.name, self.template.name)
            params = dict(drpver=self._drpver, dapver=self._dapver,
                          plate=plate, ifu=ifu, mode='MAPS', daptype=daptype,
                          path_type='mangadap5')

        return params

    def _load_maps_from_file(self, data=None):
        """Loads a MAPS file."""

        if data is not None:
            assert isinstance(data, astropy.io.fits.HDUList), 'data is not a HDUList.'
        else:
            self.data = astropy.io.fits.open(self.filename)

        self.header = self.data[0].header

        self.mangaid = self.header['MANGAID'].strip()
        self.plateifu = self.header['PLATEIFU'].strip()

        # We use EMLINE_GFLUX because is present in MPL-4 and 5 and is not expected to go away.
        header = self.data['EMLINE_GFLUX'].header
        naxis = header['NAXIS']
        wcs_pre = astropy.wcs.WCS(header)

        # Takes only the first two axis.
        self.wcs = wcs_pre.sub(2) if naxis > 2 else naxis
        self.shape = self.data['EMLINE_GFLUX'].data.shape[-2:]

        # Checks and populates release.
        file_drpver = self.header['VERSDRP3']
        file_drpver = 'v1_5_1' if file_drpver == 'v1_5_0' else file_drpver

        file_ver = marvin.config.lookUpRelease(file_drpver)
        assert file_ver is not None, 'cannot find file version.'

        if file_ver != self._release:
            warnings.warn('mismatch between file version={0} and object release={1}. '
                          'Setting object release to {0}'.format(file_ver, self._release),
                          marvin.core.exceptions.MarvinUserWarning)
            self._release = file_ver

        self._drpver, self._dapver = marvin.config.lookUpVersions(release=self._release)
        self._datamodel = datamodel[self._dapver]

        # Checks the bintype and template from the header
        if not _is_MPL4(self._dapver):
            header_bintype = self.data[0].header['BINKEY'].strip().upper()
            header_bintype = 'SPX' if header_bintype == 'NONE' else header_bintype
        else:
            header_bintype = self.data[0].header['BINTYPE'].strip().upper()

        header_template_key = 'TPLKEY' if _is_MPL4(self._dapver) else 'SCKEY'
        header_template = self.data[0].header[header_template_key].strip().upper()

        if self.bintype.name != header_bintype:
            self.bintype = self._datamodel.get_bintype(header_bintype)

        if self.template.name != header_template:
            self.template = self._datamodel.get_template(header_template)

    def _load_maps_from_db(self, data=None):
        """Loads the ``mangadap.File`` object for this Maps."""

        mdb = marvin.marvindb

        plate, ifu = self.plateifu.split('-')

        if not mdb.isdbconnected:
            raise marvin.core.exceptions.MarvinError('No db connected')

        if sqlalchemy is None:
            raise marvin.core.exceptions.MarvinError('sqlalchemy required to access the local DB.')

        if data is not None:
            assert isinstance(data, mdb.dapdb.File), 'data in not a marvindb.dapdb.File object.'
        else:

            datadb = mdb.datadb
            dapdb = mdb.dapdb
            # Initial query for version
            version_query = mdb.session.query(dapdb.File).join(
                datadb.PipelineInfo,
                datadb.PipelineVersion).filter(
                    datadb.PipelineVersion.version == self._dapver).from_self()

            # Query for maps parameters
            db_maps_file = version_query.join(
                datadb.Cube,
                datadb.IFUDesign).filter(
                    datadb.Cube.plate == plate,
                    datadb.IFUDesign.name == str(ifu)).from_self().join(
                        dapdb.FileType).filter(dapdb.FileType.value == 'MAPS').join(
                            dapdb.Structure, dapdb.BinType).join(
                                dapdb.Template,
                                dapdb.Structure.template_kin_pk == dapdb.Template.pk).filter(
                                    dapdb.BinType.name == self.bintype.name,
                                    dapdb.Template.name == self.template.name).all()

            if len(db_maps_file) > 1:
                raise marvin.core.exceptions.MarvinError(
                    'more than one Maps file found for this combination of parameters.')
            elif len(db_maps_file) == 0:
                raise marvin.core.exceptions.MarvinError(
                    'no Maps file found for this combination of parameters.')

            self.data = db_maps_file[0]

        self.header = self.data.primary_header

        # Gets the cube header
        cubehdr = self.data.cube.header

        # Gets the mangaid
        self.mangaid = cubehdr['MANGAID'].strip()

        # Gets the shape from the associated cube.
        self.shape = self.data.cube.shape.shape

        # Creates the WCS from the cube's WCS header
        self.wcs = astropy.wcs.WCS(self.data.cube.wcs.makeHeader())

    def _load_maps_from_api(self):
        """Loads a Maps object from remote."""

        url = marvin.config.urlmap['api']['getMaps']['url']

        url_full = url.format(name=self.plateifu,
                              bintype=self.bintype.name,
                              template=self.template.name)

        try:
            response = self._toolInteraction(url_full)
        except Exception as ee:
            raise marvin.core.exceptions.MarvinError(
                'found a problem when checking if remote maps exists: {0}'.format(str(ee)))

        data = response.getData()

        if self.plateifu not in data['plateifu']:
            raise marvin.core.exceptions.MarvinError('remote maps has a different plateifu!')

        self.header = astropy.io.fits.Header.fromstring(data['header'])

        # Sets the mangaid
        self.mangaid = data['mangaid']

        # Gets the shape from the associated cube.
        self.shape = data['shape']

        # Sets the WCS
        self.wcs = astropy.wcs.WCS(astropy.io.fits.Header.fromstring(data['wcs']))

        return

    @property
    def cube(self):
        """Returns the :class:`~marvin.tools.cube.Cube` for with this Maps."""

        if not self._cube:
            try:
                cube = marvin.tools.cube.Cube(plateifu=self.plateifu,
                                              release=self._release)
            except Exception as err:
                raise marvin.core.exceptions.MarvinError(
                    'cannot instantiate a cube for this Maps. Error: {0}'.format(err))
            self._cube = cube

        return self._cube

    @property
    def manga_target1(self):
        """Return MANGA_TARGET1 flag."""

        manga_target1 = self._datamodel.bitmasks['MANGA_TARGET1']

        try:
            manga_target1.mask = int(self.header['MNGTRG1'])
        except KeyError:
            manga_target1.mask = int(self.header['MNGTARG1'])

        return manga_target1

    @property
    def manga_target2(self):
        """Return MANGA_TARGET2 flag."""

        manga_target2 = self._datamodel.bitmasks['MANGA_TARGET2']

        try:
            manga_target2.mask = int(self.header['MNGTRG2'])
        except KeyError:
            manga_target2.mask = int(self.header['MNGTARG2'])

        return manga_target2

    @property
    def manga_target3(self):
        """Return MANGA_TARGET3 flag."""

        manga_target3 = self._datamodel.bitmasks['MANGA_TARGET3']

        try:
            manga_target3.mask = int(self.header['MNGTRG3'])
        except KeyError:
            manga_target3.mask = int(self.header['MNGTARG3'])

        return manga_target3

    @property
    def target_flags(self):
        """Bundle MaNGA targeting flags."""
        return [self.manga_target1, self.manga_target2, self.manga_target3]

    @property
    def quality_flag(self):
        """Return Maps DAPQUAL flag."""

        try:
            dapqual = self._datamodel.bitmasks['MANGA_DAPQUAL']
        except KeyError:
            dapqual = None
        else:
            dapqual.mask = int(self.header['DAPQUAL'])

        return dapqual
    
    def getSpaxel(self, x=None, y=None, ra=None, dec=None,
                  spectrum=True, modelcube=False, **kwargs):
        """Returns the |spaxel| matching certain coordinates.

        The coordinates of the spaxel to return can be input as ``x, y`` pixels
        relative to``xyorig`` in the cube, or as ``ra, dec`` celestial
        coordinates.

        If ``spectrum=True``, the returned |spaxel| will be instantiated with the
        DRP spectrum of the spaxel for the DRP cube associated with this Maps.

        Parameters:
            x,y (int or array):
                The spaxel coordinates relative to ``xyorig``. If ``x`` is an
                array of coordinates, the size of ``x`` must much that of
                ``y``.
            ra,dec (float or array):
                The coordinates of the spaxel to return. The closest spaxel to
                those coordinates will be returned. If ``ra`` is an array of
                coordinates, the size of ``ra`` must much that of ``dec``.
            xyorig ({'center', 'lower'}):
                The reference point from which ``x`` and ``y`` are measured.
                Valid values are ``'center'`` (default), for the centre of the
                spatial dimensions of the cube, or ``'lower'`` for the
                lower-left corner. This keyword is ignored if ``ra`` and
                ``dec`` are defined.
            spectrum (bool):
                If ``True``, the |spaxel| will be initialised with the
                corresponding DRP spectrum.
            modelcube (bool):
                If ``True``, the |spaxel| will be initialised with the
                corresponding ModelCube data.


        Returns:
            spaxels (list):
                The |spaxel| objects for this cube/maps corresponding to the
                input coordinates. The length of the list is equal to the
                number of input coordinates.

        .. |spaxel| replace:: :class:`~marvin.tools.spaxel.Spaxel`

        """

        kwargs['cube'] = self.cube if spectrum else False
        kwargs['maps'] = self.get_unbinned()
        kwargs['modelcube'] = modelcube if not _is_MPL4(self._dapver) else False

        return marvin.utils.general.general.getSpaxel(x=x, y=y, ra=ra, dec=dec, **kwargs)

    def _match_properties(self, property_name, channel=None, exact=False):
        """Returns the best match for a property_name+channel."""

        channel = channel.name if isinstance(channel, Channel) else channel

        if channel is not None:
            property_name = property_name + '_' + channel

        best = self._datamodel[property_name]
        assert isinstance(best, Property), 'the retrived value is not a property.'

        if exact:
            assert best.full() == property_name, \
                'retrieved property {0!r} does not match input {1!r}'.format(best.full(),
                                                                             property_name)

        return best

    def getMap(self, property_name, channel=None, exact=False):
        """Retrieves a :class:`~marvin.tools.map.Map` object.

        Parameters:
            property_name (str):
                The property of the map to be extractred. It may the name
                of the channel (e.g. ``'emline_gflux_ha_6564'``) or just the
                name of the property (``'emline_gflux'``).
            channel (str or None):
                If defined, the name of the channel to be appended to
                ``property_name`` (e.g., ``'ha_6564'``).
            exact (bool):
                If ``exact=False``, fuzzy matching will be used, retrieving
                the best match for the property name and channel. If ``True``,
                will check that the name of returned map matched the input
                value exactly.

        """

        best = self._match_properties(property_name, channel=channel, exact=exact)

        return marvin.tools.map.Map(self, best)

    def getMapRatio(self, property_name, channel_1, channel_2):
        """Returns a ratio :class:`~marvin.tools.map.Map`.

        For a given ``property_name``, returns a :class:`~marvin.tools.map.Map`
        which is the ratio of ``channel_1/channel_2``.

        Parameters:
            property_name (str):
                The property_name of the map to be extractred.
                E.g., `'emline_gflux'`.
            channel_1,channel_2 (str):
                The channels to use.

        """

        # TODO extend to allow for different property names and make channel optional
        map_1 = self.getMap(property_name, channel=channel_1)
        map_2 = self.getMap(property_name, channel=channel_2)

        map_1.value /= map_2.value

        # TODO: do the error propogation (BHA)
        map_1.ivar = None

        map_1.mask &= map_2.mask

        map_1.channel = '{0}/{1}'.format(channel_1, channel_2)

        if map_1.unit != map_2.unit:
            map_1.unit = '{0}/{1}'.format(map_1.unit, map_2.unit)
        else:
            map_1.unit = ''

        return map_1

    def is_binned(self):
        """Returns True if the Maps is not unbinned."""

        return self.bintype.binned

    def get_unbinned(self):
        """Returns a version of ``self`` corresponding to the unbinned Maps."""

        if self.is_binned is False:
            return self
        else:
            return Maps(plateifu=self.plateifu, release=self._release,
                        bintype=self._datamodel.get_unbinned(),
                        template=self.template, mode=self.mode)

    def get_bin_spaxels(self, binid, load=False, only_list=False):
        """Returns the list of spaxels belonging to a given ``binid``.

        If ``load=True``, the spaxel objects are loaded. Otherwise, they can be
        initiated by doing ``Spaxel.load()``. If ``only_list=True``, the method
        will return just a tuple containing the x and y coordinates of the spaxels.

        """

        if self.data_origin == 'file':
            spaxel_coords = zip(*np.where(self.data['BINID'].data.T == binid))

        elif self.data_origin == 'db':
            mdb = marvin.marvindb

            if _is_MPL4(self._dapver):
                table = mdb.dapdb.SpaxelProp
            else:
                table = mdb.dapdb.SpaxelProp5

            spaxel_coords = mdb.session.query(table.x, table.y).join(mdb.dapdb.File).filter(
                table.binid == binid, mdb.dapdb.File.pk == self.data.pk).order_by(
                    table.x, table.y).all()

        elif self.data_origin == 'api':
            url = marvin.config.urlmap['api']['getbinspaxels']['url']

            url_full = url.format(name=self.plateifu,
                                  bintype=self.bintype,
                                  template=self.template,
                                  binid=binid)

            try:
                response = self._toolInteraction(url_full)
            except Exception as ee:
                raise marvin.core.exceptions.MarvinError(
                    'found a problem requesting the spaxels for binid={0}: {1}'
                    .format(binid, str(ee)))

            response = response.getData()
            spaxel_coords = response['spaxels']

        spaxel_coords = list(spaxel_coords)
        if len(spaxel_coords) == 0:
            return []
        else:
            if only_list:
                return tuple([tuple(cc) for cc in spaxel_coords])

        spaxels = [marvin.tools.spaxel.Spaxel(x=cc[0], y=cc[1], maps=self, load=load)
                   for cc in spaxel_coords]

        return spaxels

    def get_bpt(self, method='kewley06', snr_min=3, return_figure=True,
                show_plot=True, use_oi=True, **kwargs):
        """Returns the BPT diagram for this target.

        This method produces the BPT diagram for this target using emission line maps and
        returns a dictionary of classification masks, that can be used to select spaxels
        that have been classified as belonging to a certain excitation process. It also
        provides plotting functionalities.

        Extensive documentation can be found in :ref:`marvin-bpt`.

        Parameters:
            method ({'kewley06'}):
                The method used to determine the boundaries between different excitation
                mechanisms. Currently, the only available method is ``'kewley06'``, based on
                Kewley et al. (2006). Other methods may be added in the future. For a detailed
                explanation of the implementation of the method check the
                :ref:`BPT documentation <marvin-bpt>`.
            snr_min (float or dict):
                The signal-to-noise cutoff value for the emission lines used to generate the BPT
                diagram. If ``snr_min`` is a single value, that signal-to-noise will be used for
                all the lines. Alternatively, a dictionary of signal-to-noise values, with the
                emission line channels as keys, can be used.
                E.g., ``snr_min={'ha': 5, 'nii': 3, 'oi': 1}``. If some values are not provided,
                they will default to ``SNR>=3``.
            return_figure (bool):
                If ``True``, it also returns the matplotlib figure_ of the BPT diagram plot,
                which can be used to modify the style of the plot.
            show_plot (bool):
                If ``True``, interactively display the BPT plot.
            use_oi (bool):
                If ``True``, turns uses the OI diagnostic line in classifying BPT spaxels

        Returns:
            bpt_return:
                ``get_bpt`` always returns a dictionary of classification masks. These
                classification masks (not to be confused with bitmasks) are boolean arrays with the
                same shape as the Maps or Cube (without the spectral dimension) that can be used
                to select spaxels belonging to a certain excitation process (e.g., star forming).
                The keys of the dictionary, i.e., the classification categories, may change
                depending on the selected `method`. Consult the :ref:`BPT <marvin-bpt>`
                documentation for more details.
                If ``return_figure=True``, ``get_bpt`` will also return the matplotlib figure
                for the generated plot, and a list of axes for each one of the subplots.

        Example:
            >>> cube = Cube(plateifu='8485-1901')
            >>> maps = cube.getMaps()
            >>> bpt_masks, bpt_figure = maps.get_bpt(snr=5, return_figure=True, show_plot=False)

            Now we can use the masks to select star forming spaxels from the cube

            >>> sf_spaxels = cube.flux[bpt_masks['sf']['global']]

            And we can save the figure as a PDF

            >>> bpt_figure.savefig('8485_1901_bpt.pdf')

        .. _figure: http://matplotlib.org/api/figure_api.html

        """

        if 'snr' in kwargs:
            warnings.warn('snr is deprecated. Use snr_min instead. '
                          'snr will be removed in a future version of marvin',
                          marvin.core.exceptions.MarvinDeprecationWarning)
            snr_min = kwargs.pop('snr')

        if len(kwargs.keys()) > 0:
            raise marvin.core.exceptions.MarvinError(
                'unknown keyword {0}'.format(list(kwargs.keys())[0]))

        # Makes sure all the keys in the snr keyword are lowercase
        if isinstance(snr_min, dict):
            snr_min = dict((kk.lower(), vv) for kk, vv in snr_min.items())

        # If we don't want the figure but want to show the plot, we still need to
        # temporarily get it.
        do_return_figure = True if return_figure or show_plot else False

        # Disables ion() if we are not showing the plot.
        plt_was_interactive = plt.isinteractive()
        if not show_plot and plt_was_interactive:
            plt.ioff()

        bpt_return = marvin.utils.dap.bpt.bpt_kewley06(self, snr_min=snr_min,
                                                       return_figure=do_return_figure,
                                                       use_oi=use_oi)

        if show_plot:
            plt.ioff()
            plt.show()

        # Restores original ion() status
        if plt_was_interactive and not plt.isinteractive():
            plt.ion()

        # Returs what we actually asked for.
        if return_figure and do_return_figure:
            return bpt_return
        elif not return_figure and do_return_figure:
            return bpt_return[0]
        else:
            return bpt_return

    def to_dataframe(self, columns=None, mask=None):
        ''' Converts the maps object into a Pandas dataframe

        Parameters:
            columns (list):
                The properties+channels you want to include.  Defaults to all of them.
            mask (array):
                A 2d mask array for filtering your data output

        Returns:
            df (DataFrame):
                a Pandas Dataframe
        '''

        allprops = list(itertools.chain(*[[p.fullname(c) for c in p.channels]
                                          if p.channels else [p.name] for p in self.properties]))

        if columns:
            allprops = [p for p in allprops if p in columns]
        data = np.array([self[p].value[mask].flatten() for p in allprops])

        # add a column for spaxel index
        spaxarr = np.array([np.where(mask.flatten())[0]]) \
            if mask is not None else np.array([np.arange(data.shape[1])])
        data = np.concatenate((spaxarr, data), axis=0)
        allprops = ['spaxelid'] + allprops

        # create the dataframe
        df = pd.DataFrame(data.transpose(), columns=allprops)
        return df
