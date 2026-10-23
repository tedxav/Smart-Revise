import gzip, json, time

def saveResponse(respDict):
    with open("respDump.json", "w") as f:
        json.dump(respDict, f, indent=4)



def addCredentialHeaders(headers):

    try: open("tokens.txt", "r") 
    except: open("tokens.txt", "w")


    with open("tokens.txt", "r+") as f:
        lines = f.readlines()
        if not lines:
            print("No tokens/cookies found!")
            print("""Instructions on how to find cookie and token:
            1. Go to the Smart Revise questions section
            2. Hold CTRL+SHIFT+I or right click and press "Inspect" to open inspect element
            3. In the top bar, click "Network"
            4. Complete a question (Does not matter if the question is correct)
            5. Find the request that looks like: /answer/cb?xxxxxxxxxxxxxxx
            6. Click that request, and click "Headers"
            7. Scroll to "Request Headers"
            7. Copy the headers labelled "RequestVerificationToken" and "Cookie"
            8. Paste the headers here!
            """)
            headers["RequestVerificationToken"] = input("Enter \"RequestVerificationToken\" header:\n")
            headers["Cookie"] = input("Enter \"Cookie\" header:\n")
            f.write(f"{headers["RequestVerificationToken"]}\n{headers["Cookie"]}")
        else:
            headers["RequestVerificationToken"], headers["Cookie"] = lines[0].strip("\n"), lines[1].strip("\n")

    

    return headers


def getRespDict(response):
    respBody = response.read()

    try:
        respBody = gzip.decompress(respBody)
        respDict = json.loads(respBody.decode())

    except Exception as e:

        try:
            respDict = json.loads(respBody)
        except:
            
            respDict = {}

    return respDict

def refreshRespDump():

    print("""Instructions on how to refresh the response dump:
    1. Go to the Smart Revise questions section
    2. Hold CTRL+SHIFT+I or right click and press "Inspect" to open inspect element
    3. In the top bar, click "Network"
    4. Complete a question (Does not matter if the question is correct)
    5. Find the request that looks like: /answer/cb?xxxxxxxxxxxxxxx
    6. Click that request, and click "Response"
    7. Untoggle "Raw" if possible, then copy all of the JSON (ctrl+a should work)
    8. Paste the output here!
    """)

    with open("respDump.json", "w") as f:
        json.dump(json.loads(input("Paste response JSON here:\n")), f)



def displayAnswerStatus(respDict):

    with open("config.json", "r") as f:
        configJson = json.load(f)

    if respDict["previousCorrectAnswerId"] == respDict["previousAnswerId"]:
        print("Correct!")
        time.sleep(configJson["cooldowns"][0])

    elif respDict["previousAnswerId"] == -1:
        print(respDict["previousAdviceText"])
        time.sleep(configJson["cooldowns"][1])
    else:
        print(f"Incorrect.\n{respDict["previousAdviceText"]}")
        time.sleep(configJson["cooldowns"][1])

    


def displayQuestion():

    print("\n"*20)

    with open("respDump.json", "r") as f:
        respDict = json.load(f)

    print(f"{respDict["questionText"]}\n")



    for i in range(len(respDict["answers"])):
        print(f"{respDict["answers"][i]["answerText"]}\n^{[i+1]}^\n")



def getAnswerInput():
    nextAnsInput = -12345

    while nextAnsInput not in range(-2,4):
        nextAnsInput = int(input("Enter answer ID... (0 for unknown, -1 for exit)\n"))-1

    return nextAnsInput



def generateNextBody(answerId):

    with open("respDump.json", "r") as f:
        respDict = json.load(f)

    with open("config.json", "r") as f:
        body = json.load(f)["defaultBody"]


    if answerId >= 0:
        nextAnsId = respDict["answers"][answerId]["id"]

    else: nextAnsId = answerId

    body["proposedAnswerId"] = nextAnsId
    body["QuestionHash"] = respDict.get("questionHash")
    body["PackInstanceEntryId"] = respDict.get("packInstanceId")
    body["QuestionOrdinal"] = respDict.get("questionOrdinal")

    return body
