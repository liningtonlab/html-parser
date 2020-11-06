import os
from pathlib import Path
from nmr_html_parser import soup_test


def parse(path, filepath):
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
    atom_index = columns[0]
    hspec, cspec, hmult, jcoup, ctype = soup_test.column_id_cleaner_list(columns)
    float_hspec = soup_test.column2dlist_string_to_float(hspec)
    float_cspec = soup_test.column2dlist_string_to_float(cspec)

  
    # 1. First check for float_spec
    if float_cspec and float_hspec:
        soup_test.tableto_csv(
            *soup_test.data_to_grid(compound_num, atom_index, float_cspec, ctype, float_hspec, hmult, jcoup), filepath)

    # 1A. If not either spec, with columns containing specific data check float averages as last resort.
    elif not float_cspec:
        columns = soup_test.column2dlist_string_to_float(columns)
        float_cspec, float_hspec = soup_test.get_float_avg(columns)
        ctype = soup_test.blanks_list(float_cspec)
    elif not float_hspec:
        columns = soup_test.column2dlist_string_to_float(columns)
        float_cspec, hspec = soup_test.get_float_avg(columns)
        if hspec:
            float_hspec = hspec
            hmult = soup_test.blanks_list(float_hspec)
            jcoup = soup_test.blanks_list(float_hspec)
    # 2. Second pass for float of either spec
    if float_cspec and float_hspec and not ctype:
        soup_test.tableto_csv(*soup_test.data_to_grid_Cb(compound_num, atom_index, float_cspec, float_hspec, hmult, jcoup),filepath)
    elif float_cspec and float_hspec:
        soup_test.tableto_csv(
            *soup_test.data_to_grid(compound_num, atom_index, float_cspec, ctype, float_hspec, hmult, jcoup),filepath)
    elif not float_hspec:
        soup_test.tableto_csv(*soup_test.data_to_grid_Ha(compound_num, atom_index, float_cspec, ctype),filepath)
    elif float_hspec and not hmult and not jcoup:
        soup_test.tableto_csv(*soup_test.data_to_grid_Hb(compound_num, atom_index, float_cspec, ctype, float_hspec),filepath)
    elif not float_cspec:
        soup_test.tableto_csv(*soup_test.data_to_grid_Ca(compound_num, atom_index, float_hspec, hmult, jcoup),filepath)
    elif not ctype:
        soup_test.tableto_csv(*soup_test.data_to_grid_Cb(compound_num, atom_index, float_cspec, float_hspec, hmult, jcoup),filepath)

