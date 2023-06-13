import logging
from SPARQLWrapper import SPARQLWrapper, JSON
from wikidataintegrator import wdi_core, wdi_login
import json
from login import USER, PASSWORD
import time
from tqdm import tqdm
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).parent.resolve()
RESULTS = HERE.parent.joinpath("results").resolve()

# Setup logging
logging.basicConfig(
    filename="error_log.log",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)

# Define your sources and their associated WDItemID
sources = {
    # "ICD10CM": "Q119459345", mappings are seemly of not-so-great quality
    "FMA": "Q119459341",
    "GO": "Q119459342",
    "HGNC": "Q119459343",
    "ORPHANET": "Q119459347",
    "NCBI": "Q119459346",
    "MSH": "Q118645058",
}

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

# Log in to Wikidata using credentials from login.py
login = wdi_login.WDLogin(USER, PASSWORD)

# Iterate over each source
for name, wditem in sources.items():
    # Load the JSON file
    data = json.loads(
        RESULTS.joinpath(f"cui_wikidata_from_{name}_unique.json").read_text()
    )

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

        date = datetime.now()
        timeStringNow = date.strftime("+%Y-%m-%dT00:00:00Z")
        refRetrieved = wdi_core.WDTime(timeStringNow, prop_nr="P813", is_reference=True)

        references = [
            [
                wdi_core.WDItemID(value=wditem, prop_nr="P887", is_reference=True),
                wdi_core.WDItemID(
                    value="Q118645236", prop_nr="P248", is_reference=True
                ),
                refRetrieved,
            ]
        ]
        # Create a new string statement
        statement = wdi_core.WDString(
            value=umls, prop_nr="P2892", references=references
        )

        # Set the statement
        wd_item.update([statement])
        time.sleep(0.5)
        # Write the item
        try:
            wd_item.write(
                login,
                bot_account=False,
                edit_summary="Updated UMLS CUI with heuristic based on UMLS 2023AA release.",
            )
            break
        except Exception as e:
            # Log the error
            logging.error(
                f"Source: {name}, QID: {wikidata_id}, UMLS CUI: {umls}, Error: {str(e)}"
            )
            continue
