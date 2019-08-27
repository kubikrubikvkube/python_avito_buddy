import logging
import urllib
from enum import Enum
from json.decoder import JSONObject
from typing import Optional, Type
from urllib.parse import parse_qsl, urlparse

from scrapy import Item, Field
from scrapy.exceptions import NotSupported


class DetailedItemType(Enum):
    ITEM = "item",
    XLITEM = "xlItem",
    VIP = "vip"

    @classmethod
    def resolve_item_type(cls, document: JSONObject) -> Type[Enum]:
        if document['type'] == 'item':
            return cls['ITEM']
        elif document['type'] == 'xlItem':
            return cls['XLITEM']
        elif document['type'] == 'vip':
            return cls['VIP']
        else:
            raise NotSupported()

class DetailedItem(Item):
    id = Field()
    categoryId = Field()
    locationId = Field()
    metroId = Field()
    metroType = Field()
    sharing = Field()
    coords = Field()
    address = Field()
    title = Field()
    userType = Field()
    time = Field()
    description = Field()
    parameters = Field()
    images = Field()
    price = Field()
    seller = Field()
    shopId = Field()
    shopType = Field()
    stats = Field()
    contacts = Field()
    needToCheckCreditInfo = Field()
    firebaseParams = Field()
    adjustParams = Field()
    deliveryC2C = Field()
    video = Field()
    titleGenerated = Field()
    autodeal = Field()
    directionId = Field()
    autoteka = Field()
    anonymousNumber = Field()
    shortTermRent = Field()
    needToCheckModelSpecs = Field()
    districtId = Field()
    autotekaTeaser = Field()
    disclaimer = Field()
    gender = Field()
    phonenumber = Field()
    location = Field()
    uuid = Field()
    autoCatalogAction = Field()
    geoReferences = Field()

    @staticmethod
    def resolve_item_value(document: JSONObject) -> JSONObject:
        """Resolves item value"""
        assert document is not None
        if document['type'] == 'item' or document['type'] == 'xlItem':
            return document['value']
        elif document['type'] == 'vip':
            return document['value']['list'][0]['value']
        else:
            raise NotSupported()

    @staticmethod
    def resolve_item_id(document: JSONObject) -> int:
        """Resolves item avito id"""
        return DetailedItem.resolve_item_value(document)['id']

    @staticmethod
    def decode_phone_number(document: JSONObject) -> Optional[str]:
        """Returns decoded phonenumber - it's format is 79118541231"""
        result = None

        try:
            if document['contacts']['list'][0]['type'] == "phone":
                raw_phone = document['contacts']['list'][0]['value']['uri']
                r = urllib.parse.unquote_plus(raw_phone)
                q2 = parse_qsl(urlparse(r).query)
                result = str(q2[0][1]).strip()
        except IndexError as ie:
            logging.debug(ie)
        finally:
            return result