import json
import re
from collections import namedtuple
from dataclasses import dataclass
from typing import Dict, List

from geopy import distance
from geopy.distance import geodesic

from avito.Metro import Metro
from avito.SpbMetro import SpbMetro


@dataclass
class Item:
    dictionary: Dict

    def __repr__(self) -> str:
        return json.dumps(self.dictionary, ensure_ascii=False)

    @property
    def value(self) -> Dict:
        value = None
        if self.dictionary['type'] == 'item' or self.dictionary['type'] == 'xlItem':
            value = self.dictionary['value']
        elif self.dictionary['type'] == 'vip':
            value = self.dictionary['value']['list'][0]['value']
        assert value is not None
        return value

    @property
    def natural_id(self) -> int:
        return self.value['id']

    @property
    def category(self) -> Dict:
        return self.value['category']

    @property
    def location(self) -> str:
        return self.value['location']

    @property
    def square_meters(self) -> float:
        title = self.value['title']
        strings = title.split(sep=',')
        f = re.search('[0-9.]*[0-9]+', strings[1]).group()
        return float(f)

    @property
    def address(self) -> str:
        return self.value['address']

    @property
    def coords(self) -> dict or None:
        if 'coords' in self.value:
            return self.value['coords']
        return None

    @property
    def closest_metro(self) -> Metro:
        if not hasattr(self, '_closest_metro'):
            ClosestStation = namedtuple('ClosestStation', 'station distance')
            closest = ClosestStation(None, None)
            for station in SpbMetro:
                item_station_distance = distance.distance((self.coords['lat'], self.coords['lng']),
                                                          (station.lat, station.lng)).m
                if (closest.distance is None or item_station_distance < closest.distance):
                    closest = ClosestStation(station, item_station_distance)
            self._closest_metro = closest.station
        return self._closest_metro

    @property
    def closest_metro_distance(self) -> geodesic:
        if not hasattr(self, '_closest_metro_distance'):
            item_lat = self.coords['lat']
            item_lng = self.coords['lng']
            metro_lat = self.closest_metro.lat
            metro_lng = self.closest_metro.lng
            self._closest_metro_distance = distance.distance((item_lat, item_lng), (metro_lat, metro_lng))
        return self._closest_metro_distance

    @property
    def distance_to_city_center(self) -> geodesic:
        if not hasattr(self, '_distance_to_city_centre'):
            item_lat = self.coords['lat']
            item_lng = self.coords['lng']
            metro_lat = SpbMetro.NEVSKIJ_PROSPECT.lat
            metro_lng = SpbMetro.NEVSKIJ_PROSPECT.lng
            self._distance_to_city_centre = distance.distance((item_lat, item_lng), (metro_lat, metro_lng))
        return self._distance_to_city_centre

    @property
    def time(self) -> int:
        return self.value['time']

    @property
    def title(self) -> str:
        return self.value['title']

    @property
    def user_type(self) -> str:
        return self.value['userType']

    @property
    def images(self) -> None:
        return self.value['images']

    @property
    def services(self) -> List[str]:
        return self.value['services']

    @property
    def price(self) -> int:
        return int(re.sub('\D', '', self.value['price']))

    @property
    def uri(self) -> str:
        return self.value['uri']

    @property
    def uri_mweb(self) -> str:
        return self.value['uri_mweb']

    @property
    def is_verified(self) -> bool:
        return self.value['isVerified']

    @property
    def is_favorite(self) -> bool:
        return self.value['isFavorite']
