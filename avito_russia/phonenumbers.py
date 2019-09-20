class PhoneNumberValidator:

    @staticmethod
    def is_valid(phonenumber: str) -> bool:
        if phonenumber and phonenumber.startswith("7") and len(phonenumber) == 11:
            return True
        else:
            return False
