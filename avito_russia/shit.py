import logging

from bson import ObjectId
from console_progressbar import ProgressBar
from pymongo.collection import Collection

from avito_russia import NamesDatabase
from items import DetailedItem
from locations import LocationManager
from mongodb import MongoDB

if __name__ == '__main__':
    location_name = "MOSCOW"
    location = LocationManager().get_location(location_name)
    db = MongoDB(location.detailedCollectionName)
    collection: Collection = db.collection
    names_db = NamesDatabase()

    all_documents = collection.count_documents(filter={"phonenumber": {"$exists": False}})
    pb = ProgressBar(total=all_documents, prefix='Here', suffix='Now', decimals=3, length=50, fill='X', zfill='-')
    iterations = 0

    for document in collection.find({"phonenumber": {"$exists": False}}):

        try:
            iterations += 1
            pb.print_progress_bar(iterations)
            _id = document.get('_id')
            # print(_id)
            decoded_phone_number = DetailedItem.decode_phone_number(document)
            if decoded_phone_number:
                document['phonenumber'] = decoded_phone_number
                collection.find_one_and_update({"_id": ObjectId(_id)}, {"$set": {"phonenumber": document.get("phonenumber")}})

        except AttributeError as e:
            pass
            # print(e)
        finally:
            pass
            # print(f"Remaining {all_documents} documents")

    # decoded_phone_number = DetailedItem.decode_phone_number(item)
    # if decoded_phone_number:
    #   item['phonenumber'] = decoded_phone_number
