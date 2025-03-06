import json

def loadJsonDataFromFileName(fileName):
    jsonData = {}
    try:
        with open(fileName, 'r') as file:
            jsonData = json.load(file)
            file.close()
    except:
        pass
        #print("Error reading " + str(fileName))
    return jsonData


def formatExtraStr(extraJsonObj):
    extraStr = ""
    for extraId in extraJsonObj:
        extraData = extrasDict[extraId]
        extraName = extraData["name"]
        if extraData["type"].lower() == "distance":
            extraFloat = float(extraName)
            extraFloatInInch = convertToInch(extraFloat)
            extraName = "+{}\"".format(extraFloatInInch)
        extraStr += " ({})".format(extraName)
    return extraStr

def buildListFromJsonAndDict(jsonList, lookupDict):
    nameList = []
    for jsonObj in jsonList:
        objId = jsonObj["id"]
        name = lookupDict[objId]["name"]
        if "extra" in jsonObj:
            name += formatExtraStr(jsonObj["extra"])
        factionData
        nameList.append(name)
    return nameList


def convertToInch(cmValue):
    return int(cmValue * 4 / 10)


def convertToMoveToInch(listOfCmMove):
    listOfInchMove = []
    for cmMove in listOfCmMove:
        inchMove = convertToInch(cmMove)
        listOfInchMove.append(inchMove)
    return listOfInchMove

def buildProfileFromUnit(unitData):
    for profileGroup in unitData["profileGroups"]:
        formattedProfile = {"statLines": []}
        numberOfStatLines = 0
        for statLine in profileGroup["profiles"]:
            formattedStatLine = {}
            #print(str(statLine["name"]))
            formattedStatLine["name"] = statLine["name"]
            formattedStatLine["mov"] = convertToMoveToInch(statLine["move"])
            formattedStatLine["cc"] = statLine["cc"]
            formattedStatLine["bs"] = statLine["bs"]
            formattedStatLine["ph"] = statLine["ph"]
            formattedStatLine["wip"] = statLine["wip"]
            formattedStatLine["arm"] = statLine["arm"]
            formattedStatLine["bts"] = statLine["bts"]
            formattedStatLine["w"] = statLine["w"]
            formattedStatLine["s"] = statLine["s"]
            formattedStatLine["ava"] = statLine["ava"]
            formattedStatLine["is_str"] = statLine["str"]
            formattedStatLine["equipment"] = buildListFromJsonAndDict(statLine["equip"], equipmentDict)
            formattedStatLine["skills"] = buildListFromJsonAndDict(statLine["skills"], skillsDict)
            formattedProfile["statLines"].append(formattedStatLine)
            numberOfStatLines += 1
        #formattedStatLine["profileOptions"] = createOptionsList(
        if numberOfStatLines > 1:
            print(str(formattedProfile))


def updateIdDict(idNameJson, passedDict = {}):
    idNameDict = passedDict
    for jsonRow in idNameJson:
        idIndex = jsonRow["id"]
        nameValue = jsonRow["name"]
        idNameDict[idIndex] = jsonRow
    return idNameDict


def updateIdDictFromFileName(filename):
    data = loadJsonDataFromFileName(filename)
    return updateIdDict(data)


def updateFilterDicts(factionDataArg):
    factionFiltersData = factionDataArg["filters"]

    def updateDictWithFilterData(keyStr, existingDict):
        return updateIdDict(factionFiltersData[keyStr], existingDict)

    updateDictWithFilterData("weapons", weaponsDict)
    updateDictWithFilterData("equip", equipmentDict)
    updateDictWithFilterData("skills", skillsDict)
    updateDictWithFilterData("extras", extrasDict)
    updateDictWithFilterData("peripheral", peripheralsDict)
    updateDictWithFilterData("category", categoriesDict)
    updateDictWithFilterData("ammunition", ammoDict)
    updateDictWithFilterData("chars", characteristicsDict)
    updateDictWithFilterData("type", unitTypeDict)


factionsJson = loadJsonDataFromFileName("factions.json")
# the following are populated in the updateFilterDicts() function
weaponsDict = {}
equipmentDict = {}
skillsDict = {}
extrasDict = {}
peripheralsDict = {}
categoriesDict = {}
ammoDict = {}
characteristicsDict = {}
unitTypeDict = {}

for factionMetadata in factionsJson:
    factionFileName = str(factionMetadata["id"]) + ".json"
    factionData = loadJsonDataFromFileName(factionFileName)

    if factionData:
        updateFilterDicts(factionData)

        for unit in factionData["units"]:
            buildProfileFromUnit(unit)
