from SPARQLWrapper import SPARQLWrapper, JSON

# Create a SPARQLWrapper instance
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

# Write your query
sparql.setQuery(
    """
    SELECT ?item ?itemLabel ?mesh_id
    WHERE 
    {
      ?item wdt:P486 ?mesh_id.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
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


cui_to_qid = {}
# Open the output file and map each line to Wikidata QIDs using the MeSH term
with open("mesh.txt", "r") as f:
    for line in f:
        parts = line.strip().split("|")
        cui = parts[0]
        mesh = parts[2]
        qid = mesh_to_qid.get(mesh)
        if qid:
            cui_to_qid[cui] = qid

import json
from pathlib import Path

HERE = Path(__file__).parent.resolve()
HERE.joinpath("cui_wikidata_from_mesh.json").write_text(
    json.dumps(cui_to_qid, indent=4, sort_keys=True)
)
