import pytest

from phone_repair_quote import (
    repair_quote,
    repair_days,
    trade_in_value,
)


def test_budget_screen():
    assert repair_quote("screen", "budget", False, False) == 4600


def test_flagship_screen_express():
    assert repair_quote("screen", "flagship", False, True) == 9100


def test_budget_battery():
    assert repair_quote("battery", "budget", False, False) == 1800


def test_flagship_camera():
    assert repair_quote("camera", "flagship", False, False) == 5300


def test_warranty_battery():
    assert repair_quote("battery", "budget", True, False) == 300


def test_warranty_charging_port():
    assert repair_quote("charging_port", "budget", True, False) == 300


def test_unknown_part():
    with pytest.raises(ValueError, match="unknown part"):
        repair_quote("speaker", "budget", False, False)


def test_unknown_brand_tier():
    with pytest.raises(ValueError, match="unknown brand tier"):
        repair_quote("screen", "premium", False, False)


def test_express_repair():
    assert repair_quote("charging_port", "budget", False, True) == 1600


def test_in_stock_quick():
    assert repair_days("battery", True, 2) == 1


def test_no_technician_available():
    assert repair_days("battery", True, 0) == 3


def test_screen_parts_unavailable():
    assert repair_days("screen", False, 1) == 6


def test_camera_parts_unavailable():
    assert repair_days("camera", False, 1) == 6


def test_battery_parts_unavailable():
    assert repair_days("battery", False, 1) == 3


def test_trade_in_under_12_months():
    assert trade_in_value(10000, 12, False) == 6000


def test_trade_in_between_13_and_24_months():
    assert trade_in_value(10000, 18, False) == 4000


def test_trade_in_between_25_and_48_months():
    assert trade_in_value(10000, 36, False) == 2000


def test_trade_in_over_48_months():
    assert trade_in_value(10000, 49, False) == 0


def test_trade_in_with_cracked_screen():
    assert trade_in_value(10000, 12, True) == 3000


def test_trade_in_invalid_original_price():
    with pytest.raises(ValueError, match="invalid input"):
        trade_in_value(0, 12, False)


def test_trade_in_negative_age():
    with pytest.raises(ValueError, match="invalid input"):
        trade_in_value(10000, -1, False)
