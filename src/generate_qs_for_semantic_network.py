from wdcuration import get_quickstatements_for_curated_sheet
from pathlib import Path

HERE = Path(__file__).parent.resolve()
DATA = HERE.parent.joinpath('data').resolve()
RESULTS = HERE.parent.joinpath('results').resolve()
qs = get_quickstatements_for_curated_sheet(curated_sheet_path=RESULTS / "curation_sn.csv", wikidata_property="P11955", dropnas=True)

RESULTS.joinpath("qs.txt").write_text(qs)