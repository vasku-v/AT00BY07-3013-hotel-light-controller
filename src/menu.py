# File: menu.py
# Author: Vasilissa Vilkki
# Description: Separate program for all the menu logic

# Helper function to reduce repetition
def ask_choice() -> int:
    choice = -1
    feed = input("\nYour choice: ")
    if (feed.isnumeric()):
        choice = int(feed)
    return choice

def area_menu():
    print("Area menu in progress")

def staff_menu():
    user_mode = 1
    choice = -1
    while (choice != 0):
        print("")
        print("                                 Staff Menu")
        print("")
        print("Instructions: If you want to make changes to a specific room/area choose number 1.")
        print("              If you want to make changes to areas/rooms of a specific type, such as")
        print("              suites or corridors, choose option 2.")
        print("              If you want to make changes to the whole hotel, choose option 3.")
        print("")
        print("                             1. Choose by area")
        print("                             2. Choose by category")
        print("                             3. Apply to the whole hotel")
        print("                             0. Back to main menu")
        choice = ask_choice()
        if (choice == 1):
            area_menu()
        elif (choice == 0):
            return
        else:
            print("Unknown option.")

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

        choice = ask_choice()

        # REQ-010 RoomLight's visual interface has different control panels for hotel staff and guests.
        if (choice == 1):
            staff_menu()
        elif (choice == 2):
            guest_menu()
        elif (choice == 0):
            print("Exiting the program...")
        else:
            print("Unknown option.")
