from remanage.models import Property, User
import unittest
from decimal import *


class TestProperty(unittest.TestCase):
    def setUp(self):
        self.my_user = User(name='John', email='john@test123.com')
        self.my_property = Property(name='test_property', address='123 Test Ave San Jose, CA 45678',
                                    purchase_price=1780000, percentage_down=25, interest_rate=3.25,
                                    monthly_hoa=200, property_tax_rate=1.2617,
                                    monthly_home_insurance=100, management_rate=7,
                                    maintenance_factor=10, vacancy_factor=6, gross_monthly_rent=6000,
                                    user=self.my_user)
        self.my_user.save()
        self.my_property.save()

    def tearDown(self):
        self.my_property.delete()
        self.assertEqual(Property.objects(user=self.my_user).count(), 0)
        self.my_user.delete()
        self.assertEqual(User.objects(email=self.my_user.email).count(), 0)

    def test_crud_property(self):
        self.assertEqual(Property.objects(user=self.my_user).count(), 1)
        self.assertEqual(Property.objects(user=self.my_user)[0], self.my_property)
        self.assert_(Property.objects(user=self.my_user)[0].created_at)
        self.assert_(Property.objects(user=self.my_user)[0].updated_at)

        self.my_property.name = 'test_property_2'
        self.my_property.save()
        self.assertEqual(Property.objects(id=self.my_property.id)[0].name, 'test_property_2')
        self.assertNotEqual(Property.objects(user=self.my_user)[0].updated_at,
                            Property.objects(user=self.my_user)[0].created_at)

    def test_calculated_fields(self):
        self.assertEqual(Property.objects(id=self.my_property.id)[0].down_payment,
                         Decimal('445000'))
        self.assertEqual(Property.objects(id=self.my_property.id)[0].initial_loan,
                         Decimal('1335000'))
        self.assertEqual(Property.objects(id=self.my_property.id)[0].monthly_mortgage,
                         Decimal('5810'))
        self.assertEqual(Property.objects(id=self.my_property.id)[0].monthly_property_tax,
                         Decimal('1871.52'))
        self.assertEqual(Property.objects(id=self.my_property.id)[0].total_monthly_expenses,
                         Decimal('9361.53'))
        self.assertEqual(Property.objects(id=self.my_property.id)[0].gross_yearly_rent,
                         Decimal('72000'))
        self.assertEqual(Property.objects(id=self.my_property.id)[0].net_monthly_cash_flow,
                         Decimal('-3361.53'))
        self.assertEqual(Property.objects(id=self.my_property.id)[0].net_annual_cash_flow,
                         Decimal('-40338.31'))
        self.assertEqual(Property.objects(id=self.my_property.id)[0].net_annual_roi,
                         Decimal('-9.06'))

    def test_property_deletion_when_user_deleted(self):
        self.assertEqual(User.objects(email=self.my_user.email).count(), 1)
        self.assertEqual(Property.objects(user=self.my_user).count(), 1)

        self.my_user.delete()
        self.assertEqual(User.objects(email=self.my_user.email).count(), 0)
        self.assertEqual(Property.objects(user=self.my_user).count(), 0)


class TestUser(unittest.TestCase):
    def setUp(self):
        self.my_user = User(name='John', email='john@test123.com')
        self.my_user.save()

    def tearDown(self):
        self.my_user.delete()
        self.assertEqual(User.objects.count(), 0)

    def test_crud_user(self):
        self.assertEqual(User.objects(email=self.my_user.email).count(), 1)
        self.assertEqual(User.objects(email=self.my_user.email)[0], self.my_user)
        self.assert_(User.objects(email=self.my_user.email)[0].created_at)
        self.assert_(User.objects(email=self.my_user.email)[0].updated_at)

        self.my_user.name = 'Sara'
        self.my_user.save()
        self.assertEqual(User.objects(email=self.my_user.email)[0].name, 'Sara')
        self.assertNotEqual(User.objects(email=self.my_user.email)[0].updated_at,
                            User.objects(email=self.my_user.email)[0].created_at)
