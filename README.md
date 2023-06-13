
Connecting UMLS CUIs to Wikidata using openly available resources. 

cui_wiki.json file obtained from https://github.com/afshinrahimi/wikiumls/blob/master/data/cui_wiki.json, originally from this publication: 

https://www.wikidata.org/wiki/Q105870539

It has, however, a large number of incorrect matches. 
The taxa seem to have a high score, so one way to go is to subset the dataset just for the taxa on Wikidata.

cui_wikidata_from_mesh.json obtained with `parse_umls_to_wikidata.py` on the output of 
```
grep '|MSH|' MRCONSO.RRF | awk -F '|' '$7=="Y"{print $1 "|" $14 }' | sort -u > mesh.txt
```

On UMLS' 2023 MRCONSO.RRF release



Other possible sources of UMLS to Wikidata matching: 

* https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/ICD10CM/index.html
* https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/GO/index.html
* https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/HGNC/index.html
* https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/ORPHANET/index.html
* https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/FMA/index.html
* https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/NCBI/index.html

Other sources on UMLS are listed on nlm.nih.gov/research/umls/sourcereleasedocs/index.html