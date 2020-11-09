import os
from pathlib import Path
from nmr_html_parser import soup_test

def column(path, filepath):
    inp_file = Path(path)
    out_file = Path(filepath)
    if not out_file.parent.exists():
        os.makedirs(out_file.parent)

    soup = soup_test.inputs(inp_file)
    headers = soup_test.soup_id_headers(soup)
    rows = soup_test.soup_id_rows(soup)
    comps = soup_test.soup_comp_id(soup)

    # Used stored results from previous functions calls to run
    compound_num = soup_test.compound_number(comps, headers)
    columns = soup_test.get_columns(rows, headers)
    return columns