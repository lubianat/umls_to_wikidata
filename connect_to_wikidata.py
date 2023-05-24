import logging
from SPARQLWrapper import SPARQLWrapper, JSON
from wikidataintegrator import wdi_core, wdi_login
import json
from login import USER, PASSWORD
import time
from tqdm import tqdm

# Setup logging
logging.basicConfig(
    filename="error_log.log",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)

# Fetch all UMLS IDs from Wikidata
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery(
    """
    SELECT ?umls WHERE {
        ?item wdt:P2892 ?umls.
    }
"""
)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

# Create a set of existing UMLS IDs
existing_umls_ids = {
    result["umls"]["value"] for result in results["results"]["bindings"]
}

# Load the JSON file
with open("cui_wikidata.json", "r") as f:
    data = json.load(f)

# Log in to Wikidata using credentials from login.py
login = wdi_login.WDLogin(USER, PASSWORD)

# Iterate over the data
for umls, wikidata_id in tqdm(data.items()):
    # Skip if UMLS ID already exists
    if umls in existing_umls_ids:
        continue

    # Create a new data object
    wd_item = wdi_core.WDItemEngine(
        wd_item_id=wikidata_id,
        new_item=False,
    )
    wd_item.get_wd_json_representation()

    references = [
        [wdi_core.WDItemID(value="Q105870539", prop_nr="P248", is_reference=True)]
    ]
    # Create a new string statement
    statement = wdi_core.WDString(value=umls, prop_nr="P2892", references=references)

    # Set the statement
    wd_item.update([statement])
    time.sleep(0.5)
    # Write the item
    try:
        wd_item.write(login, bot_account=False)
    except Exception as e:
        # Log the error
        logging.error(f"QID: {wikidata_id}, UMLS CUI: {umls}, Error: {str(e)}")
        continue
