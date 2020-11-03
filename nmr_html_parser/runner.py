from pathlib import Path
import nmr_html_parser.souping


def parse(fname):
    inp_file = Path(fname)  # This example has no C/CH/CHn in Carbon column
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
    float_cspec = souping.column2dlist_string_to_float(cspec)
    if not float_cspec:
        columns = souping.column2dlist_string_to_float(columns)
        cspec, hspec = souping.get_float_avg(columns)
        float_cspec = cspec
        ctype = souping.blanks_list(float_cspec)
    if not float_hspec:
        columns = souping.column2dlist_string_to_float(columns)
        cspec, hspec = souping.get_float_avg(columns)
        float_hspec = hspec
        hmult, jcoup = souping.blanks_list(
            float_hspec
        )  # might have to make variables separate
    # Turn compound tables into CSV

    return souping.tableto_csv(
        *souping.data_to_grid(
            compound_num, atom_index, float_cspec, ctype, float_hspec, hmult, jcoup
        )
    )

