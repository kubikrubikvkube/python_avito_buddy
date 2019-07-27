import uuid

from bson import ObjectId

from locations import LocationManager
from mongodb import MongoDB

if __name__ == '__main__':
    location_name = "MOSCOW"
    location = LocationManager().get_location(location_name)
    collection = MongoDB(location.detailedCollectionName).collection
    print(f"Documents without UUID before population {collection.find({'uuid': {'$exists': False}}).count()} ")

    for document in collection.find({"uuid": {"$exists": False}}):
        doc_id = str(document['_id'])
        doc_uuid = str(uuid.uuid4())
        collection.update_one({"_id": ObjectId(doc_id)}, {"$set": {"uuid": doc_uuid}})

    print(f"Documents without UUID after population {collection.find({'uuid': {'$exists': False}}).count()} ")
