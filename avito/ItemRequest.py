from dataclasses import dataclass
from io import StringIO

from avito import Location, Category


@dataclass
class ItemRequest:
    key: str
    query: str
    location: Location
    category: Category
    page: int
    last_stamp: int
    limit: int
    params: tuple

    def to_json(self):
        buf = StringIO()
        buf.write('https://m.avito.ru/api/9/items?')
        buf.write(f'key={self.key}&')
        if self.query is not None:
            buf.write(f'query={self.query}&')
        if self.location is not None:
            buf.write(f'locationId={self.location.location_id}&')
        if self.category is not None:
            buf.write(f'categoryId={self.category.category_id}&')
        if self.page is not None:
            buf.write(f'page={self.page}&')
        if self.last_stamp is not None:
            buf.write(f'lastStamp={self.last_stamp}&')
        if self.limit is not None:
            buf.write(f'limit={self.limit}&')
        if self.params is not None:
            buf.write(f'params[{self.params[0]}]={self.params[1]}&')
        buf.write('display=list')
        return buf.getvalue()
