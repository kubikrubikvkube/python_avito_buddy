import csv
import urllib
from typing import Optional
from urllib.parse import parse_qsl, urlparse

from pymongo.cursor import Cursor

from avito_russia.mongodb import MongoDB


def resolve_price(result) -> Optional[int]:
    price_str = result['price']['value']
    if price_str == 'Цена не указана' or price_str == 'Бесплатно':
        return None
    else:
        return int(price_str.replace(' ', ''))



if __name__ == '__main__':
    mongo_db = MongoDB("ekb_backup")

    # Ищем людей, продающих квартиры стоимостью более чем значение FLAT_SALE_PRICE
    FLAT_SALE_PRICE = 5000000
    cursor: Cursor = mongo_db.collection.find({'parameters.flat.0.description': 'Квартиры', 'userType': 'private'})
    valid_results = []
    print("Processing flat sellers")
    for result in cursor:
        price_int = resolve_price(result)
        if price_int and price_int > FLAT_SALE_PRICE:
            valid_results.append(result)

    # Продающие свой бизнес за стоимость более
    BUSINESS_SALE_PRICE = 300000
    cursor: Cursor = mongo_db.collection.find({"parameters.flat.0.description": "Готовый бизнес"})
    print("Processing business sellers")
    for result in cursor:
        price_int = resolve_price(result)
        if price_int and price_int > BUSINESS_SALE_PRICE:
            valid_results.append(result)
    CAR_SALE_PRICE = 3000000
    # Продающие автомобиль стоимостью более CAR_SALE_PRICE
    cursor: Cursor = mongo_db.collection.find(
        {"parameters.flat.0.description": "Автомобили", "parameters.flat.1.description": "С пробегом"})
    print("Processing car sellers")
    for result in cursor:
        price_int = resolve_price(result)
        if price_int and price_int > CAR_SALE_PRICE:
            valid_results.append(result)

    with open('ekb_rich.csv', mode='w', newline='', encoding='utf-8') as phonenumbers_file:
        writer = csv.writer(phonenumbers_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["external_id", "phone"])
        for valid_result in valid_results:
            try:
                raw_phone = valid_result['contacts']['list'][0]['value']['uri']
                r = urllib.parse.unquote_plus(raw_phone)
                q2 = parse_qsl(urlparse(r).query)
                phone_number = str.strip(q2[0][1])
                external_id = valid_result['_id']
                row = [external_id, phone_number]
                print(row)
                writer.writerow(row)
            except IndexError:
                pass

    print(f"Valid results: {len(valid_results)}")
