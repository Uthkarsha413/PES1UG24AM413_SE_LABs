import pytest
from laundry_service import extra_weight_charge, order_acceptable, dropoff_status


# =======================================================================
# 1. Tests for extra_weight_charge()
# =======================================================================

def test_unknown_garment_type():
    with pytest.raises(ValueError, match="unknown garment type"):
        extra_weight_charge("leather", 5, "standard", False)


def test_invalid_negative_weight():
    with pytest.raises(ValueError, match="invalid weight"):
        extra_weight_charge("regular", -1, "standard", False)


def test_within_included_weight_non_member():
    # regular included is 5kg; weight 4kg -> extra = -1 <= 0 -> charge 0
    assert extra_weight_charge("regular", 4, "standard", False) == 0


def test_within_included_weight_member_bonus():
    # regular included becomes 5 + 2 = 7kg for member; weight 7kg -> extra = 0 -> charge 0
    assert extra_weight_charge("regular", 7, "standard", True) == 0


def test_standard_speed_no_extra_tier():
    # regular non-member included=5; weight 8 -> extra=3; rate=30 -> 90
    assert extra_weight_charge("regular", 8, "standard", False) == 90


def test_express_speed_no_extra_tier():
    # delicate non-member included=3; weight 6 -> extra=3; rate=50 -> 150
    assert extra_weight_charge("delicate", 6, "express", False) == 150


def test_standard_speed_with_heavy_extra_tier():
    # bedding member: included is 8 (no member bonus for bedding); weight 20 -> extra=12 (>10)
    # rate = 30 + 15 = 45 -> charge = 12 * 45 = 540
    assert extra_weight_charge("bedding", 20, "standard", True) == 540


def test_express_speed_with_heavy_extra_tier():
    # regular non-member included=5; weight 17 -> extra=12 (>10)
    # rate = 50 + 15 + 10 = 75 -> charge = 12 * 75 = 900
    assert extra_weight_charge("regular", 17, "express", False) == 900


# =======================================================================
# 2. Tests for order_acceptable()
# =======================================================================

def test_delicate_acceptable_items():
    assert order_acceptable(3, 5, True) is True


def test_delicate_too_many_items():
    assert order_acceptable(3, 6, True) is False


def test_overweight_order():
    assert order_acceptable(26, 10, False) is False


def test_normal_acceptable_order():
    assert order_acceptable(20, 30, False) is True


def test_normal_too_many_items():
    assert order_acceptable(20, 45, False) is False


# =======================================================================
# 3. Tests for dropoff_status()
# =======================================================================

def test_dropoff_bedding_express_accepted():
    # cutoff = 90 + 30 = 120
    assert dropoff_status(125, True, True) == "accepted"


def test_dropoff_bedding_express_late():
    # cutoff = 120; cutoff - 20 = 100
    assert dropoff_status(110, True, True) == "late"


def test_dropoff_bedding_express_rejected():
    assert dropoff_status(95, True, True) == "rejected"


def test_dropoff_regular_standard_accepted():
    # cutoff = 60
    assert dropoff_status(65, False, False) == "accepted"


def test_dropoff_regular_standard_late():
    # cutoff = 60; cutoff - 20 = 40
    assert dropoff_status(50, False, False) == "late"


def test_dropoff_regular_standard_rejected():
    assert dropoff_status(30, False, False) == "rejected"
