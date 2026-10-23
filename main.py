import http.client
import json
from utils import *
import os

with open("config.json", "r") as f:
    configJson = json.load(f)

if not os.path.exists("respDump.json"): refreshRespDump()
refreshCredentialHeaders()

method, url, headers = configJson["reqParams"]
headers = addCredentialHeaders(headers)

conn = http.client.HTTPSConnection(configJson["domain"])
while True:

    try: displayQuestion()
    except: refreshRespDump(); displayQuestion()

    nextAnsInput = getAnswerInput()
    if nextAnsInput == -2: break
    body = generateNextBody(nextAnsInput)

    conn.request(method, url, json.dumps(body), headers)
    respDict = getRespDict(conn.getresponse())

    if "error" in respDict: 
        refreshRespDump()
    else:
        saveResponse(respDict)
        displayAnswerStatus(respDict)

conn.close()
    