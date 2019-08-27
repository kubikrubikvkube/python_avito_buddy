from locations import LocationManager
from mongodb import MongoDB
from phonenumbers import PhoneNumberValidator

if __name__ == '__main__':
    location_name = "MOSCOW"
    location = LocationManager().get_location(location_name)
    collection = MongoDB(location.detailedCollectionName).collection
    filter = {
        "$and": [
            {
                "contacts.list.0.type": "messenger"
            },
            {
                "phonenumber": {
                    "$exists": True
                }
            }
        ]
    }
    counter = 0
    #print(f"Need to be processed: {collection.count_documents(filter)}")

    for item in collection.find(filter, no_cursor_timeout=True,batch_size=100):
        phonenumber = item['phonenumber']
        if item['uuid'] and not PhoneNumberValidator.is_valid(phonenumber):
            print(f"{phonenumber}/{counter}")
            uuid = item['uuid']
            collection.update_one({"uuid": uuid}, {"$unset": {"phonenumber": ""}})
            counter += 1