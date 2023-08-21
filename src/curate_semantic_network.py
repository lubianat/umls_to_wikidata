from wdcuration import generate_curation_spreadsheet
from pathlib import Path

HERE = Path(__file__).parent.resolve()
DATA = HERE.parent.joinpath('data').resolve()
RESULTS = HERE.parent.joinpath('results').resolve()

generate_curation_spreadsheet(identifiers_property="P11955",curation_table_path=RESULTS/"semantic_network_clean2.csv",description_term_lookup="", output_file_path=RESULTS/"curation_sn.csv")