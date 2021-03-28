from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.general_services.validators import person_validation, id_validators, general_validation


class TestValidation(TestCase):

    # GENERAL VALIDATION
    def test_valid_phone_number_1(self):
        self.assertIsNone(
            general_validation.validate_phone_number(
                "(+385)/91-104-9786"
            ))

    def test_valid_phone_number_4(self):
        self.assertIsNone(
            general_validation.validate_phone_number(
                "     (+385)/91-104-9786   "
            ))

    def test_valid_phone_number_2(self):
        self.assertIsNone(
            general_validation.validate_phone_number(
                "0911049786"
            ))

    def test_valid_phone_number_3(self):
        self.assertIsNone(
            general_validation.validate_phone_number(
                "+385911049786"
            ))

    def test_invalid_phone_number_text(self):
        self.assertRaisesMessage(ValidationError,
                                 'Phone number must only contain numbers and +, () or / characters',
                                 general_validation.validate_phone_number(
                                     "+a85911049786"
                                 ))

    def test_invalid_phone_number_symbol(self):
        self.assertRaisesMessage(ValidationError,
                                 'Phone number must only contain numbers and +, () or / characters',
                                 general_validation.validate_phone_number(
                                     "+38*911049786"
                                 ))

    # AGE VALIDATION
    def test_valid_dob(self):
        self.assertIsNone(person_validation.validate_age(date(1997, 3, 16)))

    def test_invalid_dob_underage(self):
        self.assertRaises(ValidationError,
                          person_validation.validate_age, date(2005, 1, 1))

    def test_invalid_dob_below_zero(self):
        self.assertRaises(ValidationError,
                          person_validation.validate_age, date(2022, 1, 1))

    # OIB VALIDATION
    def test_valid_oib(self):
        self.assertIsNone(id_validators.validate_pid("38263212113"))

    def test_invalid_oib(self):
        self.assertRaisesMessage(ValidationError, 'PID is invalid, please check your input', id_validators.validate_pid,
                                 "38263212112")

    def test_oib_length_short(self):
        self.assertRaisesMessage(ValidationError, 'PID is of an invalid length', id_validators.validate_pid,
                                 "3826321211")

    def test_oib_length_long(self):
        self.assertRaisesMessage(ValidationError, 'PID is of an invalid length', id_validators.validate_pid,
                                 "382632121123")

    def test_oib_numeric_text(self):
        self.assertRaisesMessage(ValidationError, 'PID is not entirely numeric', id_validators.validate_pid,
                                 "382632121A3")

    def test_oib_numeric_space(self):
        self.assertRaisesMessage(ValidationError, 'PID is not entirely numeric', id_validators.validate_pid,
                                 "382632121 3")

    def test_oib_numeric_symbol(self):
        self.assertRaisesMessage(ValidationError, 'PID is not entirely numeric', id_validators.validate_pid,
                                 "382632121/3")

    def test_oib_trim_whitespace(self):
        self.assertIsNone(id_validators.validate_pid("    38263212113  "))

    # BID VALIDATION
    def test_valid_bid(self):
        self.assertIsNone(id_validators.validate_bid("01130234"))

    def test_bid_trim_whitespace(self):
        self.assertIsNone(id_validators.validate_bid("    01130234  "))

    def test_invalid_bid(self):
        self.assertRaisesMessage(ValidationError,
                                 'Business ID number is invalid',
                                 id_validators.validate_bid, "01130233")

    def test_bid_length_short(self):
        self.assertRaisesMessage(ValidationError,
                                 'Business ID number is of an invalid length',
                                 id_validators.validate_bid, "0113023")

    def test_bid_length_long(self):
        self.assertRaisesMessage(ValidationError,
                                 'Business ID number is of an invalid length',
                                 id_validators.validate_bid, "011302345")

    def test_bid_numeric_text(self):
        self.assertRaisesMessage(ValidationError,
                                 'Businnes ID number is not entirely numeric',
                                 id_validators.validate_bid, "011a0234")

    def test_bid_numeric_space(self):
        self.assertRaisesMessage(ValidationError,
                                 'Businnes ID number is not entirely numeric',
                                 id_validators.validate_bid, "011302 3")

    def test_bid_numeric_symbol(self):
        self.assertRaisesMessage(ValidationError,
                                 'Businnes ID number is not entirely numeric',
                                 id_validators.validate_bid, "011334/3")

    # CITY_ID VALIDATION
    def test_cityid_valid(self):
        self.assertIsNone(id_validators.validate_city_id("03123"))

    def test_cityid_whitespace(self):
        self.assertIsNone(id_validators.validate_city_id("  03123   "))

    def test_invalid_city_id(self):
        self.assertRaisesMessage(ValidationError,
                                 'City ID number is invalid',
                                 id_validators.validate_city_id, "03124")

    def test_city_id_length_short(self):
        self.assertRaisesMessage(ValidationError,
                                 'City ID number is of an invalid length',
                                 id_validators.validate_city_id, "3123")

    def test_city_id_length_long(self):
        self.assertRaisesMessage(ValidationError,
                                 'City ID number is of an invalid length',
                                 id_validators.validate_city_id, "031240")

    def test_city_id_numeric_text(self):
        self.assertRaisesMessage(ValidationError,
                                 'City ID number is not entirely numeric',
                                 id_validators.validate_city_id, "0312a")

    def test_city_id_numeric_space(self):
        self.assertRaisesMessage(ValidationError,
                                 'City ID number is not entirely numeric',
                                 id_validators.validate_city_id, "031 4")

    def test_city_id_numeric_symbol(self):
        self.assertRaisesMessage(ValidationError,
                                 'City ID number is not entirely numeric',
                                 id_validators.validate_city_id, "031/3")
