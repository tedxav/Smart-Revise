import gzip, json, time, os

# ------------------------------------------------ #

def saveResponse(respDict):

    # dumping response json to the respDump file #
    with open("respDump.json", "w") as f:
        json.dump(respDict, f, indent=4)

# ------------------------------------------------ #

def checkCredentialHeaders():
    # make credentials.txt if it does not exist #
    if not os.path.exists("credentials.txt"): open("credentials.txt", "w")

    with open("credentials.txt", "r+") as f:
        # checking if credentials.txt contains cookie and reqVerToken #
        lines = f.readlines()
        if len(lines) != 2:
            print("Invalid tokens.txt file!")
            print("""Instructions on how to find cookie and token:
            1. Go to the Smart Revise questions section
            2. Hold CTRL+SHIFT+I or right click and press "Inspect" to open inspect element
            3. In the top bar, click "Network"
            4. Complete a question (Does not matter if the question is correct)
            5. Find the request that looks like: /answer/cb?xxxxxxxxxxxxxxx
            6. Click that request, and click "Headers"
            7. Scroll to "Request Headers"
            8. Copy the headers labelled "RequestVerificationToken" and "Cookie" (can be easier if you right click the value and press \"Copy Value\")
            9. Paste the headers here!
            """)

            requestVerificationToken = input("Enter \"RequestVerificationToken\" header:\n")
            cookie = input("Enter \"Cookie\" header:\n")

            # write new reqVerToken and cookie to file #
            f.write(f"{requestVerificationToken}\n{cookie}")

# ------------------------------------------------ #

def addCredentialHeaders(headers):

    # adding credential headers from credentials file to other headers #
    with open("credentials.txt", "r+") as f:
        lines = f.readlines()
        headers["RequestVerificationToken"], headers["Cookie"] = lines[0].strip("\n"), lines[1].strip("\n")

    return headers

# ------------------------------------------------ #

def getRespDict(response):

    # get raw response body #
    respBody = response.read()

    try:
        # standard smartrevise responses are gzipped #
        respBody = gzip.decompress(respBody)
        respDict = json.loads(respBody.decode())

    except:
        # check if response is not gzipped, return blank dict if fail #
        try:    respDict = json.loads(respBody)
        except: respDict = {}

    return respDict

# ------------------------------------------------ #

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

# ------------------------------------------------ #

def displayAnswerStatus(respDict):

    with open("config.json", "r") as f:
        configJson = json.load(f)

    # correct msg #
    if respDict["previousCorrectAnswerId"] == respDict["previousAnswerId"]:
        print("Correct!")
        time.sleep(configJson["cooldown"])

    # unknown answer msg #
    elif respDict["previousAnswerId"] == -1:
        print(respDict["previousAdviceText"])
        time.sleep(configJson["cooldown"])
        input("Press enter for next question!")

    # incorrect msg #
    else:
        print(f"Incorrect.\n{respDict["previousAdviceText"]}")
        time.sleep(configJson["cooldown"])
        input("Press enter for next question!")
    
# ------------------------------------------------ #

def displayQuestion():

    # clear terminal #
    print("\n"*20)

    with open("respDump.json", "r") as f:
        respDict = json.load(f)

    # print question and related answer options #
    print(f"{respDict["questionText"]}\n")
    for i in range(len(respDict["answers"])):
        print(f"{respDict["answers"][i]["answerText"]}\n^{[i+1]}^\n")

# ------------------------------------------------ #

def getAnswerInput():

    # placeholder nextAnsInput to start not in range #
    nextAnsInput = -12345

    # repeat until valid answer input #
    while nextAnsInput not in range(-2,4):
        nextAnsInput = int(input("Enter answer ID... (0 for unknown, -1 for exit)\n"))-1

    return nextAnsInput

# ------------------------------------------------ #

def generateNextBody(answerId):

    with open("respDump.json", "r") as f:
        respDict = json.load(f)

    with open("config.json", "r") as f:
        body = json.load(f)["defaultBody"]

    # finding internal answer id relating to user input (if not unknown/exiting) #
    if answerId >= 0:
        nextAnsId = respDict["answers"][answerId]["id"]
    else: 
        nextAnsId = answerId

    # preparing next body #
    body["proposedAnswerId"] = nextAnsId
    body["QuestionHash"] = respDict.get("questionHash")
    body["PackInstanceEntryId"] = respDict.get("packInstanceId")
    body["QuestionOrdinal"] = respDict.get("questionOrdinal")

    return body

# ------------------------------------------------ #