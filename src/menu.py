# File: menu.py
# Author: Vasilissa Vilkki
# Description: RoomLight hotel light controller menu interface. Provides separate control panels for staff 
#              and guests allowing for user interaction.

import os
from domain import CATEGORIES, Room

# CATEGORIES = ["public", "corridor", "guest", "basic", "suite"]

# ANSI colors for UI clarity
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[0;31m"
RESET = "\033[0m"

DECORATOR = "="
TOTAL_WIDTH = 100

DEFAULT_TEMP = 4000
DEFAULT_BRIGHTNESS = 80

# --------------- GENERAL MENU CONFIGURATION ---------------

# -- Clear the screen for cleaner UI
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# -- Read and validate user input
def ask_choice() -> int:
    choice = -1
    feed = input("\n> ")
    if (feed.isnumeric()):
        choice = int(feed)
    return choice

# -- Breaks the program execution and waits for user to press enter
def enter_to_continue():
    print("")
    input("Press Enter to continue...")

# -- Renders standardized menu layout eith title, info text and options
def show_menu(title: str, info: str, options, adjuster: int):
    clear()
    print_title(title)
    print_info(info)
    print_options(options, adjuster)

# -- Print a centered, decorated title
def print_title(title: str):
    title = f" {title} "
    dec_width = TOTAL_WIDTH - len(title)

    if (dec_width < 0):
        dec_width = 0
    
    left = dec_width // 2
    right = dec_width - left

    print("")
    print(DECORATOR * left + title + DECORATOR * right)
    print("")

# -- Print centered menu options
def print_options(options, adjuster: int):
    # -- Supports flat and grouped dictionaries

    # -- Check if grouped
    grouped = True

    for v in options.values():
        if not isinstance(v, dict):
            grouped = False
            break

    # -- Calculate alignment based on longest option string
    max_len = 0
    if (grouped):
        for group in options.values():
            for text in group.values():
                length = len(text)
                if (length > max_len):
                    max_len = length
    else:
        for text in options.values():
            length = len(text)
            if (length > max_len):
                max_len = length
    
    left = (TOTAL_WIDTH - max_len) // 2 + adjuster

    if (grouped):
        for group_name, group_items in options.items():
            # Print group title
            title = f"--- {group_name} ---\n"
            print("\n" + " " * left + title)

            for key, option in group_items.items():
                line = f"{key}. {option}"
                print(" " * left + line)
    else:
        for key, option in options.items():
            line = f"{key}. {option}"
            print(" " * left + line)

# -- Print centered, highlighted info text
def print_info(info: str):
    # Use ANSI color for emphasis
    colored_text = YELLOW + info + RESET

    dec_width = TOTAL_WIDTH - len(info)

    if (dec_width < 0):
        dec_width = 0
    
    left = dec_width // 2

    print("")
    print(" " * left + colored_text)
    print("")

# --------------- GENERAL MENU CONFIGURATION END ---------------

# --------------- LIGHT SETTING CHANGES ---------------

def adjust_lighting(control_system, target, title, can_schedule: bool):
    options = {
        1: "Adjust Brightness (0-100 %)",
        2: "Adjust Light Temperature (2700-7000 K)",
        3: "Reset to Default",
        0: "Back"
    }

    choice = -1

    while (choice != 0):
        # -- Show lighting settings if the target is a specific room
        if (isinstance(target, Room)):
            # -- Expecting all light fixtures in a room to share settings
            fixture = target.fixtures[0]
            info = f"{title} | Current settings: {fixture.brightness} % | {fixture.light_temp} K"
        else:
            info = f"{title} | Adjust lighting settings for all rooms in this selection"
        
        show_menu("Lighting Adjustment", info, options, 0)
        choice = ask_choice()

        # -- Go through adjust lighting options
        if (choice == 1):
            feed = ask_brightness()
            if (feed.isnumeric()):
                value = int(feed)
                if (0 <= value <= 100):
                    if (can_schedule):
                        ask_schedule(control_system, value, "brightness", target)
                    else:
                        control_system.set_brightness(target, value)
                        print(f"Brightness updated to {value} %")
        elif (choice == 2):
            feed = ask_light_temp()
            if (feed.isnumeric()):
                value = int(feed)
                if (2700 <= value <= 7000):
                    if (can_schedule):
                        ask_schedule(control_system, value, "light temperature", target)
                    else:
                        control_system.set_light_temp(target, value)
                        print(f"Light temperature updated to {value} K")
        elif (choice == 3):
            control_system.set_brightness(target, DEFAULT_BRIGHTNESS)
            control_system.set_light_temp(target, DEFAULT_TEMP)
            print("\nBrightness set to 80 % | Light temperature set to 4000 K")
        elif (choice == 0):
            return
        else:
            print("")
            print("Unknown option.")
        enter_to_continue()

# -- Formatting 
def ask_brightness():
    print("")
    print(CYAN + "Adjust Brightness" + RESET)
    print(YELLOW + "Enter a value between 0 and 100 %")
    feed = input("> ")
    print(RESET)
    return feed

# -- Formatting
def ask_light_temp():
    print("")
    print(CYAN + "Adjust Light Temperature" + RESET)
    print(YELLOW + "Enter a value between 2700 and 7000 K")
    feed = input("> ")
    print(RESET)
    return feed

# --------------- LIGHT SETTING CHANGES END ---------------

# --------------- SCHEDULE ---------------

# REQ-005 Lighting changes can be scheduled from the visual interface.
def ask_schedule(control_system, value, setting, target):
    print("1. Apply now")
    print("2. Schedule for later")
    choice = ask_choice()

    if (choice == 1 ):
        if (setting == "brightness"):
            control_system.set_brightness(target, value)
            print(f"\nBrightness updated to {value} %")
        elif (setting == "light temperature"):
            control_system.set_light_temp(target, value)
            print(f"\nLight temperature updated to {value} K")
    elif (choice == 2):
        time = input("Enter time (HH:MM): ")
        control_system.schedule_setting_change(time, target, setting, value)
        print(f"You have scheduled [{setting}] change for {time}")

# -- See all scheduled tasks and remove them if necessary
def staff_see_and_manage_tasks(control_system):
    while True:
        clear()
        print_title("Scheduled Tasks Overview")

        tasks = control_system.scheduled_tasks

        if (len(tasks) == 0):
            print("No tasks scheduled at the moment.")
            input("\nPress Enter to continue...")
            return

        else:
            for i, task in enumerate(tasks, start=1):
                # -- Which target scheduled task is scheduled to
                target = task["target"]
                if (target == "all"):
                    target_name = "Whole Hotel"
                elif isinstance(target, str):
                    target_name = f"Category: {target}"
                else:
                    target_name = target.name # -- Both Rooms and Areas can be accessed through this
                
                print(f"{i}. Scheduled Time: {task['time']} | Target: {target_name} | Adjusted setting: {task['setting']} | Value: {task['value']}")

            print("\n0. Return to menu")
            print("1. Remove a scheduled task")

            choice = ask_choice()

            if (choice == 1):
                feed = input("\nEnter task number to remove: ")
                if feed.isnumeric():
                    index = int(feed) - 1
                    if (control_system.remove_scheduled_task(index)):
                        print("\nTask removed successfully.")
                    else:
                        print("\nUnknown task number.")
                else:
                    print("\nUnknown input.")
                input("\nPress Enter to continue...")
            elif (choice == 0):
                return
            else:
                print("\nUnknown option.")
                input("\nPress Enter to continue...")

# --------------- SCHEDULE END ---------------

# --------------- STAFF MENU CONFIGURATION ---------------

# REQ-002 Different areas can be synced to different lighting schemes.
def staff_choose_by_room(control_system):
    while True:
        clear()
        title = "Choose Room"

        # -- Get the rooms and change into a list
        rooms_list = list(control_system.rooms)

        # -- Print out an enumerated list of the rooms
        options = {}
        for i, room in enumerate(rooms_list, start=1):
            options[i] = room.name
        options[0] = "Cancel"

        info = "Select a specific room and adjust its lighting settings individually."
        show_menu(title, info, options, 0)

        choice = ask_choice()

        # -- Check that the choice is within bounds
        if (1 <= choice <= len(rooms_list)):
            target_room = rooms_list[choice - 1]
            adjust_lighting(control_system, target_room, f"Room - {target_room.name}", True)
            return
        elif (choice == 0):
            return
        else:
            print(RED + "Room not found." + RESET)
            enter_to_continue()

def staff_choose_by_area(control_system):
    while True:
        clear()
        title = "Choose Area"

        areas = control_system.areas

        options = {}
        for i, area in enumerate(areas, start=1):
            options[i] = area.name
        options[0] = "Cancel"

        info = "Change and sync up lighting settings for an entire area of the hotel."

        show_menu(title, info, options, 0)

        choice = ask_choice()
        if (1 <= choice <= len(areas)):
            target_area = areas[choice - 1]
            adjust_lighting(control_system, target_area, f"Area - {target_area.name}", True)
        elif (choice == 0):
            return
        else:
            print(RED + "Area not found." + RESET)
            enter_to_continue()

def staff_choose_by_category(control_system):
    clear()
    title = "Choose by Category"

    categories = CATEGORIES

    options = {}
    for i, category in enumerate(categories, start=1):
        options[i] = category
    
    options[0] = "Cancel"
    show_menu(title, "", options, 0)

    choice = ask_choice()
    if (1 <= choice <= len(categories)):
        target_category = categories[choice - 1]
        adjust_lighting(control_system, target_category, f"Category - {target_category}", True)
    elif (choice == 0):
        return
    else:
        print("Category not found.")
    enter_to_continue()

#REQ-001 The lighting scheme can be designed once and synced to every room through one control system.
def staff_apply_to_all(control_system):
    adjust_lighting(control_system, "all", "Change lighting setup to the whole hotel", True)

def staff_see_lighting_setup(control_system):
    clear()
    print_title("Lighting Setup Overview")

    for room in control_system.rooms:
        b = room.fixtures[0].brightness
        t = room.fixtures[0].light_temp
        print(f"{room.name:15} |  Brightness: {b:5} %  |  Light temperature: {t:5} K")
    
    enter_to_continue()

# --------------- STAFF MENU CONFIGURATION END ---------------


# --------------- MENUS -----------------
# REQ-010 RoomLight's visual interface has different control panels for hotel staff and guests.
def staff_menu(control_system):
    options = {
        "Control Scope": {
            1: "Choose by Room",
            2: "Choose by Area",
            3: "Choose by Category",
            4: "Apply Setting to All",
        },
        "Tools & Overview": {
            5: "See Lighting Setup",
            6: "See and Manage Scheduled Tasks",
        },
        "Navigation": {
            0: "Back to Main Menu"
        }
    }

    adjuster = 4

    info = "Choose how you want to manage the hotel lighting:"
    
    choice = -1 
    while (choice != 0):
        show_menu("RoomLight - Staff Menu", info, options, adjuster)
        choice = ask_choice()

        if (choice == 1):
            staff_choose_by_room(control_system)
        elif (choice == 2):
            staff_choose_by_area(control_system)
        elif (choice == 3):
            staff_choose_by_category(control_system)
        elif (choice == 4):
            staff_apply_to_all(control_system)
        elif (choice == 5):
            staff_see_lighting_setup(control_system)
        elif (choice == 6):
            staff_see_and_manage_tasks(control_system)
        elif (choice == 0):
            return
        else:
            print("")
            print("Unknown option.")
            enter_to_continue()

# REQ-010 RoomLight's visual interface has different control panels for hotel staff and guests.
def guest_menu(control_system):
    room_name = "Basic 202"

    for room in control_system.rooms:
        if (room.name == room_name):
            adjust_lighting(control_system, room, f"Guest Room - {room.name}", False)

def main_menu(control_system):
    options = {
        1: "Staff menu",
        2: "Guest menu",
        0: "Exit"
    }

    info = "                                   Manage hotel lighting settings.\n"
    info += "\n                 Staff menu - Full access to all lighting controls and scheduling tools"
    info += "\n                 Guest menu - Adjust lighting for your assigned room\n"

    adjuster = -5
    choice = -1
    while (choice != 0):
        # Execute scheduled tasks
        control_system.run_scheduled_tasks()
        show_menu("Welcome to RoomLight main menu", info, options, adjuster)
        choice = ask_choice()

        if (choice == 1):
            staff_menu(control_system)
        elif (choice == 2):
            guest_menu(control_system)
        elif (choice == 0):
            print("Exiting the program.")
        else:
            print("Unknown option.")
            enter_to_continue()

# -------------- MENUS END --------------------
