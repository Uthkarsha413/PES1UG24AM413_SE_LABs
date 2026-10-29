"""Manage flight reservations, baggage fees, and passenger manifests safely."""

import hashlib
import json
import secrets
from pathlib import Path

FLIGHTS = {
    "AI101": {
        "destination": "London",
        "seats": 2,
        "fare": 450.0,
        "is_full": False,
    },
    "BA202": {
        "destination": "New York",
        "seats": 0,
        "fare": 600.0,
        "is_full": True,
    },
    "EK303": {
        "destination": "Dubai",
        "seats": 5,
        "fare": 320.0,
        "is_full": False,
    },
}

reservation_state = {"total_revenue": 0.0}


def book_flight_seat(
    flight_no, passenger, luggage_weight=15, baggage_tags=None
):
    """Book one available seat and append a record to baggage_tags."""
    if baggage_tags is None:
        baggage_tags = []

    flight = FLIGHTS.get(flight_no)
    if flight is None or flight["is_full"] or flight["seats"] <= 0:
        return False
    if luggage_weight < 0:
        raise ValueError("Luggage weight cannot be negative.")

    flight["seats"] -= 1
    flight["is_full"] = flight["seats"] == 0
    reservation_state["total_revenue"] += flight["fare"]
    baggage_tags.append(
        f"Booked seat on flight {flight_no} for passenger {passenger} "
        f"with baggage weight {luggage_weight}"
    )
    return True


def cancel_booking(flight_no):
    """Restore one seat if the flight exists and is currently full."""
    flight = FLIGHTS.get(flight_no)
    if flight is None or not flight["is_full"]:
        return False

    flight["seats"] += 1
    flight["is_full"] = False
    return True


def check_seat_availability(flight_no):
    """Return whether a known flight has at least one available seat."""
    flight = FLIGHTS.get(flight_no)
    return flight is not None and not flight["is_full"] and flight["seats"] > 0


def calculate_baggage_fee(flight_no, surcharge_rate=0.15):
    """Calculate a baggage surcharge as a rate of the flight's base fare."""
    flight = FLIGHTS.get(flight_no)
    if flight is None:
        raise ValueError(f"Unknown flight number: {flight_no}")
    if not 0 <= surcharge_rate <= 1:
        raise ValueError("Surcharge rate must be between 0 and 1.")
    return flight["fare"] * surcharge_rate


def generate_passenger_hash(passenger_id):
    """Return a SHA-256 digest for a passenger identifier."""
    return hashlib.sha256(passenger_id.encode("utf-8")).hexdigest()


def generate_boarding_pin():
    """Generate a four-digit PIN using a cryptographically secure source."""
    return secrets.randbelow(9000) + 1000


def export_flight_manifest(filename="flight_manifest.json"):
    """Export flight details as UTF-8 JSON without invoking a shell."""
    output_path = Path(filename)
    with output_path.open("w", encoding="utf-8") as manifest_file:
        json.dump(FLIGHTS, manifest_file, indent=2)
    print(f"Boarding manifest exported to: {output_path}")


def get_flight_summary(flights):
    """Count flights that currently have seats available."""
    return sum(
        1
        for details in flights.values()
        if not details["is_full"] and details["seats"] > 0
    )


def main():
    """Run a small demonstration of the flight reservation functions."""
    booking_tags = []
    book_flight_seat("AI101", "Kritika", 20, booking_tags)
    cancel_booking("BA202")
    print("Is AI101 open:", check_seat_availability("AI101"))
    print("Baggage Fee:", calculate_baggage_fee("AI101", 0.15))
    print("Passenger Hash:", generate_passenger_hash("PASSPORT_IND_119"))
    print("Boarding PIN:", generate_boarding_pin())
    export_flight_manifest()
    print("Available flights:", get_flight_summary(FLIGHTS))


if __name__ == "__main__":
    main()
