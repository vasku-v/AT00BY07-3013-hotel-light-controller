# File: main.py
# Author: Vasilissa Vilkki
# Description: RoomLight demo main program.

# Helper function to reduce repetition
def ask_choice() -> int:
    choice = -1
    feed = input("\nYour choice: ")
    if (feed.isnumeric()):
        choice = int(feed)
    return choice


def staff_menu():
    choice = -1
    while (choice != 0):
        print("")
        print("                     Staff Menu")
        print("")
        print("")
        print("                 0. Back to main menu")
        choice = ask_choice()
        if (choice == 0):
            return

def guest_menu():
    choice = -1
    while (choice != 0):
        print("")
        print("                     Guest Menu")
        print("")
        print("")
        print("                 0. Back to main menu")

        choice = ask_choice()

        if (choice == 0):
            return

# Menu to choose between staff and guest view 
# The option would not be available in real life scenario - implemented here just to show the difference between the two
def main_menu():
    choice = -1
    while (choice != 0):
        print("")
        print("         Welcome to RoomLight main menu")
        print("")
        print("     Choose (1) staff view or (2) guest view.")
        print("                 Press 0 to exit.")
        print("")
        print("                 1. Staff menu")
        print("                 2. Guest menu")
        print("                 0. Exit")

        feed = input("\nYour choice: ")
        if (feed.isnumeric()):
            choice = int(feed)

        # REQ-010 RoomLight's visual interface has different control panels for hotel staff and guests.
        if (choice == 1):
            staff_menu()
        elif (choice == 2):
            guest_menu()
        elif (choice == 0):
            print("Exiting the program...")
        else:
            print("Unknown choice.")


def main():
    main_menu()
    return None

if __name__ == "__main__":
    main()
