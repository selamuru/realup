from decimal import *


def percentage(n, percent):
    return (Decimal(percent) * Decimal(n)) / 100

NUM_MONTHS = 12