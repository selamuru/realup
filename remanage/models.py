from mongoengine import *
from realup.settings import MONGO_DB
from remanage.utils import *
import datetime
from decimal import *

connect(MONGO_DB)


class MyDocument(Document):
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField(default=datetime.datetime.now, required=True)

    meta = {'allow_inheritance': True, 'abstract': True}

    def calculate_timestamps(self):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    _pre_save_hooks = [
        calculate_timestamps
    ]

    def save(self, *args, **kwargs):
        for hook in self._pre_save_hooks:
            hook(self)

        super(MyDocument, self).save(*args, **kwargs)


class User(MyDocument):
    name = StringField(required=True)
    email = StringField(required=True)

    meta = {'collection': 'users'}


class Property(MyDocument):
    # required fields
    name = StringField(max_length=120, required=True)
    address = StringField(max_length=500, required=True)
    purchase_price = DecimalField(required=True, precision=2)
    percentage_down = FloatField(required=True)
    interest_rate = FloatField(required=True)
    monthly_hoa = DecimalField(required=True, precision=2)
    property_tax_rate = FloatField(required=True, precision=4)
    monthly_home_insurance = DecimalField(required=True, precision=2)
    management_rate = FloatField(required=True, precision=2)
    maintenance_factor = FloatField(required=True, precision=2)
    vacancy_factor = FloatField(required=True)
    gross_monthly_rent = DecimalField(required=True, precision=2)
    user = ReferenceField('User', reverse_delete_rule=CASCADE, required=True)

    # calculated fields
    down_payment = DecimalField(precision=2)
    initial_loan = DecimalField(precision=2)
    monthly_mortgage = DecimalField(precision=2)
    monthly_property_tax = DecimalField(precision=2)
    total_monthly_expenses = DecimalField(precision=2)
    gross_yearly_rent = DecimalField(precision=2)
    net_monthly_cash_flow = DecimalField(precision=2)
    net_annual_cash_flow = DecimalField(precision=2)
    net_annual_roi = DecimalField(precision=2)

    meta = {'collection': 'properties'}

    def calculate_fields(self):
        self.down_payment = percentage(self.purchase_price, self.percentage_down)
        self.initial_loan = self.purchase_price - self.down_payment
        self.monthly_mortgage = Decimal(pmt(self.initial_loan, self.interest_rate,
                                            LOAN_TERM_MONTHS))
        self.monthly_property_tax = (percentage(self.purchase_price,
                                                self.property_tax_rate)) / NUM_MONTHS

        self.total_monthly_expenses = monthly_expenses(self.monthly_mortgage, self.monthly_hoa,
                                                       self.monthly_property_tax,
                                                       self.monthly_home_insurance,
                                                       self.gross_monthly_rent,
                                                       self.management_rate, self.vacancy_factor,
                                                       self.maintenance_factor)
        self.gross_yearly_rent = self.gross_monthly_rent * NUM_MONTHS
        self.net_monthly_cash_flow = self.gross_monthly_rent - self.total_monthly_expenses
        self.net_annual_cash_flow = self.net_monthly_cash_flow * NUM_MONTHS
        self.net_annual_roi = self.net_annual_cash_flow / self.down_payment * 100

    _pre_save_hooks = [
        MyDocument.calculate_timestamps,
        calculate_fields
    ]
