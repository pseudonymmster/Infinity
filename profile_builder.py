"""Format Infinity profiles to more readable/usable form."""
import json


found_dict = {}

name_by_cb_name = {"equip": "equipment",
                   "peripheral": "peripherals",
                   "category": "categories",
                   "ammunition": "ammo",
                   "chars": "characteristics",
                   "type": "unit type"
                   }

cb_name_by_name = {v: k for k, v in name_by_cb_name.items()}

def get_id_lookup_dict(name_of_dict):
    return {"weapons": weapons_by_id,
            "equipment": equipment_by_id,
            "skills": skills_by_id,
            "extras": extras_by_id,
            "peripherals": peripherals_by_id,
            "categories": categories_by_id,
            "ammo": ammo_by_id,
            "characteristics": characteristics_by_id,
            "unit type": unit_type_by_id,
            }[name_of_dict]


def change_value_if_present(key, lookup_dict):
    """Return value if in lookup_dict, otherwise return original key"""
    value = key
    if key in lookup_dict:
        value = lookup_dict[key]
    return value


def get_cb_name(name):
    """Return CB's name, if different; otherwise return original"""
    return change_value_if_present(name, cb_name_by_name)


def get_name(cb_name):
    """Return name, if different from CB's name; otherwise return original"""
    return change_value_if_present(cb_name, name_by_cb_name)


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


def get_factions_json():
    """Get factions data."""
    return load_json_from("jsons/factions.json")


def format_extra_string(extra_json):
    """Return formatted string form of extra json object."""
    extra_str = ""
    if extra_json:
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
        if isinstance(json_row, int):
            row_id = json_row
            name = lookup_dict[row_id]["name"]
            names.append(name)
        elif "id" in json_row:
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


def build_statlines(profile_group, name_slug):
    statlines = []
    for raw_statline in profile_group["profiles"]:
        # These are different statlines of same unit e.g. transmutation
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
        characteristics = names_from_json_and_dict(raw_statline["chars"], characteristics_by_id)
        new_statline["characteristics"] = characteristics
        unit_type = unit_type_by_id[raw_statline["type"]]["name"]
        new_statline["unit type"] = unit_type
        
        for skill in new_statline["skills"]:
            if "Super-Jump (+8" in skill and "REINF: " not in new_statline["name"]:
                found_dict[name_slug] = skill
        
        statlines.append(new_statline)
    return statlines


def get_properties_by_type(trooper_option, property_type):
    property_type_cb = get_cb_name(property_type)
    data_by_id = get_id_lookup_dict(property_type)
    properties = [] # names_from_json_and_dict(trooper_option[property_type_cb], data_by_id)
    for property_obj in trooper_option[property_type_cb]:
        formatted_property = {}
        if property_obj and "id" in property_obj:
            try:
                property_data = data_by_id[property_obj["id"]]
                formatted_property = property_data["name"]
                if "extra" in property_obj:
                    formatted_property += format_extra_string(property_obj["extra"])
                if "q" in property_obj:
                    formatted_property = str(property_obj["q"]) + "x " + formatted_property
            except KeyError:
                formatted_property = str(property_obj["id"])
        if "extra" in property_obj:
            pass
        properties.append(formatted_property)
    return properties


def format_profile(trooper_option):
    profile_details = {}
    profile_details["weapons"] = get_properties_by_type(trooper_option, "weapons")
    profile_details["equipment"] = get_properties_by_type(trooper_option, "equipment")
    profile_details["skills"] = get_properties_by_type(trooper_option, "skills")
    profile_details["peripherals"] = get_properties_by_type(trooper_option, "peripherals")
    return profile_details


def build_team_profile(unit_data):
    """Take raw "units" json data and format to readable stats."""
    team_profile = {}
    team_profile["name"] = unit_data["slug"]
    team_profile["factions"] = unit_data["factions"]
    team_profile["units"] = []
    for trooper in unit_data["profileGroups"]:
        # These are different units under the same profile (Carmen & Batard)
        formatted_trooper = {}
        formatted_trooper["statlines"] = build_statlines(trooper, team_profile["name"])
        formatted_trooper["profiles"] = []
        if trooper["category"]:
            formatted_trooper["category"] = categories_by_id[trooper["category"]]
        for specific_profile in trooper["options"]:
            formatted_profile = format_profile(specific_profile)
            formatted_trooper["profiles"].append(formatted_profile)
        team_profile["units"].append(formatted_trooper)
    # if "kerail" in team_profile["name"]:
        # example of complicated unit; multiple statlines, multiple troops
        # print(json.dumps(team_profile))



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


factions_json = get_factions_json()
factions = []
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
    faction_filename = "jsons/"+str(faction_row["id"]) + ".json"
    faction_data = load_json_from(faction_filename)

    if faction_data:
        factions.append(faction_data)
        update_filter_dicts(faction_data["filters"])

for faction in factions:
    for unit in faction["units"]:
        # "units" aren't necessarily 1 trooper. e.g. Carmen & Batard
        build_team_profile(unit)

print(json.dumps(found_dict))
print(json.dumps(len(found_dict)))

# input("\nPress Enter to continue...")
