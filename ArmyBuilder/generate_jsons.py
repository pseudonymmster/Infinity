"""Pull current Infinity JSONs and save them to ./JSONs folder."""
import json
import requests


def get_json_from_url(url_str):
    """Return json from infinity site."""
    req_headers = {"Origin": "https://infinitytheuniverse.com"}
    get_response = requests.get(url_str, headers=req_headers)
    print("{} response code: {}".format(url_str, get_response.status_code))
    return get_response.json()


def get_metadata():
    """Get metadata JSON from CB's api."""
    url = "https://api.corvusbelli.com/army/infinity/en/metadata"
    return get_json_from_url(url)


metadata_raw_json = get_metadata()


def string_cleanup(string_to_cleanup):
    """Replace character codes with non-accented characters."""
    replacements = {"\\u00a0": " ",
                    "\\u00ba": "",
                    "\\u00c0": "A",  # À
                    "\\u00c1": "A",  # Á
                    "\\u00c2": "A",  # Â
                    "\\u00c4": "A",  # Ä
                    "\\u00c8": "E",  # È
                    "\\u00c9": "E",  # É
                    "\\u00cc": "I",  # Ì
                    "\\u00cd": "I",  # Í
                    "\\u00cf": "I",  # Ï
                    "\\u00d1": "N",  # Ñ
                    "\\u00d2": "O",  # Ò
                    "\\u00d3": "O",  # Ó
                    "\\u00d9": "U",  # Ù
                    "\\u00da": "U",  # Ú
                    "\\u00e0": "a",  # à
                    "\\u00e1": "a",  # á
                    "\\u00e2": "a",  # â
                    "\\u00e4": "a",  # ä
                    "\\u00e8": "e",  # è
                    "\\u00e9": "e",  # é
                    "\\u00ec": "i",  # ì
                    "\\u00ed": "i",  # í
                    "\\u00ef": "i",  # ï
                    "\\u00f1": "n",  # ñ
                    "\\u00f2": "o",  # ò
                    "\\u00f3": "o",  # ó
                    "\\u00f9": "u",  # ù
                    "\\u00fa": "u",  # ú
                    "\\u0100": "A",  # Ā
                    "\\u0101": "a",  # ā
                    "\\u0102": "A",  # Ă
                    "\\u0103": "a",  # ă
                    "\\u0112": "E",  # Ē
                    "\\u0113": "e",  # ē
                    "\\u011a": "E",  # Ě
                    "\\u011b": "E",  # ě
                    "\\u012a": "I",  # Ī
                    "\\u012b": "i",  # ī
                    "\\u014c": "O",  # Ō
                    "\\u014d": "o",  # ō
                    "\\u014e": "O",  # Ŏ
                    "\\u014f": "o",  # ŏ
                    "\\u016a": "U",  # Ū
                    "\\u016b": "u",  # ū
                    "\\u016c": "U",  # Ŭ
                    "\\u016d": "u",  # ŭ
                    "\\u01cd": "A",  # Ǎ
                    "\\u01ce": "a",  # ǎ
                    "\\u01cf": "I",  # Ǐ
                    "\\u01d0": "i",  # ǐ
                    "\\u01d1": "O",  # Ǒ
                    "\\u01d2": "o",  # ǒ
                    }
    cleaned_up_string = string_to_cleanup
    for code, value in replacements.items():
        cleaned_up_string = cleaned_up_string.replace(code, value)
    return cleaned_up_string


traits = []


def get_keywords(trait_type):
    """Return list of keywords."""
    if trait_type in ["equips", "skills", "weapons"]:
        for trait_json in metadata_raw_json[trait_type]:
            trait_name = trait_json["name"]
            if trait_name not in traits:
                traits.append(trait_name)


def write_to_file(filename_arg, txt_to_write):
    """Save a string txt_to_write to a file with name filename_arg."""
    output = string_cleanup(txt_to_write)
    with open(filename_arg, "w") as write_file:
        write_file.write(output)


def write_to_json(filename_arg, json_to_write):
    """Write a json object json_to_write to a file with name filename_arg."""
    json_filename = "jsons/{}.json".format(filename_arg)
    json_string = json.dumps(json_to_write)
    write_to_file(json_filename, json_string)


def generate_searchable_keywords():
    """Create list of keywords and write them to searchableKeywords.js."""
    traits.sort()
    traits_str = json.dumps(traits)
    searchable_keywords_txt = "traits = " + traits_str
    write_to_file("searchableKeywords.js", searchable_keywords_txt)


# Test code below
metadata_groups = ["factions", "ammunitions", "weapons", "skills", "equips"]
write_to_json("raw", metadata_raw_json)
for group in metadata_groups:
    get_keywords(group)
    write_to_json(group, metadata_raw_json[group])
generate_searchable_keywords()

for faction in metadata_raw_json["factions"]:
    faction_id = faction["id"]
    filename = faction_id
    if "{}".format(faction_id) != "901":
        url = "https://api.corvusbelli.com/army/units/en/{}".format(faction_id)
        army_json = get_json_from_url(url)
        write_to_json(filename, army_json)
