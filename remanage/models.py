from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.db.models import *
#from mongoengine import *
from realup.settings import MONGO_USERNAME, MONGO_PASSWORD, MONGO_HOST, MONGO_DB
from remanage.utils import *
import datetime
from decimal import *
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.http import urlquote
from django.core.mail import send_mail
from django.utils import timezone


#connect(MONGO_DB)


# class BaseModel(models.Model):
#     created_at = DateTimeField(blank=False)
#     updated_at = DateTimeField(default=timezone.now, blank=False)
#
#     class Meta:
#         abstract = True
#
#     def calculate_timestamps(self):
#         if not self.created_at:
#             self.created_at = datetime.datetime.now()
#         self.updated_at = datetime.datetime.now()
#
#     _pre_save_hooks = [
#         calculate_timestamps
#     ]
#
#     def save(self, *args, **kwargs):
#         for hook in self._pre_save_hooks:
#             hook(self)
#
#         super(BaseModel, self).save(*args, **kwargs)


# class User(BaseModel):
#     first_name = CharField(blank=False)
#     last_name = CharField(blank=False)
#     email = CharField(blank=False)
#     password = CharField(blank=False)
#
#     class Meta:
#         db_table = 'users'
#
#     def hash_password(self):
#         self.password = make_password(self.password)
#
#     def set_password(self, password):
#         self.password = make_password(password)
#
#     def check_password(self, password):
#         return check_password(password, self.password)
#
#     _pre_save_hooks = [
#         BaseModel.calculate_timestamps,
#         hash_password
#     ]


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, last_login=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = EmailField('email address', max_length=254, unique=True, blank=False)
    first_name = CharField('first name', max_length=30, blank=False)
    last_name = CharField('last name', max_length=30, blank=False)
    created_at = DateTimeField(default=timezone.now, blank=False)
    updated_at = DateTimeField(default=timezone.now, blank=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        #verbose_name = 'user'
        #verbose_name_plural = 'users'
        db_table = 'users'

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])


class Property(models.Model):
    # required fields
    name = CharField(max_length=120, blank=False)
    address = CharField(max_length=500, blank=False)
    purchase_price = DecimalField(max_digits=30, blank=False, decimal_places=2)
    percentage_down = FloatField(blank=False)
    interest_rate = FloatField(blank=False)
    monthly_hoa = DecimalField(max_digits=30, blank=False, decimal_places=2)
    property_tax_rate = FloatField(blank=False)
    monthly_home_insurance = DecimalField(max_digits=30, blank=False, decimal_places=2)
    management_rate = FloatField(blank=False)
    maintenance_factor = FloatField(blank=False)
    vacancy_factor = FloatField(blank=False)
    gross_monthly_rent = DecimalField(max_digits=30, blank=False, decimal_places=2)
    user = ForeignKey('CustomUser', on_delete=CASCADE, blank=False)
    created_at = DateTimeField(default=timezone.now, blank=False)
    updated_at = DateTimeField(default=timezone.now, blank=False)

    # calculated fields
    down_payment = DecimalField(max_digits=30, decimal_places=2)
    initial_loan = DecimalField(max_digits=30, decimal_places=2)
    monthly_mortgage = DecimalField(max_digits=30, decimal_places=2)
    monthly_property_tax = DecimalField(max_digits=30, decimal_places=2)
    total_monthly_expenses = DecimalField(max_digits=30, decimal_places=2)
    gross_yearly_rent = DecimalField(max_digits=30, decimal_places=2)
    net_monthly_cash_flow = DecimalField(max_digits=30, decimal_places=2)
    net_annual_cash_flow = DecimalField(max_digits=30, decimal_places=2)
    net_annual_roi = DecimalField(max_digits=30, decimal_places=2)

    objects = Manager()

    class Meta:
        db_table = 'properties'

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

    def save(self, *args, **kwargs):
        self.calculate_fields()
        super(Property, self).save(*args, **kwargs)
