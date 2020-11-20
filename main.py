# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 11:41:54 2020

@author: maras
"""
# Use this file as a personal testing group to make sure all the functions
# work (return what you expect) and work as part of the overall data pipeline

from pathlib import Path
from nmr_html_parser import souping, runner


def main():

    # Function which takes as an input and HTML file and writes output .csv file
    inp_file = Path("tests/inputs/test_mult_ai_1.html")

    # test full thing
    # runner.parse(inp_file, "html_parse_output.csv")

    # testing individual parts
    soup = souping.inputs(inp_file)
    headers = souping.soup_id_headers(soup)
    rows = souping.soup_id_rows(soup)
    comps = souping.soup_comp_id(soup)

    # Used stored results from previous functions calls to run
    compound_num = souping.compound_number(comps, headers)
    print(compound_num)
    columns = souping.get_columns(rows, headers)

    atom_index_list,  atom_ignore_col_list = souping.get_atom_index(columns, headers)
    residues_list, residue_ignore_col_list = souping.get_residues(columns, headers)
    # residues, residue_col_index = souping.get_residues(columns, headers)

    print(atom_index_list, residues_list, atom_ignore_col_list, residue_ignore_col_list)

    two_d_NMR_col_index = souping.is_2D_NMR(headers)
    ignore_cols = residue_ignore_col_list + atom_ignore_col_list + two_d_NMR_col_index
    print(ignore_cols)

    souping.fix_multidata(columns, ignore_cols)
    float_hspec, float_cspec, hmult, jcoup, ctype = souping.column_id_cleaner_list(
        columns, ignore_cols
    )
    # print columns as csv like grid
    # for i in range(len(columns[0])):
    #     for c in columns:
    #         print(c[i], end="\t")
    #     print("")

# TODO: If multi_index, need to specify which compound numbers for which atom_index/residues
        # Ex. if 3 atom_indices, then input would need to be
        # HOW many atom_indices? 3
        # What compound numbers preceeds each multiple atom_index?(atom_index:compound_number) 2:1,3,2

    if len(atom_index_list) > 1 and residues_list:
        for atom_index,residues in atom_index_list, residues_list:
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
    else:
        atom_index = [item for items in atom_index_list for item in items]
        residues = [item for items in residues_list for item in items]
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
