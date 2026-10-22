import gzip, json

def saveResponse(respDict):
    with open("respDump.json", "w") as f:
        json.dump(respDict, f, indent=4)



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
    
    else:
        print(f"Incorrect.\n{respDict["previousAdviceText"]}")
        return False

    


def displayResponse():

    print("\n"*20)

    with open("respDump.json", "r") as f:
        respDict = json.load(f)

    print(f"{respDict["questionText"]}")

    print("-"*20)

    for i in range(len(respDict["answers"])):
        print(f"{respDict["answers"][i]["answerText"]}\n^{[i+1]}^\n")



def getNextAnsInput():

    with open("respDump.json", "r") as f:
        respDict = json.load(f)

    nextAnsInput = int(input("Enter answer ID...\n"))-1
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
