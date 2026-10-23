import http.client
import json
from utils import *

with open("config.json", "r") as f:
    configJson = json.load(f)

try:
    with open("respDump.json", "r") as f:
        respDict = json.load(f)

        if "error" in respDict: refreshRespDump()
except: 
    refreshRespDump()

method, url, headers = configJson["reqParams"]
headers = addCredentialHeaders(headers)


conn = http.client.HTTPSConnection(configJson["domain"])
while True:

    displayQuestion()

    nextAnsInput = getAnswerInput()
    if nextAnsInput == -2: break

    body = generateNextBody(nextAnsInput)


    conn.request(method, url, json.dumps(body), headers)

    respDict = getRespDict(conn.getresponse())
    saveResponse(respDict)
    displayAnswerStatus(respDict)

conn.close()
    