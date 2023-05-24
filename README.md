
Connecting UMLS CUIs to Wikidata using openly available resources. 

cui_wiki.json file obtained from https://github.com/afshinrahimi/wikiumls/blob/master/data/cui_wiki.json, originally from this publication: 

https://www.wikidata.org/wiki/Q105870539

cui_wikidata_from_mesh.json obtained with `parse_umls_to_wikidata.py` on the output of 
```
grep '|MSH|' MRCONSO.RRF | awk -F '|' '$7=="Y"{print $1 "|" $7 "|" $14 "|" $15}' | sort -u > output.txt
```

On UMLS' 2023 MRCONSO.RRF release