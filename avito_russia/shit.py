from avito_russia import NamesDatabase
from locations import LocationManager
from mongodb import MongoDB

if __name__ == '__main__':
    location_name = "SAINT-PETERSBURG"
    location = LocationManager().get_location(location_name)
    detailed_collection = MongoDB(location.detailedCollectionName)

    names_db = NamesDatabase()

    for document in detailed_collection.collection.find():
        if document.get('gender') is None:
            resolved_gender = names_db.resolve_gender(document.get('seller').get('name'))
            id = document.get('id')

    resolved_gender = names_db.resolve_gender(item['seller']['name'])
    if resolved_gender:
        item['gender'] = resolved_gender