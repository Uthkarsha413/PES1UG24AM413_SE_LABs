import pytest
from laundry_service import extra_weight_charge, order_acceptable, dropoff_status


# =======================================================================
# EXTRA WEIGHT CHARGE - BRANCH TESTING
# =======================================================================

# Test 1: Invalid garment type (triggers if garment_type not in INCLUDED_KG)
def test_garment_type_invalid():
    with pytest.raises(ValueError, match="unknown garment type"):
        extra_weight_charge("silk", 5, "standard", False)


# Test 2: Valid garment types (false branch for garment_type not in INCLUDED_KG)
def test_garment_type_valid_regular():
    assert extra_weight_charge("regular", 5, "standard", False) == 0


def test_garment_type_valid_delicate():
    assert extra_weight_charge("delicate", 3, "standard", False) == 0


def test_garment_type_valid_bedding():
    assert extra_weight_charge("bedding", 8, "standard", False) == 0


# Test 3: Negative weight (triggers if weight_kg < 0)
def test_weight_negative():
    with pytest.raises(ValueError, match="invalid weight"):
        extra_weight_charge("regular", -0.5, "standard", False)


# Test 4: Boundary weight exactly 0 (evaluates weight_kg < 0 to False)
def test_weight_zero_boundary():
    assert extra_weight_charge("regular", 0, "standard", False) == 0


# Test 5: Member bonus with non-bedding garment (is_member=True and garment_type!="bedding")
def test_member_regular_bonus():
    # included becomes 5 + 2 = 7; weight 7 -> extra 0 -> return 0
    assert extra_weight_charge("regular", 7, "standard", True) == 0


# Test 6: Member bonus with bedding garment (is_member=True and garment_type=="bedding")
def test_member_bedding_no_bonus():
    # bedding stays at 8; weight 9 -> extra = 1; rate = 30 -> charge 30
    assert extra_weight_charge("bedding", 9, "standard", True) == 30


# Test 7: Non-member with non-bedding garment (is_member=False and garment_type!="bedding")
def test_non_member_regular():
    # included is 5; weight 6 -> extra 1; rate = 30 -> charge 30
    assert extra_weight_charge("regular", 6, "standard", False) == 30


# Test 8: Non-member with bedding garment (is_member=False and garment_type=="bedding")
def test_non_member_bedding():
    # included is 8; weight 9 -> extra 1; rate = 30 -> charge 30
    assert extra_weight_charge("bedding", 9, "standard", False) == 30


# Test 9: Extra weight <= 0 (weight strictly below included limit)
def test_extra_weight_negative():
    assert extra_weight_charge("regular", 3, "standard", False) == 0


# Test 10: Extra weight boundary exactly 0 (weight == included)
def test_extra_weight_zero_boundary():
    assert extra_weight_charge("regular", 5, "standard", False) == 0


# Test 11: Extra weight > 0 with standard speed
def test_speed_standard_normal_tier():
    # extra = 8 - 5 = 3 (<= 10); rate = 30 -> charge = 90
    assert extra_weight_charge("regular", 8, "standard", False) == 90


# Test 12: Extra weight > 0 with non-standard speed (e.g., express)
def test_speed_express_normal_tier():
    # extra = 8 - 5 = 3 (<= 10); rate = 50 -> charge = 150
    assert extra_weight_charge("regular", 8, "express", False) == 150


# Test 13: Extra weight boundary exactly 10 (extra > 10 evaluates to False)
def test_extra_weight_boundary_10():
    # weight = 15, included = 5 -> extra = 10; rate remains 30 -> charge = 300
    assert extra_weight_charge("regular", 15, "standard", False) == 300


# Test 14: Extra weight boundary 11 (extra > 10 evaluates to True) with standard speed
def test_extra_weight_boundary_11_standard():
    # weight = 16, included = 5 -> extra = 11; rate = 30 + 15 = 45 -> charge = 495
    assert extra_weight_charge("regular", 16, "standard", False) == 495


# Test 15: Extra weight > 10 with express speed (triggers rate += 10)
def test_extra_weight_heavy_express():
    # weight = 16, included = 5 -> extra = 11; rate = 50 + 15 + 10 = 75 -> charge = 825
    assert extra_weight_charge("regular", 16, "express", False) == 825


