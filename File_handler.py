import json
import os

FILE = "data/Bank_data.json"


# LOAD DATA
def load_data(filename=FILE):
    try:
        with open(filename, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return {
            "accounts": [],
            "transactions": []
        }

    except json.JSONDecodeError:
        print("Error: The data file is damaged.")

        return {
            "accounts": [],
            "transactions": []
        }


# SAVE DATA
def save_data(data, filename=FILE):
    try:
        os.makedirs("data", exist_ok=True)

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    except OSError as error:
        print("File saving error:", error)
