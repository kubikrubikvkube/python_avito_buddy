import json
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Location:
    id: int
    detailedCollectionName: str
    recentCollectionName: str


class LocationManager:
    locations_list: Dict

    def __init__(self):
        with open("locations_settings.json", mode="r", encoding="UTF-8") as locations_json:
            self.locations_list = json.loads(locations_json.read(), encoding="UTF-8")

    def get_location(self, location_name: str) -> Location:
        resolved_location: Optional[dict] = self.locations_list.get(location_name)
        if resolved_location is None:
            raise AttributeError("This location is not present in locations_settings.json. Check location name.")

        return Location(resolved_location['id'],
                        resolved_location['detailedCollectionName'],
                        resolved_location['recentCollectionName'])
