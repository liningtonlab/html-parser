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
    inp_file = Path("tests/inputs/test_error_characters_ab_3.html")

    # test full thing
    #runner.parse(inp_file, "html_parse_output.csv")

    # testing individual parts
    soup = souping.inputs(inp_file)
    headers = souping.soup_id_headers(soup)
    rows = souping.soup_id_rows(soup)
    comps = souping.soup_comp_id(soup)

    # Used stored results from previous functions calls to run
    compound_num = souping.compound_number(comps, headers)
    columns = souping.get_columns(rows, headers)
    atom_index = souping.get_atom_index(columns, headers)
    hspec, cspec, hmult, jcoup, ctype = souping.column_id_cleaner_list(columns)
    float_hspec = souping.column2dlist_string_to_float(hspec)
    float_cspec = souping.column2dlist_string_to_float(cspec)
    residues = souping.get_residues(columns, headers)

    if not float_cspec or not float_hspec:
        columns = souping.column2dlist_string_to_float(columns)
        float_cspec, float_hspec = souping.get_float_avg(columns)

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
        filename="html_parse_output.csv"
    )

    # # print(headers)
    # # print(comps)
    # # print(compound_num)
    # # print(columns)
    # # print(residues)
    # # print(atom_index, float_hspec, float_cspec, hmult, jcoup, ctype)


# Best practice to use this for scripts
if __name__ == "__main__":
    main()
