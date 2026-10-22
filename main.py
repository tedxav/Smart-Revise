import http.client

import json
import time
from utils import *

with open("config.json", "r") as f:
    configJson = json.load(f)

try: 
    with open("respDump.json", "r") as f:
        respDict = json.load(f)

        try: respDict["error"]; refreshRespDump()
        except: "yeah all good  (i need to learn a better way to do this) "
        
except: 
    refreshRespDump()

method, url, headers = configJson["reqParams"]
headers = addCredentialHeaders(headers)

conn = http.client.HTTPSConnection(configJson["domain"])
while True:

    displayQuestion()
    body = generateNextBody()

    body["proposedAnswerId"] = getNextAnsInput()
    if body["proposedAnswerId"] == -2: break

    conn.request(
        method,
        url,
        json.dumps(body),
        headers
        )

    respDict = getRespDict(conn.getresponse())

    saveResponse(respDict)

    if displayAnswerStatus():
        time.sleep(configJson["cooldowns"][0])

    else:
        # Let the user read the last answer's hint if incorrectly answered #
        time.sleep(configJson["cooldowns"][1])
    
    