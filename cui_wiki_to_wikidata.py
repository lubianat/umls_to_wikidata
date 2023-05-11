import json
from wdcuration import get_qids_from_enwiki_pages

# Load the JSON file
with open("cui_wiki.json") as file:
    cui_wiki = json.load(file)

# Extract the values and add them to a list
values_list = list(cui_wiki.values())

# Print the list of values


wikipedia2qid = get_qids_from_enwiki_pages(values_list)

# Create a new dictionary with CUI-to-Wikidata mappings
cui_wikidata_dict = {}
for cui, value in cui_wiki.items():
    if value in wikipedia2qid:
        cui_wikidata_dict[cui] = wikipedia2qid[value]

# Convert the dictionary to JSON format
cui_wikidata_json = json.dumps(cui_wikidata_dict, indent=2)

# Save the CUI-to-Wikidata dictionary to a file
with open("cui_wikidata.json", "w") as file:
    json.dump(cui_wikidata_dict, file, indent=2)
