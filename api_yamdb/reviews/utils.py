import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / 'static/data/category.csv',
          newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    data = []
    for row in spamreader:
        data.append(row)
        print(', '.join(row))
    print(data)
