from unittest import TestCase

from avito.Metro import SpbMetro


class TestSpbMetro(TestCase):
    """Проверяет что в enum SpbMetro есть все необходимые значения"""

    def test___init__(self):
        for station in SpbMetro:
            assert station.station_name
            assert station.lat
            assert station.lng
