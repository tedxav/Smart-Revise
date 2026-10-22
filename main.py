import http.client

import json
import time
from utils import *

with open("config.json", "r") as f:
    configJson = json.load(f)


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
        time.sleep(3)

    else:
        # Let the user read the last answer's hint if incorrectly answered #
        time.sleep(10)
    
    