import math


def parse_order(text):
    if not isinstance(text, str):
        raise ValueError("Order must be a string")

    parts = text.split(':')
    if len(parts) != 2:
        raise ValueError("Order must contain exactly one colon in format 'garment:weight'")

    garment = parts[0].strip()
    weight_text = parts[1].strip()

    if not garment:
        raise ValueError("Garment name cannot be empty")
    if not weight_text:
        raise ValueError("Weight cannot be empty")

    try:
        kg = float(weight_text)
    except ValueError:
        raise ValueError("Weight must be a valid number")

    if not math.isfinite(kg) or kg < 0:
        raise ValueError("Weight must be a finite, non-negative number")

    return garment.title(), kg


def weight_average(weights_csv):
    if not isinstance(weights_csv, str):
        raise ValueError("Weights must be a string")

    if not weights_csv.strip():
        raise ValueError("Weights list cannot be empty")

    parts = weights_csv.split(',')
    values = []

    for item in parts:
        item = item.strip()
        if not item:
            raise ValueError("Weight list contains an empty element")
        try:
            val = int(item)
        except ValueError:
            raise ValueError("All weights must be valid integers")

        if val < 0:
            raise ValueError("Weights cannot be negative")
        values.append(val)

    if not values:
        raise ValueError("Weights list cannot be empty")

    return sum(values) // len(values)


def payable_charge(text):
    if not isinstance(text, str):
        raise ValueError("Charge details must be a string")

    parts = text.split('|')
    if len(parts) != 2:
        raise ValueError("Input must contain exactly one '|' in format 'charge|discount'")

    charge_text = parts[0].strip()
    discount_text = parts[1].strip()

    if not charge_text or not discount_text:
        raise ValueError("Charge and discount cannot be empty")

    try:
        charge = float(charge_text)
        discount = float(discount_text)
    except ValueError:
        raise ValueError("Charge and discount must be valid numbers")

    if not math.isfinite(charge) or not math.isfinite(discount):
        raise ValueError("Charge and discount must be finite numbers")

    if charge < 0 or discount < 0:
        raise ValueError("Charge and discount cannot be negative")

    total = charge * 1.18 - discount
    return max(total, 0)


def main():
    print("==== Running parse_order ====")
    user_input = input("Enter garment:weight in kg (e.g. regular:6): ")
    try:
        result = parse_order(user_input)
        print("Garment and Weight:", result)
    except ValueError as e:
        print("Invalid input:", e)

    print("\n==== Running weight_average ====")
    user_input = input("Enter garment weights as CSV (e.g. 3,5,8): ")
    try:
        result = weight_average(user_input)
        print("Average Weight:", result)
    except ValueError as e:
        print("Invalid input:", e)

    print("\n==== Running payable_charge ====")
    user_input = input("Enter charge|discount (e.g. 300|40): ")
    try:
        result = payable_charge(user_input)
        print("Payable Charge:", result)
    except ValueError as e:
        print("Invalid input:", e)


if __name__ == "__main__":
    main()
