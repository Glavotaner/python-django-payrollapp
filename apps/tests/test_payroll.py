from typing import List, TYPE_CHECKING

from django.test import TestCase

if TYPE_CHECKING:
    from ..employee_data_app.employee_app.models import Employee
    from ..payroll_app.models import Labour

from apps.third_parties_app.models import City, Bank
from apps.calculation_data_app.models import ContributionsModel
from apps.tests import setUp, load_fixtures
from apps.employee_data_app.employee_app.models import Employee
from apps.payroll_app.models import Labour
from apps.calculation_data_app.models import HourFund
from datetime import date
from apps.employee_data_app.employment_app.models import Contract, Position, ContractType


class TestPayroll(TestCase):
    fixtures = load_fixtures.load_fixtures()

    def setUp(self) -> None:
        setUp._set_up()

        HourFund.objects.create(
            year=2021,
            month=3,
            total_hours=168
        ).save()

    def test_eligible(self):
        ctr1: Contract = Contract.objects.create(
            contract_type=ContractType.objects.get(pk=1),
            position=Position.objects.get(pk=1),
            multiplier=1,
            start_date=date(2021, 3, 20),
            end_date=date(2021, 3, 28)
        )
        ctr2: Contract = Contract.objects.create(
            contract_type=ContractType.objects.get(pk=1),
            position=Position.objects.get(pk=1),
            multiplier=1,
            start_date=date(2021, 3, 20),
            end_date=date(2021, 4, 28)
        )
        ctr3: Contract = Contract.objects.create(
            contract_type=ContractType.objects.get(pk=1),
            position=Position.objects.get(pk=1),
            multiplier=1,
            start_date=date(2021, 3, 20)
        )
        ctr4: Contract = Contract.objects.create(
            contract_type=ContractType.objects.get(pk=1),
            position=Position.objects.get(pk=1),
            multiplier=1,
            start_date=date(2021, 4, 20),
            end_date=date(2021, 4, 28)
        )

        Employee.objects.create(
            oib="38263212119",
            first_name="Marin", last_name="Glavaš",
            date_of_birth=date(1997, 3, 16),
            disability="N",
            hrvi=0,
            street_name="Dinka Šimunovića", street_number="10", city=City.objects.get(pk=1),
            iban="HR64322456845613",
            first_employment=True,
            first_employment_with_company=True,
            employee_bank=Bank.objects.get(pk=1),
            contributions_model=ContributionsModel.objects.get(pk=1),
            signed_contract=ctr1
        ).save()

        Employee.objects.create(
            oib="38263212419",
            first_name="Marin", last_name="Glavaš",
            date_of_birth=date(1997, 3, 16),
            disability="N",
            hrvi=0,
            street_name="Dinka Šimunovića", street_number="10", city=City.objects.get(pk=1),
            iban="HR64331456845613",
            first_employment=True,
            first_employment_with_company=True,
            employee_bank=Bank.objects.get(pk=1),
            contributions_model=ContributionsModel.objects.get(pk=1),
            signed_contract=ctr2
        ).save()

        Employee.objects.create(
            oib="38253212119",
            first_name="Marin", last_name="Glavaš",
            date_of_birth=date(1997, 3, 16),
            disability="N",
            hrvi=0,
            street_name="Dinka Šimunovića", street_number="10", city=City.objects.get(pk=1),
            iban="HR64321456445613",
            first_employment=True,
            first_employment_with_company=True,
            employee_bank=Bank.objects.get(pk=1),
            contributions_model=ContributionsModel.objects.get(pk=1),
            signed_contract=ctr3
        ).save()

        Employee.objects.create(
            oib="37263212119",
            first_name="Marin", last_name="Glavaš",
            date_of_birth=date(1997, 3, 16),
            disability="N",
            hrvi=0,
            street_name="Dinka Šimunovića", street_number="10", city=City.objects.get(pk=1),
            iban="HR64321456845623",
            first_employment=True,
            first_employment_with_company=True,
            employee_bank=Bank.objects.get(pk=1),
            contributions_model=ContributionsModel.objects.get(pk=1),
            signed_contract=ctr4
        ).save()

        eligible: List['Employee'] = Employee.get_eligible_employees(2021, 4)

        self.assertEqual(len(eligible), 4)

    def test_labour(self):
        ctr1: Contract = Contract.objects.create(
            contract_type=ContractType.objects.get(pk=1),
            position=Position.objects.get(pk=1),
            multiplier=1,
            start_date=date(2021, 3, 20),
            end_date=date(2021, 3, 28)
        )
        ctr2: Contract = Contract.objects.create(
            contract_type=ContractType.objects.get(pk=1),
            position=Position.objects.get(pk=1),
            multiplier=1,
            start_date=date(2021, 3, 20),
            end_date=date(2021, 4, 28)
        )
        ctr3: Contract = Contract.objects.create(
            contract_type=ContractType.objects.get(pk=1),
            position=Position.objects.get(pk=1),
            multiplier=1,
            start_date=date(2021, 3, 20)
        )
        ctr4: Contract = Contract.objects.create(
            contract_type=ContractType.objects.get(pk=1),
            position=Position.objects.get(pk=1),
            multiplier=1,
            start_date=date(2021, 4, 20),
            end_date=date(2021, 4, 28)
        )

        Employee.objects.create(
            oib="38263212119",
            first_name="Marin", last_name="Glavaš",
            date_of_birth=date(1997, 3, 16),
            disability="N",
            hrvi=0,
            street_name="Dinka Šimunovića", street_number="10", city=City.objects.get(pk=1),
            iban="HR64322456845613",
            first_employment=True,
            first_employment_with_company=True,
            employee_bank=Bank.objects.get(pk=1),
            contributions_model=ContributionsModel.objects.get(pk=1),
            signed_contract=ctr1
        ).save()

        Employee.objects.create(
            oib="38263212419",
            first_name="Marin", last_name="Glavaš",
            date_of_birth=date(1997, 3, 16),
            disability="N",
            hrvi=0,
            street_name="Dinka Šimunovića", street_number="10", city=City.objects.get(pk=1),
            iban="HR64331456845613",
            first_employment=True,
            first_employment_with_company=True,
            employee_bank=Bank.objects.get(pk=1),
            contributions_model=ContributionsModel.objects.get(pk=1),
            signed_contract=ctr2
        ).save()

        Employee.objects.create(
            oib="38253212119",
            first_name="Marin", last_name="Glavaš",
            date_of_birth=date(1997, 3, 16),
            disability="N",
            hrvi=0,
            street_name="Dinka Šimunovića", street_number="10", city=City.objects.get(pk=1),
            iban="HR64321456445613",
            first_employment=True,
            first_employment_with_company=True,
            employee_bank=Bank.objects.get(pk=1),
            contributions_model=ContributionsModel.objects.get(pk=1),
            signed_contract=ctr3
        ).save()

        Employee.objects.create(
            oib="37263212119",
            first_name="Marin", last_name="Glavaš",
            date_of_birth=date(1997, 3, 16),
            disability="N",
            hrvi=0,
            street_name="Dinka Šimunovića", street_number="10", city=City.objects.get(pk=1),
            iban="HR64321456845623",
            first_employment=True,
            first_employment_with_company=True,
            employee_bank=Bank.objects.get(pk=1),
            contributions_model=ContributionsModel.objects.get(pk=1),
            signed_contract=ctr4
        ).save()

        Labour.set_labour(
            2021, 4, 168
        )

        self.assertEqual(len(Labour.objects.all()), 4)
        self.assertEqual(Labour.objects.get(employee=Employee.objects.get(oib='38263212114')).regular_hours, 168)
