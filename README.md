# nmr html parser

html parser extracts NMR html tables from Journal of Natural Products.
Gathering NMR table types/number of compounds, parsing the rows/columns and separating multiple data types from a single cell.

## Installation

(TBD)

## Usage

(TBD)

### Goal

To produce an output JSON file with all the data for each compound in the data table.
A recommended output type might look something like this (_don't worry about the extra meta-data fields right now_):

```json
{
  "name": "Compound Name",
  "c_nmr": {
    "solvent": "CDCl3",
    "temperature": 20,
    "reference": "residual_solvent",
    "frequency": "151 MHz",
    "spectrum": [
      {
        "shift": 168.9,
        "atom_index": "1",
        "carbon_type": "CH2"
      }
      // ... and repeat for every row for a given compound
    ]
  },
  "h_nmr": {
    "solvent": "CDCl3",
    "temperature": 20, // Standard room temp, required in NP-MRD
    "reference": "residual_solvent",
    "frequency": "600 MHz", // Could split or omit unit if implicit
    "spectrum": [
      {
        "atom_index": "1",
        "shift": 4.44,
        "integration": 1,
        "multiplicity": "dd",
        "coupling_constants": [9.3, 9.3]
      }
      //...  And so on
    ]
  }
}
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
