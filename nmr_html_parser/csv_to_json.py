import csv,json


# Filepaths
csvFilePath = "tests/outputs/test_12.csv"
jsonFilePath = "happy.json"


with open(csvFilePath) as csvFile:
  csvReader = csv.DictReader(csvFile)
  new_dict = {}
  for d in list(csvReader):
    for k, v in d.items():
      if k in new_dict:
        new_dict[k] = new_dict[k] + [v]
      else:
        new_dict[k] = [v]
  print(new_dict)