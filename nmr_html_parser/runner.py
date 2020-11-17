import os
from pathlib import Path
from nmr_html_parser import souping


def parse(path, filepath):
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
    atom_index, atom_col_index = souping.get_atom_index(columns, headers)
    residues, residue_col_index = souping.get_residues(columns, headers)
    ignore_cols = [atom_col_index]
    if residue_col_index is not None:
        ignore_cols.append(residue_col_index)
    float_hspec, float_cspec, hmult, jcoup, ctype = souping.column_id_cleaner_list(
        columns, ignore_cols
    )
    # float_hspec = souping.column2dlist_string_to_float(hspec)
    # float_cspec = souping.column2dlist_string_to_float(cspec)

    # if not float_cspec or not float_hspec:
    #     columns = souping.column2dlist_string_to_float(columns)
    #     float_cspec, float_hspec = souping.get_float_avg(columns)

    # if float_cspec and float_hspec:
    souping.tableto_csv(
        *souping.data_to_grid(
            compound_num,
            atom_index,
            resi=residues,
            cspec=float_cspec,
            ctype=ctype,
            hspec=float_hspec,
            hmult=hmult,
            hcoup=jcoup,
        ),
        filename=filepath
    )
