import os
from pathlib import Path
from nmr_html_parser import souping


def column(path, filepath):
    inp_file = Path(path)
    out_file = Path(filepath)
    if not out_file.parent.exists():
        os.makedirs(out_file.parent)

    soup = souping.inputs(inp_file)
    headers = souping.soup_id_headers(soup)
    rows = souping.soup_id_rows(soup)
    comps = souping.soup_comp_id(soup)

    # Used stored results from previous functions calls to run
    compound_num = souping.compound_number(comps, headers)
    columns = souping.get_columns(rows, headers)
    return columns
