import pytest
from hypothesis import given, strategies as st
from laundry_service import parse_order, weight_average, payable_charge


# =======================================================================
# 1. Hypothesis Fuzz Testing (Handling arbitrary strings and None)
# =======================================================================

@given(st.text() | st.none())
def test_parse_order_no_crash(s):
    try:
        parse_order(s)
    except ValueError:
        pass


@given(st.text() | st.none())
def test_weight_average_no_crash(s):
    try:
        weight_average(s)
    except ValueError:
        pass


@given(st.text() | st.none())
def test_payable_charge_no_crash(s):
    try:
        payable_charge(s)
    except ValueError:
        pass


# =======================================================================
# 2. Valid Input Unit Tests
# =======================================================================

def test_parse_order_valid():
    assert parse_order("regular:6") == ("Regular", 6.0)
    assert parse_order("  delicate  : 3.5 ") == ("Delicate", 3.5)
    assert parse_order("bedding:10") == ("Bedding", 10.0)


def test_weight_average_valid():
    assert weight_average("3,5,8") == 5
    assert weight_average("10") == 10
    assert weight_average(" 4 , 6 , 8 ") == 6


def test_payable_charge_valid():
    # 300 * 1.18 - 40 = 354 - 40 = 314.0
    assert payable_charge("300|40") == 314.0
    # Large discount capping at 0
    assert payable_charge("100|200") == 0


# =======================================================================
# 3. Invalid Input Unit Tests
# =======================================================================

def test_parse_order_invalid_inputs():
    with pytest.raises(ValueError):
        parse_order(None)
    with pytest.raises(ValueError):
        parse_order("")
    with pytest.raises(ValueError):
        parse_order("regular")
    with pytest.raises(ValueError):
        parse_order("regular:abc")
    with pytest.raises(ValueError):
        parse_order(":5")
    with pytest.raises(ValueError):
        parse_order("regular:-5")
    with pytest.raises(ValueError):
        parse_order("regular:nan")


def test_weight_average_invalid_inputs():
    with pytest.raises(ValueError):
        weight_average(None)
    with pytest.raises(ValueError):
        weight_average("")
    with pytest.raises(ValueError):
        weight_average("3,,8")
    with pytest.raises(ValueError):
        weight_average("3,abc,8")
    with pytest.raises(ValueError):
        weight_average("3,-5,8")


def test_payable_charge_invalid_inputs():
    with pytest.raises(ValueError):
        payable_charge(None)
    with pytest.raises(ValueError):
        payable_charge("")
    with pytest.raises(ValueError):
        payable_charge("300")
    with pytest.raises(ValueError):
        payable_charge("300|abc")
    with pytest.raises(ValueError):
        payable_charge("-300|40")
    with pytest.raises(ValueError):
        payable_charge("300|-10")
    with pytest.raises(ValueError):
        payable_charge("inf|40")
