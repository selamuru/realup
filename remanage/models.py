from mongoengine import *
from realup.settings import MONGO_DB
import datetime

connect(MONGO_DB)

class Property(Document):
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    updated_at = DateTimeField(default=datetime.datetime.now, required=True)
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

    meta = {'collection': 'properties'}
