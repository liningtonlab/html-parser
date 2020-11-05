import os
from pathlib import Path
from nmr_html_parser import souping


def parse(path, filename):
    inp_file = Path(path)  # This example has no C/CH/CHn in Carbon column
    out_file = Path(filename)
    if not out_file.parent.exists():
        os.makedirs(out_file.parent)
    soup = souping.inputs(inp_file)
    headers = souping.soup_id_headers(soup)
    rows = souping.soup_id_rows(soup)
    comps = souping.soup_comp_id(soup)
    compound_num = souping.compound_number(comps, headers)

    # Used stored results from previous function calls to run
    columns = souping.get_columns(rows, headers)

    atom_index = columns[0]
    hspec, cspec, hmult, jcoup, ctype = souping.column_id_cleaner_list(columns)
    float_hspec = souping.column2dlist_string_to_float(hspec)
    if len(float_hspec) < 1:
        float_hspec = False
    float_cspec = souping.column2dlist_string_to_float(cspec)

    if float_cspec and float_hspec == True:
        souping.tableto_csv(
            *souping.data_to_grid(
                compound_num, atom_index, float_cspec, ctype, float_hspec, hmult, jcoup
            ),
            filename
        )
    if not float_cspec:
        columns = souping.column2dlist_string_to_float(columns)
        cspec, hspec = souping.get_float_avg(columns)
        float_cspec = cspec
        ctype = souping.blanks_list(float_cspec)
    elif not float_hspec:
        columns = souping.column2dlist_string_to_float(columns)
        cspec, hspec = souping.get_float_avg(columns)
        if hspec:
            float_hspec = hspec
            hmult, jcoup = souping.blanks_list(float_hspec)

    if float_cspec and float_hspec == True:
        souping.tableto_csv(
            *souping.data_to_grid(
                compound_num, atom_index, float_cspec, ctype, float_hspec, hmult, jcoup
            ),
            filename
        )
    elif not float_cspec:
        souping.tableto_csv(
            *souping.data_to_grid_Ca(
                compound_num, atom_index, float_hspec, hmult, jcoup
            ),
            filename
        )
    elif not ctype:
        souping.tableto_csv(
            *souping.data_to_grid_Cb(
                compound_num, float_cspec, atom_index, float_hspec, hmult, jcoup
            ),
            filename
        )

    elif float_hspec == False or not float_hspec:
        souping.tableto_csv(
            *souping.data_to_grid_Ha(compound_num, atom_index, float_cspec, ctype),
            filename
        )
    elif not hmult:
        souping.tableto_csv(
            *souping.data_to_grid_Hb(
                compound_num, atom_index, float_cspec, ctype, float_hspec, jcoup
            ),
            filename
        )
    elif not jcoup:
        souping.tableto_csv(
            *souping.data_to_grid_Hc(
                compound_num, atom_index, float_cspec, ctype, float_hspec, hmult
            ),
            filename
        )
    elif float_hspec and not hmult and jcoup:
        souping.tableto_csv(
            *souping.data_to_grid_Hc(
                compound_num, atom_index, float_cspec, ctype, float_hspec
            ),
            filename
        )

