import unittest
import uuid
from datetime import date
from jsonschema import validate, Draft202012Validator, exceptions, ValidationError

import json

# Charger le schéma depuis un fichier externe ou le copier ici directement
with open("extended_schemes\\reservation_schema.json", "r") as f:
    schema = json.load(f)

validator = Draft202012Validator(schema)

# Quelques fonctions d'exemple pour générer des données valides
def generate_valid_concert_reservation():
    return {
        "reservationID": str(uuid.uuid4()),
        "event_type": {
            "artists": [
                {
                    "band_name": "The Rolling Stones",
                    "nb_members": 5,
                    "music_type": "rock"
                }
            ]
        },
        "starting_date": date.today().isoformat(),
        "ending_date": date.today().isoformat(),
        "duration": "02:00:00",
        "status": "confirmed",
        "hall": {
            "name": "Grande Salle",
            "address": {
                "street_address": "123 Rue de Paris",
                "city": "Paris",
                "state": "Île-de-France",
                "country": "France"
            },
            "nb_seat": 500,
            "accessibility": ["metro", "buses", "highway"],
            "highway_id": "A10",
            "metro": {
                "line": "4",
                "stop": "Châtelet"
            },
            "bus": {
                "line": "7",
                "stop": "Lieu de Vie"
            },
            "parking": True,
            "parking_spots": 100
        }
    }

def generate_invalid_reservation_missing_required():
    data = generate_valid_concert_reservation()
    del data["hall"]["address"]
    return data

def generate_valid_match_reservation():
    return {
        "reservationID": str(uuid.uuid4()),
        "event_type": {
            "kind": "championship",
            "rankings": "quarter final",
            "teams": [
                {
                    "name": "Red Lions",
                    "sport": "basket",
                    "coach": {
                        "firstname": "Jean",
                        "lastname": "Dupont"
                    },
                    "nb_players": 12
                },
                {
                    "name": "Blue Hawks",
                    "sport": "basket",
                    "coach": {
                        "firstname": "Alice",
                        "lastname": "Martin"
                    },
                    "nb_players": 10
                }
            ]
        },
        "starting_date": "2025-07-01",
        "ending_date": "2025-07-01",
        "duration": "01:30:00",
        "status": "pending",
        "hall": {
            "name": "Stade Central",
            "address": {
                "street_address": "45 Avenue des Champs",
                "city": "Lyon",
                "state": "Rhône",
                "country": "France"
            },
            "nb_seat": 2000,
            "accessibility": ["highway"],
            "highway_id": "A6",
            "parking": False
        }
    }

class TestReservationSchema(unittest.TestCase):

    def test_valid_concert_reservation(self):
        data = generate_valid_concert_reservation()
        try:
            validator.validate(data)
        except ValidationError as e:
            self.fail(f"Valid concert reservation failed validation: {e.message}")

    def test_valid_match_reservation(self):
        data = generate_valid_match_reservation()
        try:
            validator.validate(data)
        except ValidationError as e:
            self.fail(f"Valid match reservation failed validation: {e.message}")

    def test_missing_required_field(self):
        data = generate_invalid_reservation_missing_required()
        with self.assertRaises(ValidationError):
            validator.validate(data)

    def test_invalid_enum_value(self):
        data = generate_valid_concert_reservation()
        data["status"] = "approved"  # Invalid status
        with self.assertRaises(ValidationError):
            validator.validate(data)

    def test_missing_parking_spots_when_parking_true(self):
        data = generate_valid_concert_reservation()
        del data["hall"]["parking_spots"]  # Required when parking is true
        with self.assertRaises(ValidationError):
            validator.validate(data)

if __name__ == "__main__":
    unittest.main()
