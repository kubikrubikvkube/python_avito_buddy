import urllib
from urllib.parse import parse_qsl, urlparse

from pymongo.cursor import Cursor

from avito_russia.mongodb import MongoDB

if __name__ == '__main__':
    mongo_db = MongoDB("ekb")
    cursor: Cursor = mongo_db.collection.find({'parameters.flat.0.description': 'Квартиры', 'userType': 'private'})
    valid_results = []
    for result in cursor:
        price_str = result['price']['value']
        if price_str == 'Цена не указана':
            pass
        else:
            price_int = int(price_str.replace(' ', ''))
            if price_int > 5000000:
                valid_results.append(result)
    for valid_result in valid_results:
        title = valid_result['title']
        raw_phone = valid_result['contacts']['list'][0]['value']['uri']
        r = urllib.parse.unquote_plus(raw_phone)
        q2 = parse_qsl(urlparse(r).query)
        name = valid_result['seller']['name']
        phone_number = str.strip(q2[0][1])
        price = valid_result['price']['value']
        print((title, price, name, phone_number))

    print(f"Valid results: {len(valid_results)}")
