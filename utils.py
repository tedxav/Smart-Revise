import gzip, json

def saveResponse(respDict):
    with open("respDump.json", "w") as f:
        json.dump(respDict, f, indent=4)



def addCredentialHeaders(headers):

    with open("tokens.txt", "r+") as f:

        lines = f.readlines()

        if not lines:
            print("No tokens/cookies found!")
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

def displayAnswerStatus():

    with open("respDump.json", "r") as f:
        respDict = json.load(f)

    if respDict["previousCorrectAnswerId"] == respDict["previousAnswerId"]:
        print("Correct!")
        return True

    elif respDict["previousAnswerId"] == -1:
        print(respDict["previousAdviceText"])
    
    else:
        print(f"Incorrect.\n{respDict["previousAdviceText"]}")
        return False

    


def displayQuestion():

    print("\n"*20)

    with open("respDump.json", "r") as f:
        respDict = json.load(f)

    print(f"{respDict["questionText"]}\n")



    for i in range(len(respDict["answers"])):
        print(f"{respDict["answers"][i]["answerText"]}\n^{[i+1]}^\n")



def getNextAnsInput():

    with open("respDump.json", "r") as f:
        respDict = json.load(f)

    nextAnsInput = -12345

    while nextAnsInput not in range(-2,3):
        nextAnsInput = int(input("Enter answer ID... (0 for unknown, -1 for exit)\n"))-1

    nextAnsId = respDict["answers"][nextAnsInput]["id"] if nextAnsInput != 0 else -1

    return nextAnsId



def generateNextBody():

    with open("respDump.json", "r") as f:
        respDict = json.load(f)

    with open("config.json", "r") as f:
        body = json.load(f)["defaultBody"]

    try:
        body["QuestionHash"] = respDict["questionHash"]
        body["PackInstanceEntryId"] = respDict["packInstanceId"]
        body["QuestionOrdinal"] = respDict["questionOrdinal"]

    except: "cry"

    return body
