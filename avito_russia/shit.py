import urllib
import uuid
from urllib.parse import parse_qsl, urlparse

from bson import ObjectId

from locations import LocationManager
from mongodb import MongoDB

if __name__ == '__main__':
    location_name = "MOSCOW"
    location = LocationManager().get_location(location_name)
    collection = MongoDB(location.detailedCollectionName).collection
    not_exists_filter = {
        "$and": [
            {'seller.userKey': {'$exists': False}},
            {'userType': {"$eq": "private"}},
            {'seller.link': {"$exists": True}}
        ]
    }
    print(f"Documents without userKey before population {collection.count_documents(not_exists_filter)} ")

    for document in collection.find(not_exists_filter):
        if document['userType'] == 'private' and document['seller']['link']:
            r = urllib.parse.unquote_plus(document['seller']['link'])
            q2 = parse_qsl(urlparse(r).query)
            userKey = str(q2[0][1]).strip()
            doc_id = str(document["_id"])
            collection.update_one({"_id": ObjectId(doc_id)}, {"$set": {"seller.userKey": userKey}})
            print(f"Updated {doc_id}")

    print(f"Documents without userKey after population {collection.count_documents(not_exists_filter)} ")
