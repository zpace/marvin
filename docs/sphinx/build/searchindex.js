Search.setIndex({envversion:46,filenames:["index","marvin","marvin.api","marvin.api.api","marvin.api.base","marvin.api.cube","marvin.api.general","marvin.db","marvin.db.database","marvin.tools","marvin.tools.core","marvin.tools.core.colourPrint","marvin.tools.core.core","marvin.tools.core.exceptions","marvin.tools.core.logger","marvin.tools.cube","marvin.tools.query","marvin.tools.query.query","marvin.tools.query.results","marvin.tools.tests","marvin.tools.tests.test_cube","marvin.utils","marvin.utils.db","marvin.utils.db.dbutils","marvin.utils.general","marvin.utils.general.decorators","marvin.utils.general.general","marvin.web","marvin.web.controllers","marvin.web.controllers.index","marvin.web.jinja_filters"],objects:{"":{marvin:[1,0,0,"-"]},"marvin.Config":{"_checkConfig":[1,1,1,""],"_getDrpAllPath":[1,1,1,""],"_setDbConfig":[1,1,1,""],drpall:[1,4,1,""],mode:[1,4,1,""],setDefaultDrpAll:[1,1,1,""],setMPL:[1,1,1,""],setVersions:[1,1,1,""]},"marvin.api":{api:[3,0,0,"-"],base:[4,0,0,"-"],cube:[5,0,0,"-"],general:[6,0,0,"-"]},"marvin.api.api":{Interaction:[3,3,1,""]},"marvin.api.api.Interaction":{"_checkResponse":[3,1,1,""],"_loadConfigParams":[3,1,1,""],"_preloadResults":[3,1,1,""],"_sendRequest":[3,1,1,""],checkMyConfig:[3,1,1,""],getData:[3,1,1,""],getRouteMap:[3,1,1,""]},"marvin.api.base":{BaseView:[4,3,1,""],processRequest:[4,2,1,""]},"marvin.api.base.BaseView":{add_config:[4,1,1,""],after_request:[4,1,1,""],before_request:[4,1,1,""],reset_results:[4,1,1,""],reset_status:[4,1,1,""],update_results:[4,1,1,""]},"marvin.api.cube":{"_getCube":[5,2,1,""],CubeView:[5,3,1,""]},"marvin.api.cube.CubeView":{get:[5,1,1,""],getAllSpectra:[5,1,1,""],getSpectra:[5,1,1,""],index:[5,1,1,""],route_base:[5,4,1,""]},"marvin.api.general":{GeneralRequestsView:[6,3,1,""]},"marvin.api.general.GeneralRequestsView":{buildRouteMap:[6,1,1,""],mangaid2plateifu:[6,1,1,""],route_base:[6,4,1,""]},"marvin.db":{database:[8,0,0,"-"]},"marvin.tools":{core:[10,0,0,"-"],cube:[15,0,0,"-"],query:[16,0,0,"-"],tests:[19,0,0,"-"]},"marvin.tools.core":{colourPrint:[11,0,0,"-"],core:[12,0,0,"-"],exceptions:[13,0,0,"-"],logger:[14,0,0,"-"]},"marvin.tools.core.colourPrint":{"_color_text":[11,2,1,""],"_decode_preferred_encoding":[11,2,1,""],"_write_with_fallback":[11,2,1,""],colourPrint:[11,2,1,""],isatty:[11,2,1,""]},"marvin.tools.core.core":{MarvinToolsClass:[12,3,1,""]},"marvin.tools.core.core.MarvinToolsClass":{"_doLocal":[12,1,1,""],"_doRemote":[12,1,1,""],"_getFullPath":[12,1,1,""]},"marvin.tools.core.exceptions":{MarvinError:[13,5,1,""],MarvinSkippedTestWargning:[13,5,1,""],MarvinUserWarning:[13,5,1,""]},"marvin.tools.core.logger":{MarvinLogger:[14,3,1,""],MyFormatter:[14,3,1,""],important:[14,2,1,""],initLog:[14,2,1,""]},"marvin.tools.core.logger.MarvinLogger":{"_set_defaults":[14,1,1,""],"_showwarning":[14,1,1,""],"_stream_formatter":[14,1,1,""],saveLog:[14,1,1,""]},"marvin.tools.core.logger.MyFormatter":{format:[14,1,1,""],info_fmt:[14,4,1,""],warning_fmp:[14,4,1,""]},"marvin.tools.cube":{Cube:[15,3,1,""]},"marvin.tools.cube.Cube":{"_getCubeFromDB":[15,1,1,""],"_getExtensionData":[15,1,1,""],"_getFullPath":[15,1,1,""],"_openFile":[15,1,1,""],flux:[15,4,1,""],getSpectrum:[15,1,1,""],getWavelength:[15,1,1,""],ivar:[15,4,1,""],mask:[15,4,1,""]},"marvin.tools.query":{query:[17,0,0,"-"],results:[18,0,0,"-"]},"marvin.tools.query.query":{Query:[17,3,1,""]},"marvin.tools.query.query.Query":{add_condition:[17,1,1,""],run:[17,1,1,""],set_params:[17,1,1,""]},"marvin.tools.query.results":{Results:[18,3,1,""]},"marvin.tools.query.results.Results":{download:[18,1,1,""],getNext:[18,1,1,""],sort:[18,1,1,""],toTable:[18,1,1,""]},"marvin.tools.tests":{MarvinTest:[19,3,1,""],skipIfNoDB:[19,2,1,""],test_cube:[20,0,0,"-"]},"marvin.tools.tests.MarvinTest":{skipTest:[19,1,1,""]},"marvin.tools.tests.test_cube":{TestCube:[20,3,1,""]},"marvin.tools.tests.test_cube.TestCube":{"_addToDB":[20,1,1,""],"_getSpectrum_db_fail":[20,1,1,""],"_getSpectrum_db_flux_ra_dec":[20,1,1,""],"_getSpectrum_file_fail":[20,1,1,""],"_getSpectrum_file_flux_ra_dec":[20,1,1,""],"_getSpectrum_remote":[20,1,1,""],"_getSpectrum_remote_fail":[20,1,1,""],"_load_from_db_fail":[20,1,1,""],"_test_getSpectrum":[20,1,1,""],"_test_getSpectrum_raise_exception":[20,1,1,""],setUp:[20,1,1,""],setUpClass:[20,6,1,""],tearDown:[20,1,1,""],tearDownClass:[20,6,1,""],test_cube_load_from_local_database_multipleresultsfound:[20,1,1,""],test_cube_load_from_local_database_nodbconnected:[20,1,1,""],test_cube_load_from_local_database_nodrpver:[20,1,1,""],test_cube_load_from_local_database_noresultsfound:[20,1,1,""],test_cube_load_from_local_database_otherexception:[20,1,1,""],test_cube_load_from_local_database_success:[20,1,1,""],test_cube_load_from_local_file_by_filename_fail:[20,1,1,""],test_cube_load_from_local_file_by_filename_success:[20,1,1,""],test_cube_loadfail:[20,1,1,""],test_getSpectrum_db_flux_ra_dec_full:[20,1,1,""],test_getSpectrum_db_flux_ra_dec_int:[20,1,1,""],test_getSpectrum_db_flux_ra_dec_partial:[20,1,1,""],test_getSpectrum_db_flux_ra_dec_twosigfig:[20,1,1,""],test_getSpectrum_db_flux_x_y:[20,1,1,""],test_getSpectrum_file_flux_ra_dec_full:[20,1,1,""],test_getSpectrum_file_flux_ra_dec_int:[20,1,1,""],test_getSpectrum_file_flux_ra_dec_parital:[20,1,1,""],test_getSpectrum_file_flux_ra_dec_twosigfig:[20,1,1,""],test_getSpectrum_file_flux_x_y:[20,1,1,""],test_getSpectrum_inputs:[20,1,1,""],test_getSpectrum_outside_cube:[20,1,1,""],test_getSpectrum_remote_fail_badpixcoords:[20,1,1,""],test_getSpectrum_remote_fail_badresponse:[20,1,1,""],test_getSpectrum_remote_fail_nourlmap:[20,1,1,""],test_getSpectrum_remote_ra_dec_success:[20,1,1,""],test_getSpectrum_remote_x_y_success:[20,1,1,""]},"marvin.utils":{db:[22,0,0,"-"],general:[24,0,0,"-"]},"marvin.utils.db":{dbutils:[23,0,0,"-"]},"marvin.utils.db.dbutils":{get_traceback:[23,2,1,""],testDbConnection:[23,2,1,""]},"marvin.utils.general":{decorators:[25,0,0,"-"],general:[26,0,0,"-"]},"marvin.utils.general.decorators":{parseRoutePath:[25,2,1,""]},"marvin.utils.general.general":{convertCoords:[26,2,1,""],lookUpMpl:[26,2,1,""],lookUpVersions:[26,2,1,""],mangaid2plateifu:[26,2,1,""],parseName:[26,2,1,""]},"marvin.web":{controllers:[28,0,0,"-"],create_app:[27,2,1,""],jinja_filters:[30,0,0,"-"]},"marvin.web.controllers":{index:[29,0,0,"-"]},"marvin.web.controllers.index":{Marvin:[29,3,1,""]},"marvin.web.controllers.index.Marvin":{base_args:[29,4,1,""],database:[29,1,1,""],get:[29,1,1,""],index:[29,1,1,""],quote:[29,1,1,""],route_base:[29,4,1,""],test:[29,1,1,""]},marvin:{Config:[1,3,1,""],api:[2,0,0,"-"],db:[7,0,0,"-"],tools:[9,0,0,"-"],utils:[21,0,0,"-"],web:[27,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","method","Python method"],"2":["py","function","Python function"],"3":["py","class","Python class"],"4":["py","attribute","Python attribute"],"5":["py","exception","Python exception"],"6":["py","classmethod","Python class method"]},objtypes:{"0":"py:module","1":"py:method","2":"py:function","3":"py:class","4":"py:attribute","5":"py:exception","6":"py:classmethod"},terms:{"_addtodb":20,"_checkconfig":1,"_checkrespons":3,"_checksasurl":[],"_color_text":11,"_decode_preferred_encod":11,"_doloc":12,"_doremot":12,"_getcub":5,"_getcubefromdb":15,"_getdrpallpath":1,"_getextensiondata":15,"_getfullpath":[12,15],"_getspectrum_db_fail":20,"_getspectrum_db_flux_ra_dec":20,"_getspectrum_file_fail":20,"_getspectrum_file_flux_ra_dec":20,"_getspectrum_remot":20,"_getspectrum_remote_fail":20,"_load_from_db_fail":20,"_loadconfigparam":3,"_login":[],"_openfil":15,"_preloadresult":3,"_sendrequest":3,"_set_default":14,"_setdbconfig":1,"_showwarn":14,"_stream_formatt":14,"_test_getspectrum":20,"_test_getspectrum_raise_except":20,"_write_with_fallback":11,"boolean":23,"byte":11,"case":[11,19],"class":[1,3,4,5,6,12,13,14,15,17,18,19,20,29],"default":[1,11,15],"float":15,"function":[4,11,14],"import":14,"int":15,"jos\u00e9":11,"return":[1,4,6,11,12,15,23,26],"s\u00e1nchez":[6,11,12,13],"super":4,"true":11,abil:14,actual:11,add:[4,17],add_condit:17,add_config:4,addit:14,after:[4,11],after_request:4,all:[4,5,6,11],ani:[8,11],ansi:11,api:[],app:6,append:14,appropri:15,arg:[4,5,11,12,14,15,17,18,20],argument:11,arrai:[15,26],asctim:14,assertionerror:20,asstr:23,assum:[11,15],astropi:[11,14],astyp:3,attempt:11,auto:26,avail:26,back:11,base:[],base_arg:29,baseview:[4,5,6],befor:26,before_request:4,black:11,blue:11,blueprint:6,bluesn2:26,bottom:15,bound:11,brian:[4,30],brown:11,bsd:[4,6,11,12,13,30],build:[4,6],buildroutemap:6,built:[11,14],calcul:26,call:[5,6,11,14],can:[6,8,15],cannot:11,captur:14,celesti:15,center:26,centr:15,certain:[1,15,26],check:1,checkmyconfig:3,cherinka:[6,30],clase:4,classi:4,classmethod:20,claus:[4,6,11,12,13,30],closest:15,code:[6,11,15],collect:6,color:[11,14],color_print:11,color_text:11,colored_text:11,colour:11,colourprint:[],colvaldict:20,come:11,condit:17,config:[1,26],configur:[1,3],connect:[8,12,23],content:[],context:14,control:[],conveni:[3,20],convert:26,convertcoord:26,coord:20,coordin:[15,26],copyright:11,core:[],creat:[11,30],create_app:27,cube:[],cubeview:5,custom:19,cyan:11,dap:26,dapver:1,darkgrei:11,data:[1,12,15,17,18],databas:[],dbutil:[],debug:27,dec:[15,20,26],decod:11,decor:[],defin:[3,11,14,26],delet:8,depend:15,describ:5,detail:[],determin:[11,26],dict:4,dictionari:[3,4,6],displai:11,download:18,drp:26,drpall:[1,26],drpver:[1,26],easili:[6,14],effect:11,either:[15,26],empti:11,enabl:14,encod:11,end:11,endpoint:6,errmsg1:20,errmsg2:20,errmsg:20,escap:11,everi:4,exampl:8,except:[],exctyp:20,exist:[3,11],expect:20,ext:15,extens:15,extnam:15,extract:26,fail:11,fall:11,fals:27,feb:[6,12,13],file:[8,11,12,14,15,20,26],filenam:14,fileobj:11,first:11,flask:[4,6],flask_classi:[4,29],flaskview:[4,29],flux:15,fmt:14,font:11,form:4,format:[6,14],formatt:14,from:[4,15,17,20,23],full:[12,15],funcnam:14,galaxi:26,gallego:[6,11,12,13],gener:[],generalrequestsview:6,get:[3,4,5,6,17,20,29],get_traceback:23,getallspectra:5,getdata:3,getmangaid:[],getmangaidlist:[],getnext:18,getpreferredencod:11,getroutemap:3,getspectra:[5,6],getspectrum:[6,15,20],getwavelength:15,give:1,given:[5,8,11,26],global:4,green:11,handl:[4,6,8],have:11,hdr:26,heavili:14,here:11,higher:26,histori:[4,6,12,13,30],idx:20,ifu:26,ignor:26,inappropri:20,includ:11,index:[],info:[4,14],info_fmt:14,initi:[4,6,12,13,14,30],initlog:14,input:[15,20,26],inst:5,interact:3,interest:4,invalid:11,isatti:11,issu:[19,26],ivar:15,jinja_filt:[],join:23,json:4,keep:14,kei:6,keyword:[6,15],kwarg:[4,5,11,12,14,15,17,18,20],last:[4,30],latin:11,left:15,level:14,levelnam:14,licens:[4,6,11,12,13,30],lightblu:11,lightcyan:11,lightgreen:11,lightgrei:11,lightmagenta:11,lightr:11,like:11,list:[14,23],load:[3,12],local:[3,11,12,26],locat:1,log:14,logfilelevel:14,logfilepath:14,logger:[],loglevel:14,lookupmpl:26,lookupvers:26,magenta:11,mai:[11,15],main:14,make:26,manag:14,manga:[5,26],mangaid2plateifu:[6,26],mangaid:[6,26],map:[3,6],marvinerror:13,marvinlogg:14,marvinskippedtestwargn:13,marvintest:[19,20],marvintoolsclass:[12,15,17,18],marvinuserwarn:13,marvinwarn:13,mask:15,member:11,messag:[11,14,20],method:[4,5,6,20],methodnam:[19,20],mode:[1,14,26],modifi:[4,8,30],modul:[],more:[4,26],most:[11,26],mpl:[1,26],mplver:[1,26],msg:11,must:[6,11],myformatt:14,name:[4,5,6,11,14,26],need:8,newresult:4,none:[1,3,4,5,15,23,26],noth:5,nov:11,now:[5,6],numpi:15,object:[1,3,11,12],option:11,origin:[14,15],other:8,output:14,outsid:20,over:14,page:0,pair:11,param:[3,20],paramet:[3,17,23],pars:[25,26],parsenam:26,parseroutepath:25,path:[1,6,12,14,15,25,26],pathparam:12,pathtyp:12,perform:[4,5],pixel:15,placehold:5,plate:26,plateifu:26,posit:11,possibl:12,post:[3,4,6],postgresql:8,prefer:11,primari:13,print:[6,11],process:4,processrequest:4,purpos:6,python:11,queri:[],quot:29,rais:20,real:6,recent:26,record:14,red:11,redsn2:26,rel:[15,26],relat:5,remot:[12,26],replac:6,request:[3,4,5,6,26],request_typ:3,reserv:11,reset:[4,11,14],reset_result:4,reset_statu:4,respect:26,respons:[3,4],rest:3,result:[],retriev:[3,5,15,26],revis:[4,6,12,13,30],right:11,rout:[3,5,6,25],route_bas:[5,6,29],run:[4,17],runtest:[19,20],savelog:14,sdsssync:18,search:0,see:4,self:[6,14],sent:3,sequenc:11,server:15,session:23,set:[1,14,17],set_param:17,setdefaultdrpal:1,setmpl:1,setup:20,setupclass:20,setvers:1,shape:26,side:15,simpli:8,singl:[],skip:[13,19],skipifnodb:19,skiptest:19,sky:26,sn2:26,some:11,sort:18,sourc:[1,3,4,5,6,11,12,13,14,15,17,18,19,20,23,25,26,27,29],spaxel:[15,26],spectra:[5,6],spectrum:15,standard:14,state:[11,14],statu:4,stdout:11,str:[11,15,26],string:[11,23,26],style:11,submodul:[],substitut:6,sum:26,suppli:11,syntax:6,system:14,teardown:20,teardownclass:20,termin:11,test:[],test_cub:[],test_cube_load_from_local_database_multipleresultsfound:20,test_cube_load_from_local_database_nodbconnect:20,test_cube_load_from_local_database_nodrpv:20,test_cube_load_from_local_database_noresultsfound:20,test_cube_load_from_local_database_otherexcept:20,test_cube_load_from_local_database_success:20,test_cube_load_from_local_file_by_filename_fail:20,test_cube_load_from_local_file_by_filename_success:20,test_cube_loadfail:20,test_getspectrum_db_flux_ra_dec_ful:20,test_getspectrum_db_flux_ra_dec_int:20,test_getspectrum_db_flux_ra_dec_parti:20,test_getspectrum_db_flux_ra_dec_twosigfig:20,test_getspectrum_db_flux_x_i:20,test_getspectrum_file_flux_ra_dec_ful:20,test_getspectrum_file_flux_ra_dec_int:20,test_getspectrum_file_flux_ra_dec_parit:20,test_getspectrum_file_flux_ra_dec_twosigfig:20,test_getspectrum_file_flux_x_i:20,test_getspectrum_input:20,test_getspectrum_outside_cub:20,test_getspectrum_remote_fail_badpixcoord:20,test_getspectrum_remote_fail_badrespons:20,test_getspectrum_remote_fail_nourlmap:20,test_getspectrum_remote_ra_dec_success:20,test_getspectrum_remote_x_y_success:20,testcas:19,testcub:20,testdbconnect:23,text:11,than:26,thi:[3,4,5,8,11,14,26],thing:4,those:[11,15],tool:[],totabl:18,traceback:23,track:14,tree:[12,15],tri:[1,26],tty:11,type:[11,15,20],under:[4,6,11,12,13,30],unicodeencodeerror:11,unittest:19,until:11,updat:4,update_result:4,url:[3,5,6],urlmap:6,user:11,userwarn:13,utf:11,util:[],valu:26,variabl:6,version:[1,4,6,12,13,26,30],via:18,view:4,warn:[13,14,19],warning_fmp:14,wavelength:15,web:[],when:[13,19,20],where:11,which:26,white:11,won:11,wrap:11,wrapper:3,wrapperlength:14,write:11,writeabl:11,writer:11,xcube:26,ycube:26,yellow:11},titles:["Welcome to Marvin&#8217;s documentation!","marvin package","marvin.api package","marvin.api.api module","marvin.api.base module","marvin.api.cube module","marvin.api.general module","marvin.db package","marvin.db.database module","marvin.tools package","marvin.tools.core package","marvin.tools.core.colourPrint module","marvin.tools.core.core module","marvin.tools.core.exceptions module","marvin.tools.core.logger module","marvin.tools.cube module","marvin.tools.query package","marvin.tools.query.query module","marvin.tools.query.results module","marvin.tools.tests package","marvin.tools.tests.test_cube module","marvin.utils package","marvin.utils.db package","marvin.utils.db.dbutils module","marvin.utils.general package","marvin.utils.general.decorators module","marvin.utils.general.general module","marvin.web package","marvin.web.controllers package","marvin.web.controllers.index module","marvin.web.jinja_filters module"],titleterms:{api:[2,3,4,5,6],base:4,colourprint:11,content:[1,2,7,9,10,16,19,21,22,24,27,28],control:[28,29],core:[10,11,12,13,14],cube:[5,15],databas:8,dbutil:23,decor:25,document:0,except:13,gener:[6,24,25,26],index:29,indic:0,jinja_filt:30,logger:14,marvin:[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],modul:[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],packag:[1,2,7,9,10,16,19,21,22,24,27,28],queri:[16,17,18],result:18,submodul:[2,7,9,10,16,19,22,24,27,28],subpackag:[1,9,21,27],tabl:0,test:[19,20],test_cub:20,tool:[9,10,11,12,13,14,15,16,17,18,19,20],util:[21,22,23,24,25,26],web:[27,28,29,30],welcom:0}})