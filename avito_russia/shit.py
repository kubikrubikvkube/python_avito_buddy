import csv
import logging

from bson import ObjectId
from console_progressbar import ProgressBar
from geopy.distance import geodesic
from pymongo.collection import Collection

from avito_russia import NamesDatabase
from items import DetailedItem
from locations import LocationManager
from mongodb import MongoDB

if __name__ == '__main__':
    location_name = "EKATERINBURG"
    location = LocationManager().get_location(location_name)
    collection = MongoDB(location.detailedCollectionName).collection

    valid = []
    valid_phonenumbers = []
    main_address = (56.832265, 60.571037)
    for document in collection.find({"$text": {"$search": "шиномонтаж"}}):
        result = geodesic((document['coords']['lat'],document['coords']['lng']), main_address).meters
        if result < 1500 and valid_phonenumbers.count(document['phonenumber']) is 0:
            valid.append(document)
            valid_phonenumbers.append(document['phonenumber'])

    with open('tires.csv', 'w', newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["name","phonenumber","title","url"])
        for document in valid:
            writer.writerow([document['seller']['name'],document['phonenumber'],document['title'],document['sharing']['url']])