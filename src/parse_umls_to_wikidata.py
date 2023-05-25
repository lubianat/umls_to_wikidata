from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent.resolve()
DATA = HERE.parent.joinpath("UMLS_data").resolve()
RESULTS = HERE.parent.joinpath("results").resolve()
# Create a SPARQLWrapper instance
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

# Write your query
sparql.setQuery(
    """
    SELECT ?item  ?mesh_id
    WHERE 
    {
      ?item wdt:P486 ?mesh_id.
    }
"""
)

# Set the return format to JSON
sparql.setReturnFormat(JSON)

# Execute the query and convert the result to a Python dictionary
results = sparql.query().convert()

# Create a MeSH to QID dictionary
mesh_to_qid = {
    result["mesh_id"]["value"]: result["item"]["value"].split("/")[-1]
    for result in results["results"]["bindings"]
}

# Create a dictionary to store CUI:MeSH mappings
mesh_to_cui = defaultdict(list)

# Open the output file and map each line to MeSH terms
with open(DATA.joinpath("mesh.txt"), "r") as f:
    for line in f:
        parts = line.strip().split("|")
        cui = parts[0]
        mesh = parts[1]
        mesh_to_cui[mesh].append(cui)

# Create a dictionary to store CUI to QID mappings, excluding CUIs with more than one MeSH term
cui_to_qid = {}
for mesh, cui_list in mesh_to_cui.items():
    if (
        len(cui_list) == 1
    ):  # only add to dictionary if there is a single CUI for the MeSH
        cui = cui_list[0]
        qid = mesh_to_qid.get(mesh)
        if qid:
            cui_to_qid[cui] = qid

import json
from pathlib import Path

# Save CUI to QID mappings as a JSON file
RESULTS.joinpath("cui_wikidata_from_mesh_unique.json").write_text(
    json.dumps(cui_to_qid, indent=4, sort_keys=True)
)
