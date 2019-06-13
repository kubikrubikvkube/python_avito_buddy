from unittest import TestCase

from Location import Location


class TestLocation(TestCase):
    """Проверяет что в enum Location есть все необходимые значения"""

    def test___init__(self):
        for location in Location:
            if location.name == 'ALL':
                assert not location.location_id
                assert not location.location_name
            else:
                assert location.location_id
                assert location.location_name
