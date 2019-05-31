import json
import logging
import os
import urllib.parse as urlparse
from datetime import datetime, timedelta
from typing import List

from IPython.core.display import display
from ipywidgets import widgets
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from tqdm._tqdm_notebook import tqdm_notebook

from avito import Database
from avito.Item import Item
from avito.ItemRequest import ItemRequest
from avito.SQLiteDatabase import SQLiteDatabase


class Avito:
    _browser: Chrome
    _key: str
    _database: Database

    def __init__(self, database: Database = None):
        if database:
            self._database = database

    def __del__(self):
        self.database.session.close()

    @property
    def browser(self):
        if not hasattr(self, '_browser'):
            options = Options()
            options.set_headless()
            chromedriver = os.path.abspath(os.path.join(os.path.dirname(__file__), '.', 'chromedriver.exe'))
            self._browser = Chrome(chrome_options=options, executable_path=chromedriver)
            logging.info(f'For RealBrowser {self} set browser {self._browser}')
            self.key = self.__get_key__()
            logging.debug(f'Key {self.key} set for {self} with browser {self._browser}')
        return self._browser

    def get_item_request(self, url: ItemRequest) -> str:
        logging.debug(f'Fetching {url}')
        self.browser.get(url)
        body = self.browser.find_element_by_tag_name("body")
        logging.debug(f'Fetched body {body}')
        assert body is not None and body.text is not None
        return body.text

    def search(self, query=None, location=None, category=None, page=None, last_stamp=None, limit=None,
               params: tuple = None) -> List[Item] or None:
        """Поиск по avito с заданными параметрами"""
        get_request = ItemRequest(key=self.key, query=query, location=location, category=category, page=page,
                                  last_stamp=last_stamp, limit=limit, params=params).to_json()
        logging.debug(f'Get reqest prepared {get_request}')
        response = self.get_item_request(get_request)
        json_response = json.loads(response)
        logging.debug(f'Response received {json_response}')
        if json_response['status'] != 'internal-error':
            items_list = list(map(lambda d: Item(d), json_response['result']['items']))
            logging.debug(f'Fetched {len(items_list)} items')

            def set_natural_id(i: Item):
                i.id = i.natural_id
                logging.debug(f'For {i.id} set natural id {i.natural_id}')

            [set_natural_id(i) for i in items_list]
            return items_list
        else:
            return None

    @property
    def key(self):
        if not hasattr(self, '_key'):
            self.key = self.__get_key__()
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    @property
    def database(self) -> Database:
        if not hasattr(self, '_database'):
            self._database = SQLiteDatabase(persist=False, echo=True)
        return self._database

    @database.setter
    def database(self, database):
        self._database = database

    @database.deleter
    def database(self):
        self.database.__del__()

    def search_whole_month(self, query=None, location=None, category=None, params: tuple = None) -> List[Item]:
        """Поиск по Авито за последний месяц"""
        month_result = []
        if query is None:
            label = widgets.HTML(f"<h3>Ищу всё в категории {category.category_name} за последние 30 дней...<h3>")
        else:
            label = widgets.HTML(f"<h3>Ищу {query} в категории {category.category_name} за последние 30 дней...<h3>")
        display(label)

        with tqdm_notebook(leave=True, unit=' страниц объявлений') as progressbar:
            for day_delta in range(0, 30):
                logging.debug(f'Processing day {day_delta}')
                last_stamp = int((datetime.now() - timedelta(days=day_delta) - timedelta(minutes=5)).timestamp())
                global_last_item_id = None
                for page in range(1, 99):
                    logging.debug(f'Processing page {page}')
                    progressbar.update(1)
                    found_items = self.search(query=query, location=location, category=category, page=page,
                                              last_stamp=last_stamp, limit=99, params=params)

                    if found_items:
                        logging.debug(f'Found {len(found_items)} items')
                        month_result += found_items
                        last_item = found_items[-1]
                        item_id = last_item.natural_id

                        if global_last_item_id == item_id or item_id is None:
                            break
                        else:
                            global_last_item_id = item_id
        logging.debug(f'Search completed {len(month_result)} non-unqie items found in month')
        month_result = self.__filter_by_distinct_ad_keys__(month_result)
        logging.debug(f'{len(month_result)} unqie items found in month')
        logging.info(f"Найдено {len(month_result)} записей")
        return month_result

    @staticmethod
    def __filter_by_distinct_ad_keys__(items_list: List[Item]) -> List[Item]:
        logging.debug(f'Изначальное количество объявлений {len(items_list)}')
        final_list = []
        existing_item_keys = []
        for item in items_list:
            item_id = item.natural_id

            if item_id not in existing_item_keys:
                existing_item_keys.append(item_id)
                final_list.append(item)
        logging.debug(f'Количество уникальных объявлений {len(final_list)}')
        return final_list

    def __get_key__(self) -> str:
        logging.info('Getting the api key started')
        chrome = self.browser
        chrome.get("http://m.avito.ru")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logging.debug(f'Current dir is {current_dir}')
        jquery_js = os.path.join(current_dir, "js/jquery-3.4.1.min.js")
        logging.debug(f'Jquery.js path is {jquery_js}')
        console_logs_js = os.path.join(current_dir, "js/console_logs.js")
        logging.debug(f'Console logs js path is {console_logs_js}')
        chrome.execute_script(open(jquery_js).read())
        chrome.execute_script(open(console_logs_js).read())
        chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        while len(chrome.execute_script("return console.logs")) is 0:
            chrome.implicitly_wait(1)
        available_logs = chrome.execute_script("return console.logs")
        logging.debug(f'Available console logs is {available_logs}')

        key = None
        for url in available_logs:
            if url.startswith('https://m.avito.ru/api/1/main/items?key='):
                parsed = urlparse.urlparse(url)
                key_values = urlparse.parse_qs(parsed.query)['key']
                assert len(key_values) == 1
                key = list.pop(key_values)

        assert key is not None
        logging.debug(f'Key found {key}')
        return key
