from decimal import *
import numpy


def percentage(n, percent):
    return Decimal(float(percent) * float(n) / 100)


def monthly_interest_rate(annual_interest_rate):
    return annual_interest_rate / 100 / NUM_MONTHS


def pmt(principle, annual_interest_rate, loan_term):
    return abs(numpy.pmt(monthly_interest_rate(annual_interest_rate), loan_term, float(principle)))


def monthly_expenses(monthly_mortgage, monthly_hoa, monthly_property_tax, monthly_home_insurance,
                     gross_monthly_rent, management_rate, vacancy_factor, maintenance_factor):
    return Decimal(float(monthly_mortgage) + float(monthly_hoa) + float(monthly_property_tax) +
                   float(monthly_home_insurance) +
                   float(percentage(gross_monthly_rent, management_rate)) +
                   float(percentage(gross_monthly_rent, vacancy_factor)) +
                   float(percentage(gross_monthly_rent, maintenance_factor)))

NUM_MONTHS = 12
LOAN_TERM_YEARS = 30
LOAN_TERM_MONTHS = NUM_MONTHS * LOAN_TERM_YEARS