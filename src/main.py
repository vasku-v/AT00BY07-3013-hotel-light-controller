# File: main.py
# Author: Vasilissa Vilkki
# Description: RoomLight demo main program

from menu import main_menu
from data import load_rooms_from_json, save_rooms_to_json
from hotel import create_hotel

def main():
    control_system = load_rooms_from_json()

    if (control_system is None):
        control_system = create_hotel()

    main_menu(control_system)

    save_rooms_to_json(control_system)
    return None

if __name__ == "__main__":
    main()
