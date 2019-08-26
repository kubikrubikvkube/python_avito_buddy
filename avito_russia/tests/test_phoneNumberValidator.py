from unittest import TestCase

from phonenumbers import PhoneNumberValidator


class TestPhoneNumberValidator(TestCase):

    def setUp(self) -> None:
        self.validator = PhoneNumberValidator()

    def test_valid_phonenumber(self):
        result = self.validator.is_valid("79503337612")
        self.assertEqual(result, True, "Valid number should be validated as 'valid'")

    def test_invalid_phonenumber(self):
        result = self.validator.is_valid("1000048999")
        self.assertEqual(result, False, "Invalid number should be validated as 'invalid'")

    def test_null_phonenumber(self):
        result = self.validator.is_valid(None)
        self.assertEqual(result,False,"None number should be validated as 'ivalid'")