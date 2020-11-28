import csv, json

# Filepaths
csvFilePath = "table_example.csv"
jsonFilePath = "happy.json"


# CSV reformatting to structure for JSON
with open(csvFilePath, encoding="UTF-8") as csvFile:
    csvReader = csv.DictReader(csvFile)
    new_dict = {}
    for d in list(csvReader):
        for k, v in d.items():
            if k in new_dict:
                new_dict[k] = new_dict[k] + [v]
            else:
                new_dict[k] = [v]
    #print(new_dict)  # New dictionary created

    '''atom_index': ['2', '3', '4', '4a', '5', '6', '7', '8', '8a', '9', '10', '11', '', '12', '13', '14', '15', '2′',
                   '3′', '4′', '4a′', '5′', '6′', '7′', '8′', '8a′', '9′', '10′', '11′', '', '12′', '13′', '14′',
                   '15′',
                   'OCH3-5'],
    '1_cspec': ['118.6', '117.5', '125.0', '108.0', '144.0', '113.5', '149.1', '128.1', '141.7', '143.7', '105.0',
                '69.9', '', '120.4', '137.8', '17.9', '25.7', '161.0', '112.6', '139.0', '107.1', '148.4', '114.2',
                '158.1', '94.6', '152.5', '145.0', '104.9', '72.6', '', '82.8', '82.5', '22.8', '29.1', '60.9'],
    '1_hspec': ['', '5.73', '7.22', '', '', '', '', '', '', '7.51', '6.86', '4.53', '', '5.3', '', '1.54', '1.59',
                '',
                '6.1', '8.06', '', '', '', '', '7.15', '', '7.59', '7.1', '4.86', '', '4.44', '', '1.65', '1.55',
                '4.04'],
    '1_multi': ['', 'd', 'd', '', '', '', '', '', '', 'd', 'd', 'd', '', 't', '', 's', 's', '', 'd', 'd', '', '',
                '', '',
                'brs', '', 'd', 'dd', 'd', '', 't', '', 's', 's', 's'],
    '1_coupling': ['', '9.9', '9.9', '', '', '', '', '', '', '2.2', '2.2', '7.0', '', '7.0', '', '', '', '', '9.8',
                   '9.8', '', '', '', '', '', '', '2.4', '2.4, 1.0', '6.4', '', '6.4', '', '', '', ''],
    '2_cspec': ['117.6', '117.0', '125.4', '108.0', '144.2', '113.3', '149.6', '128.2', '142.0', '143.8', '104.9',
                '70.2', '', '120.5', '138.5', '18.1', '25.8', '160.9', '113.2', '138.9', '107.3', '148.1', '114.0',
                '158.1', '95.0', '152.6', '145.3', '104.6', '71.3', '', '81.1', '82.0', '22.8', '27.8', '60.9'],
    '2_hspec': ['', '5.67', '7.24', '', '', '', '', '', '', '7.52', '6.87', '4.71', '4.73', '5.6', '', '1.69',
                '1.75',
                '', '6.2', '8.12', '', '', '', '', '7.2', '', '7.6', '6.95', '4.57', '4.54', '4.79', '', '1.35',
                '1.71',
                '4.05'],
    '2_multi': ['', 'd', 'd', '', '', '', '', '', '', 'd', 'd', 'dd', 'dd', 't', '', 's', 's', '', 'd', 'd', '', '',
                '',
                '', 'brs', '', 'd', 'dd', 'dd', 'dd', 'dd', '', 's', 's', 's'],
    '2_coupling': ['', '9.9', '9.9', '', '', '', '', '', '', '2.1', '2.1', '11.3, 7.0', '11.3, 7.0', '7.0', '', '',
                   '',
                   '', '9.8', '9.8', '', '', '', '', '', '', '2.4', '2.4, 0.9', '10.2, 6.4', '10.2, 5.4',
                   '6.4, 5.4', '',
                   '', '', '']}'''

    '''"spectrum": [
    {
      "shift": 4.76,
      "atom_index": 2,
      "multiplicity": "d",
      "coupling": [
        9.8
      ]
    },'''


    # Split up the data for each compound
    # Since no multi-ai, same residues and atom index for each compound


    def dictionary_parser(num_comps):
        comps_shift_data = {}
        for i in range(1,num_comps + 1):
            possible_variables = [
                str(i) + "_cspec",
                str(i) + "_hspec",
                str(i) + "_multi",
                str(i) + "_coupling"]

            found_variables = {key: val for key, val in new_dict.items() if key in possible_variables and bool(new_dict.get(k))}
            comps_shift_data["compound_"+str(i)] = found_variables
        return comps_shift_data


    shift_comps = dictionary_parser(2)
    print(shift_comps)


    # Structured format for JSON output (list of dictionaries)
    data = [
        {
            "name": "Compound 1",
            "smiles": None,
            "c_nmr": {
                "solvent": None,
                "temperature": None,
                "reference": None,
                "frequency": None,
                "spectrum": [
                    {"shift": 118.6,
                     "atom_index": 2},
                    {"shift": 117.5,
                     "atom_index": 3}
                ]
            },
            "h_nmr": {
                "solvent": None,
                "temperature": None,
                "reference": None,
                "frequency": None,
                "spectrum": [
                    {
                        "shift": 4.76,
                        "atom_index": 2,
                        "multiplicity": "d",
                        "coupling": [9.8]
                    },
                    {
                        "shift": 5.73,
                        "atom_index": 3,
                        "multiplicity": "d",
                        "coupling": [9.9]
                    }
                ]
            }
        },
        {"name": "Compound 2",
         "smiles": None,
         "c_nmr": {
             "solvent": None,
             "temperature": None,
             "reference": None,
             "frequency": None,
             "spectrum": [
                 {"shift": 117.6,
                  "atom_index": 2},
                 {"shift": 117.0,
                  "atom_index": 3}
             ]
         },
         "h_nmr": {
             "solvent": None,
             "temperature": None,
             "reference": None,
             "frequency": None,
             "spectrum": [
                 {
                     "shift": 5.67,
                     "atom_index": 3,
                     "multiplicity": "d",
                     "coupling": [9.9]
                 }
             ]
         }
         }
    ]
    with open("table_test_output.json", "w") as f:
        # json.dump(data, f)
        # nicer output
        f.write(json.dumps(data, indent=2))
