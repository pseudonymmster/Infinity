import json

def load_json_from(filename):
    json_data = {}
    try:
        with open(filename, 'r') as file:
            json_data = json.load(file)
            file.close()
    except:
        pass
        #print("Error reading " + str(filename))
    return json_data


def format_extra_string(extra_json):
    extraStr = ""
    for extra_id in extra_json:
        extraData = extrasDict[extra_id]
        extraName = extraData["name"]
        if extraData["type"].lower() == "distance":
            extraFloat = float(extraName)
            extraFloatInInch = convert_to_inch(extraFloat)
            extraName = "+{}\"".format(extraFloatInInch)
        extraStr += " ({})".format(extraName)
    return extraStr

def build_list_from_json_and_dict(json_list, lookup_dict):
    names = []
    for json_row in json_list:
        row_id = json_row["id"]
        name = lookup_dict[row_id]["name"]
        if "extra" in json_row:
            name += format_extra_string(json_row["extra"])
        names.append(name)
    return names


def convert_to_inch(cm_value):
    return int(cm_value * 4 / 10)


def convert_move_to_inch(moves_in_cm):
    moves_in_inches = []
    for cm_move in moves_in_cm:
        inch_move = convert_to_inch(cm_move)
        moves_in_inches.append(inch_move)
    return moves_in_inches

def buildProfileFromUnit(unitData):
    for profileGroup in unitData["profileGroups"]:
        formattedProfile = {"statLines": []}
        numberOfStatLines = 0
        for statLine in profileGroup["profiles"]:
            formattedStatLine = {}
            #print(str(statLine["name"]))
            formattedStatLine["name"] = statLine["name"]
            formattedStatLine["mov"] = convert_move_to_inch(statLine["move"])
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
            formattedStatLine["equipment"] = build_list_from_json_and_dict(statLine["equip"], equipmentDict)
            formattedStatLine["skills"] = build_list_from_json_and_dict(statLine["skills"], skillsDict)
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
    data = load_json_from(filename)
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


factionsJson = load_json_from("factions.json")
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
    factionData = load_json_from(factionFileName)

    if factionData:
        updateFilterDicts(factionData)

        for unit in factionData["units"]:
            buildProfileFromUnit(unit)
