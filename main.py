# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 11:41:54 2020

@author: maras
"""
# Use this file as a personal testing group to make sure all the functions
# work (return what you expect) and work as part of the overall data pipeline

from pathlib import Path
from nmr_html_parser import souping

def main():

    # Function which takes as an input and HTML file and writes output .csv file
    inp_file = Path("tests/inputs/test_multi_data_dash_2.html")

    # test full thing
    # runner.parse(inp_file, "html_parse_output.csv")

    # testing individual parts
    soup = souping.inputs(inp_file)
    headers = souping.soup_id_headers(soup)
    rows = souping.soup_id_rows(soup)
    comps = souping.soup_comp_id(soup)

    # Used stored results from previous functions calls to run
    compound_num = souping.compound_number(comps, headers)

    columns = souping.get_columns(rows, headers)
    atom_index, atom_col_index = souping.get_atom_index(columns, headers)
    residues, residue_col_index = souping.get_residues(columns, headers)

    # Remove atom_index_like from get_atom index
    if atom_index is None and souping.atom_index_like(columns[0]):
        atom_col_index, atom_index = 0, columns[0]
        headers = ["no."] + headers
        columns = souping.get_columns(rows, headers)


    two_d_NMR_col_index = souping.is_2_d_nmr(headers)
    ignore_cols = [atom_col_index] + two_d_NMR_col_index
    if residue_col_index is not None:
        ignore_cols.append(residue_col_index)

    souping.fix_multidata(columns, ignore_cols)
    float_hspec, float_cspec, hmult, jcoup, ctype = souping.column_id_cleaner_list(
        columns, ignore_cols
    )

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
        filename="html_parse_output.csv"
    )

    # print(headers)
    # print(comps)
    # print(compound_num)
    # print(columns)
    # print(residues)
    # print(atom_index, float_hspec, float_cspec, hmult, jcoup, ctype)


# Best practice to use this for scripts
if __name__ == "__main__":
    main()
