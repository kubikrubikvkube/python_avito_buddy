import csv
from typing import List

from items import MongoDetailedItem


class CsvGenerator:
    @staticmethod
    def write_into_csv_file(entries: List[MongoDetailedItem], filename: str, headers: List[str]):
        with open(filename, mode='w', newline='', encoding='utf-8') as phonenumbers_file:
            writer = csv.DictWriter(phonenumbers_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,
                                    fieldnames=headers, extrasaction='ignore')
            writer.writeheader()
            for entry in entries:
                writer.writerow(entry.__dict__)
