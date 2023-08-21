from pathlib import Path

HERE = Path(__file__).parent.resolve()
DATA = HERE.parent.joinpath('UMLS_data').resolve()
RESULTS = HERE.parent.joinpath('results').resolve()

import pandas as pd 


df = pd.read_csv(DATA / "SRDEF", sep="|", index_col=False)

print(df)

df.to_csv(RESULTS / "semantic_network_clean.csv", index=False)