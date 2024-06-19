import requests
import json
import os
import jsonpath_ng
import time
import logging
from jsonpath_ng import jsonpath, parse


#import requests
start=time.time()

#local path to dump the extract files to be hoovered into the SCCS
pathName="c:\deleteme\\"
#set up logging
fn=pathName+'logging\\QlikAppExtract.log'
os.makedirs(os.path.dirname(fn),exist_ok=True)
LOG_FORMAT="%(levelname)s %(asctime)s-%(message)s"
logging.basicConfig(filename=fn,level=logging.INFO,format=LOG_FORMAT,filemode='w')
logger=logging.getLogger()
logger.info("Starting")
bearerToken = 'Bearer eyJhbGciOiJFUzM4NCIsImtpZCI6IjQ3MDNhMDc4LTBjMTgtNGQ2My04M2ZiLWFlMTgxNjI2ODQ3NyIsInR5cCI6IkpXVCJ9.eyJzdWJUeXBlIjoidXNlciIsInRlbmFudElkIjoiaGlNd1lsZEZFd3dGZzRMYnJ1Y2pVcHVCVU5CbG5BMnIiLCJqdGkiOiI0NzAzYTA3OC0wYzE4LTRkNjMtODNmYi1hZTE4MTYyNjg0NzciLCJhdWQiOiJxbGlrLmFwaSIsImlzcyI6InFsaWsuYXBpL2FwaS1rZXlzIiwic3ViIjoiNGphX3VPUl9UN185elpLSzJwOFRtdUZKdTBkeXZBclIifQ.yfZOlKVbcRbj6VmJIVoonY2aJVkaQ_Kt4KSISvwpRo3NjKHrNInP0rh7umThrhA3giw6A8BmWjv3DzcOvRyBTo2ApHBsQFROegMwmDw4YIl7wxq53OwmTv3QQM2kDuJV'
tenant='https://m3data.eu.qlikcloud.com/'
spacesUrl = tenant+'/api/v1/spaces?limit=100'
head = {'Authorization': 'token {}'.format(bearerToken),
        'Content-Type': 'application/json'
        }
response = requests.get(spacesUrl, headers=head)
data=response.json()
logger.info("gettiing spaces")
#get a list of all the spaces we can access
allSpaces=data['data']

#list spaces we don't want (these are on cloud backup spaces or temp spaces)
spacesToExclude=['RepositoryBackup','RepositoryBackupCurrent','ZZZRepositoryBackup','ZZZRepositoryBackupCurrent','ExtractFromOnPrem']

#keep the non excluded spaces
includeSpaces=[({"space":space['id'],"spacename":space['name']}) for space in allSpaces if space['name'] not in spacesToExclude ]
includeSpaceIds=[space['space'] for space in includeSpaces ]

#get all apps in the system
print('$$$$$ Get a list of all apps in the system, hopefully won\'t be more than 10000 $$$$$\n\n')
appUrl=tenant+'api/v1/apps?limit=10000'
responseAppBlock=requests.get(appUrl,headers=head)
appsData=responseAppBlock.json()

#get all the apps data block, then only pick those that are in an allowed space
json_string=appsData['data']
json_data = json_string
jsonpath_expression = parse('$..attributes')
lstIdsToProcess=list()
appsToProcess=[]
for match in jsonpath_expression.find(json_data):
    matchedValue=match.value
    try:
        thisApp=dict()
        if matchedValue['spaceId'] in includeSpaceIds:
            lstIdsToProcess.append(matchedValue['id'])
            thisApp['spaceId']=matchedValue['spaceId']
            thisApp['id']=matchedValue['id']
            thisApp['name']=matchedValue['name']
            thisApp['_resourcetype']=matchedValue['_resourcetype']
            appsToProcess.append(thisApp)
    except KeyError as e:
        pass
    
errorList=[]
missingSpaces=[]
totalApps=0

logger.info("Iterating apps...")
#go through the app list, and do the extract for each we are allowed to, error if we're not
for app in appsToProcess:
        appAttributes=app
        try:#see if the json has a space id, if not it will error so scoot past it
            spaceId=appAttributes.get('spaceId')
            if spaceId:
                if appAttributes['spaceId'] in includeSpaceIds:
                    print ('\nAppname: '+appAttributes['name'],'\nAppId: '+appAttributes['id'],'\nFile Type: '+appAttributes['_resourcetype'],'\nSpaceId: '+appAttributes['spaceId'])
                    logger.info ('Appname: '+appAttributes['name']+' AppId: '+appAttributes['id']+' File Type: '+appAttributes['_resourcetype']+' SpaceId: '+appAttributes['spaceId'])
                    #get the total number of apps we are processing so we know what we have
                    totalApps+=1
                    
                    #do the extract, lord only knows why we have to Post then Get 
                    appExtracUrl=tenant+'api/v1/apps/'+appAttributes['id']+'/export?NoData=true'
                    print (appExtracUrl)
                    response=requests.post(appExtracUrl, headers=head,json={})
                    if response.ok:
                        location=response.headers._store['location'][1]
                        appDownloadUrl=tenant+location
                        responseDownload=requests.get(appDownloadUrl, headers=head,json={})
                        
                        #if we get this far lets get the space whence it came
                        spaceUrl=tenant+'api/v1/spaces/' + appAttributes['spaceId']
                        responseSpaceBlock = requests.get(spaceUrl, headers=head)
                        spaceData=responseSpaceBlock.json()
                        spaceName=spaceData['name']
                        print('Space:',spaceName)
                        
                        #probably redundant now but double check the space allowance
                        if spaceName not in spacesToExclude:
                            pathName=pathName+spaceName+"\\"
                            try:
                                fn=pathName+appAttributes['name']+".qvf"
                                os.makedirs(os.path.dirname(fn),exist_ok=True)

                                with open(fn,"wb") as outfile:
                                    outfile.write(responseDownload.content)
                            except OSError as e:
                                logger.error ('OSError'+str(e.errno))
                                errorList.append('OSError: '+str(e.errno))
                            except FileNotFoundError as e:
                                print ('FileNotFound')
                                errorList.append('FileNotFound')
                            except:
                                print("error")
                                errorList.append('Unknown Error')
            else:
                print ('no space id available for '+ appAttributes['name'])
                missingSpaces.append(appAttributes['name'])
        except KeyError as e:
            print('KeyError for:'+ appAttributes['name']+str(e))
            errorList.append('KeyError for:'+ appAttributes['name']+str(e))
        except BaseException as e:
            excepName = type(e).__name__           
            print(excepName)
            errorList.append('BaseException '+excepName)
        except:
            print("there has been an error somewhere") 
            errorList.append("there has been an error somewhere")
elapsed=time.time()- start     
print('It took: '+str(elapsed)+ ' seconds.')     
print('The errors were: ',errorList)      
print('Missing space info: ',missingSpaces)    
print('Total Apps: ',totalApps)