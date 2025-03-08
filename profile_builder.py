"""Format Infinity profiles to more readable/usable form."""
import json


def load_json_from(filename):
    """Return json data from a file with name filename."""
    json_data = {}
    try:
        with open(filename, 'r') as file:
            json_data = json.load(file)
    except:
        pass
        # print("Error reading " + str(filename))
    return json_data


def format_extra_string(extra_json):
    """Return formatted string form of extra json object."""
    extra_str = ""
    for extra_id in extra_json:
        extra_data = extras_by_id[extra_id]
        extra_name = extra_data["name"]
        if extra_data["type"].lower() == "distance":
            extra_in_inches = convert_to_inch(extra_name)
            extra_name = "+{}\"".format(extra_in_inches)
        extra_str += " ({})".format(extra_name)
    return extra_str


def names_from_json_and_dict(json_list, lookup_dict):
    """Get names from lookup_dict based on ids from json_list."""
    names = []
    for json_row in json_list:
        row_id = json_row["id"]
        name = lookup_dict[row_id]["name"]
        if "extra" in json_row:
            name += format_extra_string(json_row["extra"])
        names.append(name)
    return names


def convert_to_inch(cm_value):
    """Convert cm value to inch value (note: CB uses 4/10)."""
    return int(float(cm_value) * 4 / 10)


def convert_move_to_inch(moves_in_cm):
    """Convert move list from cm to inches."""
    moves_in_inches = []
    for cm_move in moves_in_cm:
        inch_move = convert_to_inch(cm_move)
        moves_in_inches.append(inch_move)
    return moves_in_inches


def build_profile_from_unit_data(unit_data):
    """Take a single unit json data and format to readable stats."""
    for profile_group in unit_data["profileGroups"]:
        formatted_profile = {"statLines": []}
        statline_count = len(profile_group["profiles"])
        for raw_statline in profile_group["profiles"]:
            new_statline = {}
            new_statline["name"] = raw_statline["name"]
            new_statline["mov"] = convert_move_to_inch(raw_statline["move"])
            new_statline["cc"] = raw_statline["cc"]
            new_statline["bs"] = raw_statline["bs"]
            new_statline["ph"] = raw_statline["ph"]
            new_statline["wip"] = raw_statline["wip"]
            new_statline["arm"] = raw_statline["arm"]
            new_statline["bts"] = raw_statline["bts"]
            new_statline["w"] = raw_statline["w"]
            new_statline["s"] = raw_statline["s"]
            new_statline["ava"] = raw_statline["ava"]
            new_statline["is_str"] = raw_statline["str"]
            equipment = names_from_json_and_dict(raw_statline["equip"], equipment_by_id)
            new_statline["equipment"] = equipment
            skills = names_from_json_and_dict(raw_statline["skills"], skills_by_id)
            new_statline["skills"] = skills
            formatted_profile["statLines"].append(new_statline)
        if statline_count > 1:
            print(str(formatted_profile))


def update_id_dict(json_data, dict_to_update):
    """Update dict_to_update with id/value pairs."""
    for json_row in json_data:
        json_id = json_row["id"]
        dict_to_update[json_id] = json_row


def update_filter_dicts(filters_data):
    """Use filters_data to update all of the filters dicts."""
    def update_filter_type(filter_type, existing_dict):
        """Use filters_data[filter_type) to update existing_dict."""
        update_id_dict(filters_data[filter_type], existing_dict)

    update_filter_type("weapons", weapons_by_id)
    update_filter_type("equip", equipment_by_id)
    update_filter_type("skills", skills_by_id)
    update_filter_type("extras", extras_by_id)
    update_filter_type("peripheral", peripherals_by_id)
    update_filter_type("category", categories_by_id)
    update_filter_type("ammunition", ammo_by_id)
    update_filter_type("chars", characteristics_by_id)
    update_filter_type("type", unit_type_by_id)


factions_json = load_json_from("factions.json")
# the following are populated in the update_filter_dicts() function
weapons_by_id = {}
equipment_by_id = {}
skills_by_id = {}
extras_by_id = {}
peripherals_by_id = {}
categories_by_id = {}
ammo_by_id = {}
characteristics_by_id = {}
unit_type_by_id = {}

for faction_row in factions_json:
    faction_filename = str(faction_row["id"]) + ".json"
    faction_data = load_json_from(faction_filename)

    if faction_data:
        update_filter_dicts(faction_data["filters"])

        for unit in faction_data["units"]:
            build_profile_from_unit_data(unit)
