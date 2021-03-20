from datetime import date

from apps.calculation_data_app.models import ContributionsModel
from apps.employee_data_app.employee_app.models import Employee, Dependent
from apps.employee_data_app.employment_app.models import Contract, ContractType, Position
from apps.third_parties_app.models import City, Bank


def _set_up():
    city: City = City.objects.get(joppd="03123")
    bank: Bank = Bank.objects.get(oib="14036333877")
    contributions_model: ContributionsModel = ContributionsModel.objects.get(id=1)

    Contract.objects.create(
        contract_type=ContractType.objects.get(id=2),
        position=Position.objects.get(id=1),
        multiplier=1,
        sign_date=date.today(),
        expiration_date=None
    ).save()

    signed_contract: Contract = Contract.objects.get(id=1)

    Employee.objects.create(
        pid="38263212114",
        first_name="Marin", last_name="Glavaš",
        date_of_birth=date(1997, 3, 16),
        disability="N",
        street_address="Dinka Šimunovića 10", city=city,
        phone_number="123456987",
        iban="HR64321456845613",
        first_employment=True,
        first_employment_with_company=True,
        employee_bank=bank,
        contributions_model=contributions_model,
        signed_contract=signed_contract
    ).save()

    employee = Employee.objects.get(pid="38263212114")

    Dependent.objects.create(pid="38263212111",
                             child_in_line=1,
                             first_name="Stjepan", last_name="Ivić",
                             date_of_birth=date.today(),
                             disability="N",
                             dependent_of=employee).save()

    Dependent.objects.create(pid="38263212112",
                             first_name="Stjepan", last_name="Ivić",
                             date_of_birth=date.today(),
                             disability="N",
                             dependent_of=employee).save()

    Dependent.objects.create(pid="38263212120",
                             child_in_line=2,
                             first_name="Stjepan", last_name="Ivić",
                             date_of_birth=date.today(),
                             disability="D",
                             dependent_of=employee).save()

    Dependent.objects.create(pid="38263212115",
                             child_in_line=3,
                             first_name="Stjepan", last_name="Ivić",
                             date_of_birth=date.today(),
                             disability="D100",
                             dependent_of=employee).save()

    Dependent.objects.create(pid="38263212116",
                             first_name="Stjepan", last_name="Ivić",
                             date_of_birth=date.today(),
                             disability="N",
                             dependent_of=employee).save()

    Dependent.objects.create(pid="38263212117",
                             first_name="Stjepan", last_name="Ivić",
                             date_of_birth=date.today(),
                             disability="D",
                             dependent_of=employee).save()

    Dependent.objects.create(pid="38263212118",
                             first_name="Stjepan", last_name="Ivić",
                             date_of_birth=date.today(),
                             disability="D",
                             dependent_of=employee).save()

    Dependent.objects.create(pid="38263212119",
                             child_in_line=5,
                             first_name="Stjepan", last_name="Ivić",
                             date_of_birth=date.today(),
                             disability="N",
                             dependent_of=employee).save()
