from typing import Any

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


class Selenium:
    def __init__(self) -> None:
        opts = Options()
        self.browser = Firefox(options=opts)

    def get(self, url: str) -> Any:
        self.browser.get('https://duckduckgo.com')
