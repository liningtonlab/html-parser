# html parser

html parser extracts html tables from Journal of Natural Products. Gathering NMR table types/number of compounds, parsing the rows/columns and separating multiple data types from a single cell.

## Installation

(TBD)

## Usage

```python
from html_parser import souping

a_variable = souping.inputs(r'C:\Users\name\html_table_file.html') # Returns soup(html source code) from file
souping.soup_id_headers(a_variable) # Returns column headers
souping.soup_comp_id(a_variable) # Returns compounds id/number secondary headers
souping.soup_id_rows(a_variable) # Returns list of all the rows in 2D list
'
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)