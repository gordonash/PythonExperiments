import json
import jsonpath_ng
from jsonpath_ng import jsonpath, parse
json_string ='''
 [{
    "attributes": {
        "id": "000a3021-92d7-4841-9e87-9490a810bfb6",
        "name": "Data Diagnostics-Profilehist-20240514",
        "description": "",
        "thumbnail": "",
        "lastReloadTime": "2022-09-02T14:48:49.574Z",
        "createdDate": "2024-05-14T15:07:46.985Z",
        "modifiedDate": "2024-05-15T15:01:32.192Z",
        "owner": "auth0|1029c97d1b7bafb826a4c4fcd0cadb3020b2b82a69951a712a0d13612112193b",
        "ownerId": "4ja_uOR_T7_9zZKK2p8TmuFJu0dyvArR",
        "dynamicColor": "",
        "published": false,
        "publishTime": "",
        "custom": {},
        "hasSectionAccess": false,
        "encrypted": true,
        "originAppId": "",
        "isDirectQueryMode": false,
        "usage": "ANALYTICS",
        "spaceId": "6628d931342648bd8b3de5af",
        "_resourcetype": "app"
    },
    "privileges": [],
    "create": []
}, {
    "attributes": {
        "id": "000a788f-de29-4b57-9b88-9b43eb506919",
        "name": "20240419-BulletinElementMetaData_vw.qvd",
        "description": "",
        "thumbnail": "",
        "lastReloadTime": "2022-02-22T10:14:30.253Z",
        "createdDate": "2024-04-19T15:58:35.983Z",
        "modifiedDate": "2024-04-22T11:03:50.071Z",
        "owner": "auth0|1029c97d1b7bafb826a4c4fcd0cadb3020b2b82a69951a712a0d13612112193b",
        "ownerId": "4ja_uOR_T7_9zZKK2p8TmuFJu0dyvArR",
        "dynamicColor": "",
        "published": false,
        "publishTime": "",
        "custom": {},
        "hasSectionAccess": false,
        "encrypted": true,
        "originAppId": "",
        "isDirectQueryMode": false,
        "usage": "ANALYTICS",
        "spaceId": "661fc680b5653e5c9f6e68c6",
        "_resourcetype": "app"
    },
    "privileges": [],
    "create": []
}]

'''
json_data = json.loads(json_string)
print (type(json_data))
jsonpath_expression = parse('$..attributes')
lstIdsToProcess=list()
for match in jsonpath_expression.find(json_data):
    print(type(match.value))      
    #print(f'emolyeeid:{match.value}')
    d=match.value
    print(d['id'],d['spaceId'])
    if d['spaceId']=='661fc680b5653e5c9f6e68c6':
        lstIdsToProcess.append(d['id'])
print(lstIdsToProcess)
        

