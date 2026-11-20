import json
import os


# FILE LOCATION
# Gets the folder where File_handler.py is located
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))


# Gets the data folder inside LocBank
DATA_FOLDER = os.path.join(BASE_FOLDER, "data")


# JSON file location
FILE = os.path.join(DATA_FOLDER, "bank_data.json")


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
        # Creates the data folder if it does not exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Saves the banking data into JSON
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        print("Bank data successfully saved.")

    except OSError as error:
        print("File saving error:", error)
