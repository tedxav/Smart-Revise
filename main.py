import http.client
import json
from utils import *
import os

# ------------------------------------------------ #

with open("config.json", "r") as f: configJson = json.load(f)

if not os.path.exists("respDump.json"): refreshRespDump()
method, url, headers = configJson["reqParams"]

checkCredentialHeaders()
headers = addCredentialHeaders(headers)

httpsconn = http.client.HTTPSConnection(configJson["domain"])

# ------------------------------------------------ #

while True:

    lastRespDict = fetchRespDump()
    if not checkRespDictValidity(lastRespDict): refreshRespDump()

    displayQuestion(lastRespDict)

    # get the next answer input and close if -2 (-1 input -1) #
    nextAnsInput = getAnswerInput()
    if nextAnsInput == -2: break

    # generate next request body with inputted answer num #
    body = generateNextBody(lastRespDict, nextAnsInput)

    # send answer request and get response #
    httpsconn.request(method, url, json.dumps(body), headers)
    respDict = makeRespDict(httpsconn.getresponse())

    # prompting respDump refresh if unexpected response #
    if "error" in respDict or respDict == {}: 
        refreshRespDump()
    else:
        saveResponse(respDict)
        displayAnswerStatus(respDict)

# try to close http connection after -1 input #
httpsconn.close()
    