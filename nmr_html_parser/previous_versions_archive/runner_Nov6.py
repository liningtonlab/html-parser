import os
from pathlib import Path
from nmr_html_parser.previous_versions_archive import souping_Nov6


def parse(path, filepath):
    inp_file = Path(path)
    out_file = Path(filepath)
    if not out_file.parent.exists():
        os.makedirs(out_file.parent)

    soup = souping_Nov6.inputs(inp_file)
    headers = souping_Nov6.soup_id_headers(soup)
    rows = souping_Nov6.soup_id_rows(soup)
    comps = souping_Nov6.soup_comp_id(soup)
    compound_num = souping_Nov6.compound_number(comps, headers)

    # Used stored results from previous function calls to run
    columns = souping_Nov6.get_columns(rows, headers)
    atom_index = columns[0]
    hspec, cspec, hmult, jcoup, ctype = souping_Nov6.column_id_cleaner_list(columns)
    float_hspec = souping_Nov6.column2dlist_string_to_float(hspec)
    float_cspec = souping_Nov6.column2dlist_string_to_float(cspec)

    if float_cspec and float_hspec:
        souping_Nov6.tableto_csv(
            *souping_Nov6.data_to_grid(
                compound_num, atom_index, float_cspec, ctype, float_hspec, hmult, jcoup
            ),
            filepath
        )
    if not float_cspec:
        columns = souping_Nov6.column2dlist_string_to_float(columns)
        cspec, hspec = souping_Nov6.get_float_avg(columns)
        float_cspec = cspec
        ctype = souping_Nov6.blanks_list(float_cspec)
    elif not float_hspec:
        columns = souping_Nov6.column2dlist_string_to_float(columns)
        cspec, hspec = souping_Nov6.get_float_avg(columns)
        if hspec:
            float_hspec = hspec
            hmult, jcoup = souping_Nov6.blanks_list(float_hspec)

    if float_cspec and float_hspec:
        souping_Nov6.tableto_csv(
            *souping_Nov6.data_to_grid(
                compound_num, atom_index, float_cspec, ctype, float_hspec, hmult, jcoup
            ),
            filepath
        )
    elif not float_cspec:
        souping_Nov6.tableto_csv(
            *souping_Nov6.data_to_grid_Ca(
                compound_num, atom_index, float_hspec, hmult, jcoup
            ),
            filepath
        )
    elif not ctype:
        souping_Nov6.tableto_csv(
            *souping_Nov6.data_to_grid_Cb(
                compound_num, float_cspec, atom_index, float_hspec, hmult, jcoup
            ),
            filepath
        )

    elif not float_hspec:
        souping_Nov6.tableto_csv(
            *souping_Nov6.data_to_grid_Ha(compound_num, atom_index, float_cspec, ctype),
            filepath
        )
    elif not hmult:
        souping_Nov6.tableto_csv(
            *souping_Nov6.data_to_grid_Hb(
                compound_num, atom_index, float_cspec, ctype, float_hspec, jcoup
            ),
            filepath
        )
    elif not jcoup:
        souping_Nov6.tableto_csv(
            *souping_Nov6.data_to_grid_Hc(
                compound_num, atom_index, float_cspec, ctype, float_hspec, hmult
            ),
            filepath
        )
    elif float_hspec and not hmult and jcoup:
        souping_Nov6.tableto_csv(
            *souping_Nov6.data_to_grid_Hc(
                compound_num, atom_index, float_cspec, ctype, float_hspec
            ),
            filepath
        )

