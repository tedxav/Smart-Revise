import http.client

import json
import time
from utils import *

with open("config.json", "r") as f:
    configJson = json.load(f)

conn = http.client.HTTPSConnection(configJson["domain"])

body = generateNextBody()


method, url, headers = configJson["reqParams"]
with open("tokens.txt", "r+") as f:

    lines = f.readlines()

    if not lines:
        print("No tokens/cookies found!")
        headers["RequestVerificationToken"] = input("Enter \"RequestVerificationToken\" header:\n")
        headers["Cookie"] = input("Enter \"Cookie\" header:\n")
        f.write(f"{headers["RequestVerificationToken"]}\n{headers["Cookie"]}")

    else:
        headers["RequestVerificationToken"], headers["Cookie"] = lines[0].strip("\n"), lines[1].strip("\n")

print(headers)



for i in range(100):

    displayResponse()
    body = generateNextBody()
    body["proposedAnswerId"] = getNextAnsInput()

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
    
    