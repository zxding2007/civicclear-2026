"""Toronto residential municipal property tax *estimate*, excluding education tax."""
from decimal import Decimal, ROUND_HALF_UP


def municipal_tax(assessed_value: float, rate_percent: float) -> float:
    value = Decimal(str(assessed_value))
    rate = Decimal(str(rate_percent))
    if value < 0 or rate < 0:
        raise ValueError('assessed value and rate must not be negative')
    return float((value * rate / Decimal('100')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))


def compare(assessed_value: float, before_rate: float, after_rate: float) -> dict:
    before = municipal_tax(assessed_value, before_rate)
    after = municipal_tax(assessed_value, after_rate)
    return {'before': before, 'after': after, 'difference': round(after - before, 2)}
