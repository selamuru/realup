from mongoengine import *
from realup.settings import MONGO_DB
from remanage.utils import percentage
import datetime

connect(MONGO_DB)

class MyDocument(Document):
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField(default=datetime.datetime.now, required=True)

    meta = {'allow_inheritance': True}

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
    purchase_price = FloatField(required=True)
    percentage_down = FloatField(required=True)
    interest_rate = FloatField(required=True)
    monthly_hoa = FloatField(required=True)
    property_tax_rate = FloatField(required=True)
    monthly_home_insurance = FloatField(required=True)
    management_rate = FloatField(required=True)
    maintenance_factor = FloatField(required=True)
    vacancy_factor = FloatField(required=True)
    gross_monthly_rent = FloatField(required=True)
    user = ReferenceField(User, reverse_delete_rule=CASCADE)

    # calculated fields
    down_payment = FloatField()
    initial_loan = FloatField()

    def calculate_fields(self):
        self.down_payment = percentage(self.purchase_price, self.percentage_down)
        self.initial_loan = self.purchase_price - self.down_payment

    _pre_save_hooks = [
        MyDocument.calculate_timestamps,
        calculate_fields
    ]

    meta = {'collection': 'properties'}

