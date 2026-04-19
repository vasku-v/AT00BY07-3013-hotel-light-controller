# File: menu.py
# Author: Vasilissa Vilkki
# Description: Separate program for all the menu logic

import os
from hotel import create_hotel
from control import Room

# -- Create the shared hotel control system instance
control_system = create_hotel()

DEFAULT_TEMP = 4000
DEFAULT_BRIGHTNESS = 80

# -- Clear the screen for cleaner UI
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# -- Read the numeric menu choice from the user
def ask_choice() -> int:
    choice = -1
    feed = input("\nYour choice: ")
    if (feed.isnumeric()):
        choice = int(feed)
    return choice

# -- Print a centered title with decorative separators
def print_title(title: str):
    total_width = 70
    title = f" {title} "
    decoration_width = total_width - len(title)

    if decoration_width < 0:
        decoration_width = 0
    
    left = decoration_width // 2
    right = decoration_width - left

    print("\n" + "=" * left + title + "=" * right + "\n")

# -- Renders a menu with title, optional info text and numbered options
def show_menu(title: str, other: str, options: dict[int, str]):
    clear()
    print_title(title)
    if other != "":
        print(other)
    for key, option in options.items():
        print(f"                        {key}. {option}")

# REQ-005 Lighting changes can be scheduled from the visual interface
# -- Ask whether the user wants to apply a change now or schedule it for later
def ask_apply_or_schedule():
    print("\n1. Apply now")
    print("2. Schedule for later")
    feed = input("Choose: ")
    return feed

# -- Adjust brightness/temperature for any target (room, area, category, whole hotel)
def adjust_lighting(control_system, target, title, can_schedule: bool):
    options = {
        1: "Adjust brightness",
        2: "Adjust temperature",
        3: "Reset to default",
        0: "Back"
    }

    choice = -1
    while choice != 0:
        # -- Show current values only for a single room
        if isinstance(target, Room):
            b = target.fixtures[0].brightness
            t = target.fixtures[0].temperature
            other = f"{title} | Brightness: {b}% | Temp: {t}K\n"
        else:
            other = f"{title}\n"

        show_menu("Lighting Adjustment", other, options)
        choice = ask_choice()

        # -- Adjust BRIGHTNESS
        if choice == 1:
            feed = input("Enter brightness (10–100): ")
            if feed.isnumeric():
                value = int(feed)
                if 10 <= value <= 100:
                    
                    if can_schedule:
                        mode = ask_apply_or_schedule()
                        if mode == "1":
                            control_system.set_brightness(target, value)
                            print(f"\nBrightness updated to [{value} %]")
                        elif mode == "2":
                            time_str = input("Enter time (HH:MM): ")
                            control_system.schedule_change(time_str, target, "brightness", value)
                            print(f"Brightness scheduled for {time_str}")
                    else:
                        control_system.set_brightness(target, value)
                        print(f"\nBrightness updated to [{value} %]")
                else:
                    print("\nInvalid value. Must be between 10 and 100.")
            else:
                print("\nInvalid input. Please enter a number.")
            
            input("\nPress Enter to continue...")
        
        # -- Adjust TEMPERATURE
        elif choice == 2:
            feed = input("Enter temperature (2700–7000): ")
            if feed.isnumeric():
                value = int(feed)
                if 2700 <= value <= 7000:
                    
                    if can_schedule:
                        mode = ask_apply_or_schedule()
                        if mode == "1":
                            control_system.set_temperature(target, value)
                            print(f"\nTemperature updated to [{value} K]")
                        elif mode == "2":
                            time_str = input("Enter time (HH:MM): ")
                            control_system.schedule_change(time_str, target, "temperature", value)
                            print(f"Temperature scheduled for {time_str}")
                    else:
                        control_system.set_temperature(target, value)
                        print(f"\nTemperature updated to [{value} K]")
                else:
                    print("\nInvalid value. Must be between 2700 and 7000.")
            else:
                print("\nInvalid input. Please enter a number.")
            
            input("\nPress Enter to continue...")
        
        # -- Reset to default settings
        elif choice == 3:
            control_system.set_brightness(target, DEFAULT_BRIGHTNESS)
            control_system.set_temperature(target, DEFAULT_TEMP)
            print(f"\nBrightness set to {DEFAULT_BRIGHTNESS} % - Light temperature set to {DEFAULT_TEMP} K")
            input("\nPress Enter to continue...")

        elif choice == 0:
            return

