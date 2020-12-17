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
    inp_file = Path("tests/inputs_elsevier/test_elsevier_num_headers.html") # TODO: had to remove extra tags within <td>

    # testing individual parts
    soup = souping.inputs(inp_file)# TODO: **Might not need to change**

    headers = souping.elsevier_headers(soup)# TODO: Working for no primary headers!; with primary headers, positon included
                                                   # Will have to likely change comp_num or swap position to main headers

    rows = souping.elsevier_rows(soup)# TODO: Have to add logic for multi data <td>
    comps = souping.elsevier_comp_headers(soup)# TODO:
    print(headers)
    #headers.pop(0)
    print(comps)
    # Used stored results from previous functions calls to run
    compound_num = souping.compound_number(comps, headers)# TODO:
    print(compound_num)

    columns = souping.get_columns(rows, headers)# TODO: Get format of inputs_elsevier into input arguments for get_columns
    atom_index, atom_col_index = souping.get_atom_index(columns, headers)
    residues, residue_col_index = souping.get_residues(columns, headers)

    # Remove atom_index_like from get_atom index
    if atom_index is None and souping.atom_index_like(columns[0]):
        headers = ["no."] + headers
        columns = souping.get_columns(rows, headers)
        atom_col_index, atom_index = 0, columns[0]


    two_d_NMR_col_index = souping.is_2_d_nmr(headers)
    ignore_cols = [atom_col_index] + two_d_NMR_col_index
    if residue_col_index is not None:
        ignore_cols.append(residue_col_index)

    souping.fix_multidata(columns, ignore_cols)
    float_hspec, float_cspec, hmult, jcoup, ctype = souping.column_id_cleaner_list(
        columns, ignore_cols
    )
    print(atom_index)
    print(columns)
    souping.tableto_csv(
        *souping.data_to_grid(
            compound_num,
            atom_index,
            resi=residues,
            cspec=float_cspec,
            hspec=float_hspec,
            hmult=hmult,
            hcoup=jcoup,
        ),
        filename="html_parse_output_elsevier.csv"
    )

# Best practice to use this for scripts
if __name__ == "__main__":
    main()
