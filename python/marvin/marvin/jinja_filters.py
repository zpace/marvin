#!/usr/bin/python

'''
This file contains all custom Jinja2 filters.
'''

from manga_utils import generalUtils as gu
import numpy as np

def split(string, delim=None):
    '''Split a string based on a delimiter'''
    
    if not delim: delim=' '
    
    return string.split(delim) if string else None
    
    
def colorCode(value, column):
    ''' Return status code for class to color-code it '''
    
    state = None
    if 'status' in column and value=='fault': state='danger'
    if 'apocomp' in column:
        if value=='In': state='success'
        if value=='Out': state='danger'
    if 'complete' in column:
        state = 'success' if value=='Yes' else 'danger' if value=='No' else ''
    
    return state

def popOver(value,column,location=None,title=False,content=False):
    ''' Return a tooltip for a given column '''
    
    tip = None
    
    # DRP2/3 QUALITY FLAGS
    name = 'MANGA_{0}'.format(column.upper())
    if 'qual' in column:        
        flag = gu.getSDSSFlagName(value,name=name)        
        tip = 'popover'
    if tip and location: tip=location
    if tip and title: tip = 'Flags'
    if tip and content: tip=flag
    
    return tip
    
def setFlag(value,column):
    ''' set quality flags '''
    
    flag = None
    name = 'MANGA_{0}'.format(column.upper())
    if 'qual' in column:
        flag = gu.getSDSSFlagName(value,name=name)
        
    return flag
    
def getMPL(value):
    ''' Define the MPL version '''
    
    name = value
    
    if 'MPL' in value:
        if value == 'MPL-4': name='{0}: v1_5_1, NA'.format(value)
        if value == 'MPL-3': name='{0}: v1_3_3, v1_0_0'.format(value)
        if value == 'MPL-2': name='{0}: v1_2_0, NA'.format(value)
        if value == 'MPL-1': name='{0}: v1_0_0, NA'.format(value)        
    else:
        if value == 'v1_0_0': name='{0} (MPL 1)'.format(value)
        if value == 'v1_1_2': name='{0} (MPL 2)'.format(value)
        if value == 'v1_3_3': name='{0} (MPL 3)'.format(value)
        if value == 'v1_5_1': name='{0} (MPL 4)'.format(value)
        if value == 'v1_5_2': name='{0} (DR13)'.format(value)
   
    return name

def filterForm(value,name,form):
    ''' Filter the form display values based on form parameters '''

    if form:
        try: value = form[name]
        except: return value

    return value
    
def nsatip(value,id):
    ''' Provide a NSA tooltip based on the input parameter '''

    tip=''
    if id in [1]:
        tip = 'e.g. < 1.2 ; > 0.5 ; 0.5-1.2'
    
    return tip
    
def getNSAval(value, id, mag=None, form=None, magids=None):
    ''' Get any NSA values from the form '''
    
    if form:
        nsatext = form['nsatext'] if 'nsatext' in form else []
        if any(nsatext):
            # construct full index array of string ids
            #magid=[2,7,8,13,14] #pre PT column change
            #magid=[2,3,4,9,12,13,14,15,20,21]
            magid = magids
            mags=['f','n','u','g','r','i','z']
            full=[]
            tmp = [full.append(str(i)) if i not in magid else full.extend([''.join(z) for z in zip([str(i)]*7,mags)]) for i in xrange(1,max(magid)+1)]
            # get unique input id
            val = str(id)+mag if mag else str(id)
            # select the nsa text if it exists
            value = nsatext[full.index(val)] if nsatext[full.index(val)] else value
    
    return value
    
def dapissuetype(value,id):
    ''' Define the DAP QA issue type '''
    
    print('dap id',id)
    if id in range(13,20): value = 'dapissues maps'
    if id == 20: value = 'dapissues radgrad'
    if id in range(21,37): value = 'dapissues spectra'
    
    return value
    
def dapclass(value,id):
    ''' add a dap class '''
    if id == 5: value='dapqacomms'
    return value
    
def issuesubcat(value):
    ''' returns a subcategory for a given issue '''
    #temporary fix
    print('value',value)
    if value in range(13,20): return 1
    if value == 20: return 2
    if value in range(21,37): return 3

def dapmaptype(value,key):
    ''' returns map type for a given value, key '''
    return value    
    
def filterByName(value,name,ifu,type):
    ''' filter the inspection dictionary by name, and type '''
        
    if 'drp' in name:
        cols = value.cols
        keys = value.keys
        if type == 'comments':
            comments = value.cubecomments[ifu] if value.cubecomments and ifu in value.cubecomments else None
        elif type == 'search':
            comments = value.searchcomments if value.searchcomments else None
    elif 'dap' in name:
        cols = value.dapqacols
        keys = value.dapqakeys
        if type == 'comments':
            comments = value.dapqacubecomments[ifu] if value.dapqacubecomments and ifu in value.dapqacubecomments else None
        elif type == 'search':
            comments = value.dapqasearchcomments if value.dapqasearchcomments else None

    return cols,keys,comments

def makeID(value,type):
    ''' make a div id for the collapse panels for each name, and type '''
    
    return '{0}_{1}collapse'.format(value,type)

def filterVersion(value):
    ''' filter the version based on criteria '''

    newver = 'v1_5_1' if value=='v1_5_0' else value

    return newver

def prettyError(value):
    ''' make the error captured via sys_exc presentable '''

    # set None defaults
    trace=None; val=None; type=None; msg=None

    # get values
    if len(value.args) == 4: msg, type, val, trace = value.args
    elif len(value.args) == 3:  msg, type, val = value.args
    elif len(value.args) == 2:  msg, type  = value.args
    elif len(value.args) == 1:  msg = value.args[0]

    return msg, type, val, trace
    
def uploadType(value):
    ''' filter the upload type name '''

    if value == 'plateifu': new = 'Plate-IFU'
    if value == 'mangaid': new = 'MaNGA ID'
    if value == 'radec': new = 'RA/Dec'

    return new

    

    
    