# Test 16: Extra weight > 10 with alternate non-express speed
def test_extra_weight_heavy_alternate_speed():
    # speed "overnight" != "standard" (rate 50), extra=12 (>10 -> rate 65), speed != "express"
    assert extra_weight_charge("regular", 17, "overnight", False) == 12 * 65


# =======================================================================
# ORDER ACCEPTABLE - BRANCH TESTING
# =======================================================================

# Test 17: Delicate order with items <= 5 (boundary: exactly 5 items)
def test_order_delicate_items_boundary_5():
    assert order_acceptable(10, 5, True) is True


# Test 18: Delicate order with items < 5
def test_order_delicate_items_below_5():
    assert order_acceptable(10, 2, True) is True


# Test 19: Delicate order with items > 5 (boundary: exactly 6 items)
def test_order_delicate_items_boundary_6():
    assert order_acceptable(10, 6, True) is False


# Test 20: Non-delicate order with weight > 25 (boundary: exactly 26kg)
def test_order_non_delicate_weight_boundary_26():
    assert order_acceptable(26, 10, False) is False


# Test 21: Non-delicate order with weight exactly 25kg (boundary weight_kg > 25 is False)
def test_order_non_delicate_weight_boundary_25():
    assert order_acceptable(25, 40, False) is True


# Test 22: Non-delicate order with items <= 40 (boundary: exactly 40 items)
def test_order_non_delicate_items_boundary_40():
    assert order_acceptable(20, 40, False) is True


# Test 23: Non-delicate order with items > 40 (boundary: exactly 41 items)
def test_order_non_delicate_items_boundary_41():
    assert order_acceptable(20, 41, False) is False


# =======================================================================
# DROPOFF STATUS - BRANCH TESTING
# =======================================================================

# Case A: Standard + Regular (has_bedding=False, is_express=False) -> cutoff = 60
def test_dropoff_standard_regular_accepted_boundary():
    # minutes == 60 (accepted boundary)
    assert dropoff_status(60, False, False) == "accepted"


def test_dropoff_standard_regular_accepted_above():
    # minutes == 75 (strictly accepted)
    assert dropoff_status(75, False, False) == "accepted"


def test_dropoff_standard_regular_late_upper_boundary():
    # minutes == 59 (late upper boundary)
    assert dropoff_status(59, False, False) == "late"


def test_dropoff_standard_regular_late_lower_boundary():
    # minutes == 40 (cutoff 60 - 20 = 40, late lower boundary)
    assert dropoff_status(40, False, False) == "late"


def test_dropoff_standard_regular_rejected_boundary():
    # minutes == 39 (rejected upper boundary)
    assert dropoff_status(39, False, False) == "rejected"


# Case B: Express + Regular (has_bedding=False, is_express=True) -> cutoff = 60 + 30 = 90
def test_dropoff_express_regular_accepted_boundary():
    assert dropoff_status(90, False, True) == "accepted"


def test_dropoff_express_regular_late_boundary():
    # cutoff 90 - 20 = 70
    assert dropoff_status(70, False, True) == "late"


def test_dropoff_express_regular_rejected_boundary():
    assert dropoff_status(69, False, True) == "rejected"


# Case C: Standard + Bedding (has_bedding=True, is_express=False) -> cutoff = 90
def test_dropoff_standard_bedding_accepted_boundary():
    assert dropoff_status(90, True, False) == "accepted"


def test_dropoff_standard_bedding_late_boundary():
    # cutoff 90 - 20 = 70
    assert dropoff_status(70, True, False) == "late"


def test_dropoff_standard_bedding_rejected_boundary():
    assert dropoff_status(69, True, False) == "rejected"


# Case D: Express + Bedding (has_bedding=True, is_express=True) -> cutoff = 90 + 30 = 120
def test_dropoff_express_bedding_accepted_boundary():
    assert dropoff_status(120, True, True) == "accepted"


def test_dropoff_express_bedding_late_upper():
    assert dropoff_status(119, True, True) == "late"


def test_dropoff_express_bedding_late_lower_boundary():
    # cutoff 120 - 20 = 100
    assert dropoff_status(100, True, True) == "late"


def test_dropoff_express_bedding_rejected_boundary():
    assert dropoff_status(99, True, True) == "rejected"
