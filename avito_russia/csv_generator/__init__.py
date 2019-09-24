import csv
from typing import List, Dict


class CsvGenerator:
    @staticmethod
    def write_into_csv_file(entries: List[Dict], filename: str, headers: List[str]):
        with open(filename, mode='w', newline='', encoding='utf-8') as phonenumbers_file:
            writer = csv.writer(phonenumbers_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(headers)
            for entry in entries:
                try:
                    print(entry)
                    # writer.writerow(row)
                except IndexError:
                    pass
