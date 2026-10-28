import pytest

from phone_repair_quote import (
    repair_quote,
    repair_days,
    trade_in_value,
)


# 1. Part validation branches

def test_valid_part():
    assert repair_quote("battery", "budget", False, False) == 1800


def test_invalid_part():
    with pytest.raises(ValueError, match="unknown part"):
        repair_quote("speaker", "budget", False, False)


# 2. Brand tier validation branches

def test_valid_brand_tier():
    assert repair_quote("screen", "budget", False, False) == 4600


def test_invalid_brand_tier():
    with pytest.raises(ValueError, match="unknown brand tier"):
        repair_quote("screen", "premium", False, False)


# 3. Flagship and budget branches

def test_flagship_cost():
    assert repair_quote("battery", "flagship", False, False) == 3300


def test_budget_cost():
    assert repair_quote("battery", "budget", False, False) == 1800


# 4. Screen and non-screen branches

def test_screen_labour():
    assert repair_quote("screen", "budget", False, False) == 4600


def test_non_screen_labour():
    assert repair_quote("camera", "budget", False, False) == 2800


# 5. Warranty branches

def test_warranty_non_screen():
    assert repair_quote("battery", "budget", True, False) == 300


def test_warranty_screen():
    assert repair_quote("screen", "budget", True, False) == 4600


def test_no_warranty():
    assert repair_quote("battery", "budget", False, False) == 1800


# 6. Express service branches

def test_express_enabled():
    assert repair_quote("battery", "budget", False, True) == 2300


def test_express_disabled():
    assert repair_quote("battery", "budget", False, False) == 1800


# 7. Technician availability branches

def test_no_technicians_free():
    assert repair_days("battery", True, 0) == 3


def test_technician_available():
    assert repair_days("battery", True, 1) == 1


# 8. Parts availability branches

def test_parts_in_stock():
    assert repair_days("battery", True, 1) == 1


def test_parts_not_in_stock_screen():
    assert repair_days("screen", False, 1) == 6


def test_parts_not_in_stock_camera():
    assert repair_days("camera", False, 1) == 6


def test_parts_not_in_stock_battery():
    assert repair_days("battery", False, 1) == 3


def test_parts_not_in_stock_charging_port():
    assert repair_days("charging_port", False, 1) == 3


# 9. Invalid trade-in inputs

def test_zero_original_price():
    with pytest.raises(ValueError, match="invalid input"):
        trade_in_value(0, 12, False)


def test_negative_original_price():
    with pytest.raises(ValueError, match="invalid input"):
        trade_in_value(-100, 12, False)


def test_negative_age():
    with pytest.raises(ValueError, match="invalid input"):
        trade_in_value(10000, -1, False)


# 10. Age over 48 months

def test_age_over_48_months():
    assert trade_in_value(10000, 49, False) == 0


def test_age_exactly_48_months():
    assert trade_in_value(10000, 48, False) == 2000


# 11. Trade-in age bands

def test_age_12_months():
    assert trade_in_value(10000, 12, False) == 6000


def test_age_13_months():
    assert trade_in_value(10000, 13, False) == 4000


def test_age_24_months():
    assert trade_in_value(10000, 24, False) == 4000


def test_age_25_months():
    assert trade_in_value(10000, 25, False) == 2000


# 12. Cracked and uncracked screens

def test_screen_not_cracked():
    assert trade_in_value(10000, 12, False) == 6000


def test_screen_cracked():
    assert trade_in_value(10000, 12, True) == 3000
