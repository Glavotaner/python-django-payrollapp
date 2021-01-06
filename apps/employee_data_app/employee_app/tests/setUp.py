from datetime import date
from apps.employee_data_app.employment_app.models import Contract, ContractType, Position
from apps.third_parties_app.models import City, Bank
from apps.employee_data_app.employee_app.models import Employee, Dependent
from apps.calculation_data_app.models import ContributionsModality, Deductible
from apps.payroll_app.services.calculations import deductibles_calculation

def _setUp(self):
    
    City.objects.create(
        joppd="03123",
        iban="HR8110010051731212002",
        postal_code="31000",
        city_name="OSIJEK",
        tax_rate=0.13,
        tax_break=0
    )

    city = City.objects.get(joppd="03123")

    Bank.objects.create(
        business_id="3777928",
        oib="87939104217",
        bank_name="HRVATSKA POŠTANSKA BANKA d.d. Zagreb",
        street_address="Jurišićeva 4",
        city=city
    )

    ContributionsModality.objects.create(
        modality_mark="REG",
        pension_fund_min_base=3265,
        pension_fund_gen=0.15,
        pension_fund_ind=0.05,
        health_insurance=0.165
    )

    ContractType.objects.create(
        contract_type="Neodređeno vrijeme"
    )

    contract_type = ContractType.objects.get(id=1)

    Position.objects.create(
        position_name="Developer",
        salary=5600
    )

    position = Position.objects.get(id=1)

    Contract.objects.create(
        contract_type=contract_type,
        position=position,
        multiplier=0.00,
        sign_date=date.today()
    )

    Deductible.objects.create(
        base_deductible=2500,
        personal_deductible_coef=1.6,
        valid_from=date.today()
    )

    bank = Bank.objects.get(oib="87939104217")
    contributions_model = ContributionsModality.objects.get(id=1)
    signed_contract = Contract.objects.get(id=1)

    Employee.objects.create(
        pid="38263212113",
        first_name="Marin", last_name="Glavaš",
        date_of_birth=date(1997, 3, 16),
        disability="N",
        street_address="Dinka Šimunovića 20", city=city,
        phone_number="123456987",
        iban="HR64321456845613",
        first_employment=True,
        first_employment_with_company=True,
        employee_bank=bank,
        contributions_model=contributions_model,
        signed_contract=signed_contract
    )

    self.employee = Employee.objects.get(pid="38263212113")
    
    self.current_deductibles_model = Deductible.objects.latest()
    self.personal_deductible_amount = deductibles_calculation._personal_deductible_amount(self)

    Dependent.objects.create(pid="38263212111",\
                            child=True,\
                            first_name="Stjepan", last_name="Ivić",
                            date_of_birth=date.today(), 
                            disability="N", 
                            dependent_of=self.employee)
    
    Dependent.objects.create(pid="38263212112",\
                            child=False,\
                            first_name="Stjepan", last_name="Ivić",
                            date_of_birth=date.today(), 
                            disability="N", 
                            dependent_of=self.employee)
    
    Dependent.objects.create(pid="38263212114",\
                            child=True,\
                            first_name="Stjepan", last_name="Ivić",
                            date_of_birth=date.today(), 
                            disability="D", 
                            dependent_of=self.employee)
    
    Dependent.objects.create(pid="38263212115",\
                            child=True,\
                            first_name="Stjepan", last_name="Ivić",
                            date_of_birth=date.today(), 
                            disability="D100", 
                            dependent_of=self.employee)
    
    Dependent.objects.create(pid="38263212116",\
                            child=False,\
                            first_name="Stjepan", last_name="Ivić",
                            date_of_birth=date.today(), 
                            disability="N", 
                            dependent_of=self.employee)
    
    Dependent.objects.create(pid="38263212117",\
                            child=False,\
                            first_name="Stjepan", last_name="Ivić",
                            date_of_birth=date.today(), 
                            disability="D", 
                            dependent_of=self.employee)
    
    Dependent.objects.create(pid="38263212118",\
                            child=False,\
                            first_name="Stjepan", last_name="Ivić",
                            date_of_birth=date.today(), 
                            disability="D", 
                            dependent_of=self.employee)
    
    Dependent.objects.create(pid="38263212119",\
                            child=True,\
                            first_name="Stjepan", last_name="Ivić",
                            date_of_birth=date.today(), 
                            disability="N", 
                            dependent_of=self.employee)
    
    self.deductible_dependents =\
        deductibles_calculation._deductible_dependents(self)
    self.deductible_children =\
        deductibles_calculation._deductible_children(self)
    self.deductible_dependents_disabled =\
        deductibles_calculation._deductible_dependents_disabled(
        self)
    self.deductible_dependents_disabled_100 =\
        deductibles_calculation._deductible_dependents_disabled_100(
        self)
    self.total_deductibles =\
        deductibles_calculation._total_deductibles(self)

