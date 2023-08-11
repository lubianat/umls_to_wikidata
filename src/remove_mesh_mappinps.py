import requests
from login import USER, PASSWORD
import json
from wikibaseintegrator import WikibaseIntegrator
from wikibaseintegrator.wbi_helpers import remove_claims
from wikibaseintegrator.wbi_login import Clientlogin

from wdcuration import query_wikidata
from wikibaseintegrator.wbi_config import config as wbi_config
from tqdm import tqdm
wbi_config['USER_AGENT'] = 'TiagoLubianaBot'

query = """


SELECT ?item ?claim ?n_claims WHERE {
  
{SELECT ?item (COUNT(DISTINCT ?claim) as ?n_claims) 
WHERE {
  ?item wdt:P2892 ?any .
  ?item p:P2892 ?claim . 
  ?claim prov:wasDerivedFrom [ pr:P887 wd:Q118645058 ] .
} GROUP BY ?item
}
  ?item p:P2892 ?claim . 
  ?claim prov:wasDerivedFrom [ pr:P887 wd:Q118645058 ] .  
  
}

"""

results = query_wikidata(query)
login_instance = Clientlogin(user=USER, password=PASSWORD)

wbi = WikibaseIntegrator(login=login_instance)


target_qids = [ result["item"].split("/")[-1] for result in results if int(result["n_claims"]) >1]

target_claims = [result["claim"][-30:] for result in results if int(result["n_claims"]) >1]



target_qids = list(set(target_qids))
target_qids.sort()

for qid in tqdm(target_qids):
    item = wbi.item.get(entity_id=qid)
    claims = item.claims
    for claim in claims:
        claim_json = claim.get_json()
        if claim_json["id"][-30:] in target_claims:
            claim_json = claim.get_json()
            claim.remove()
    item.write(summary="Removed UMLS CUI with MeSH heuristic due to high rate of broad matches.") 