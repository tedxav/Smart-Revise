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
        print(e)
        print(str(respBody))

        try:
            respDict = json.loads(respBody)
        except:
            
            respDict = {}

    return respDict



def displayAnswerStatus():

    with open("respDump.json", "r") as f:
        respDict = json.load(f)

    if respDict["previousCorrectAnswerId"] == respDict["previousAnswerId"]:
        print("Correct!")
        return True

    elif respDict["previousCorrectAnswerId"] == -1:
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

    nextAnsInput = int(input("Enter answer ID... (0 for unknown, -1 for exit)\n"))-1
    print(nextAnsInput)
    nextAnsId = respDict["answers"][nextAnsInput]["id"]

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