# -- STAFF MENU LOGIC --
# REQ-013 All lighting controls can be accessed by staff from a single unified view
def staff_choose_by_room(control_system):
    clear()
    print_title("Choose Room")
    rooms = control_system.rooms

    for i, room in enumerate(rooms, start=1):
        print(f"{i}. {room.name}")

    feed = input("\nSelect room number: ")
    if not feed.isnumeric():
        return

    index = int(feed) - 1
    if not (0 <= index < len(rooms)):
        return

    room = rooms[index]
    adjust_lighting(control_system, room, f"Room: {room.name}", True)

# REQ-002 Different areas can be synced to different lighting schemes.
def staff_choose_by_area(control_system):
    clear()
    print_title("Choose Area")
    areas = control_system.areas

    for i, area in enumerate(areas, start=1):
        print(f"{i}. {area.name}")

    feed = input("\nSelect area number: ")
    if not feed.isnumeric():
        return

    index = int(feed) - 1
    if not (0 <= index < len(areas)):
        return

    area = areas[index]
    adjust_lighting(control_system, area, f"Area: {area.name}", True)

# -- Allow staff to adjust lighting for all rooms in a specific category
def staff_choose_by_category(control_system):
    clear()
    print_title("Choose Category")
    categories = sorted({cat for room in control_system.rooms for cat in room.categories})

    for i, cat in enumerate(categories, start=1):
        print(f"{i}. {cat}")

    feed = input("\nSelect category number: ")
    if not feed.isnumeric():
        return

    index = int(feed) - 1
    if not (0 <= index < len(categories)):
        return

    category = categories[index]
    adjust_lighting(control_system, category, f"Category: {category}", True)

# REQ-001 The lighting scheme can be designed once and synced to every room through one control system
def staff_apply_to_hotel(control_system):
    adjust_lighting(control_system, "all", "Whole Hotel", True)

# -- Show brightness and temperature for all rooms
def staff_see_lighting_setup(control_system):
    clear()
    print_title("Lighting Setup Overview")

    for room in control_system.rooms:
        b = room.fixtures[0].brightness
        t = room.fixtures[0].temperature
        print(f"{room.name:15} | Brightness: {b:3}% | Temp: {t}K")

    input("\nPress Enter to continue...")


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
                
                print(f"{i}. Scheduled Time: {task['time']} | Target: {target_name} | Adjusted setting: {task['attr']} | Value: {task['value']}")

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

# REQ-010 RoomLight's visual interface has different control panels for hotel staff and guests.
# REQ-013 All lighting controls can be accessed by staff from a single unified view
def staff_menu(control_system):
    options = {
        1: "Choose by room",
        2: "Choose by area",
        3: "Choose by category",
        4: "Apply to the whole hotel",
        5: "See lighting setup",
        6: "See and manage scheduled tasks",
        0: "Back to main menu"
    }

    choice = -1
    while choice != 0:
        show_menu("RoomLight - Staff Menu", "", options)
        choice = ask_choice()

        if choice == 1:
            staff_choose_by_room(control_system)
        elif choice == 2:
            staff_choose_by_area(control_system)
        elif choice == 3:
            staff_choose_by_category(control_system)
        elif choice == 4:
            staff_apply_to_hotel(control_system)
        elif choice == 5:
            staff_see_lighting_setup(control_system)
        elif (choice == 6):
            staff_see_and_manage_tasks(control_system)
        elif choice == 0:
            return

# REQ-010 RoomLight's visual interface has different control panels for hotel staff and guests.
def guest_menu(control_system):
    room = control_system.get_room_by_name("Basic 202")
    if room:
        # Same function as for staff view, but scheduling feature has been removed 
        adjust_lighting(control_system, room, f"Guest Room: {room.name}", False)
    else:
        print("Room not found.")
        input("\nPress Enter to continue...")

# -- Main entry point to the RoomLight control system
# -- Staff view or guest view can be chosen for the sake of simulation, in reality would be more separated
def main_menu():
    options = {
        1: "Staff menu",
        2: "Guest menu",
        0: "Exit"
    }
    
    choice = -1
    while (choice != 0):
        # -- Execute scheduled tasks
        control_system.run_scheduled_tasks()
        show_menu("Welcome to RoomLight Main Menu", "", options)
        choice = ask_choice()

        if (choice == 1):
            staff_menu(control_system)
        elif (choice == 2):
            guest_menu(control_system)
        elif (choice == 0):
            print("Exiting the program...")
        else:
            print("Unknown option.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main_menu()
