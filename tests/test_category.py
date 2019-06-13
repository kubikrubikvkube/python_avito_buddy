from unittest import TestCase

from Category import Category


class TestCategory(TestCase):
    """Проверяет что в enum Category есть все необходимые значения"""

    def test___init__(self):
        for category in Category:
            if category.name == 'ALL':
                assert not category.category_id
                assert not category.category_name
            else:
                assert category.category_id
                assert category.category_name
