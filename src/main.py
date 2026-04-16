# File: main.py
# Author: Vasilissa Vilkki
# Description: RoomLight demo main program.

from menu import main_menu

def get_brightness(user_mode) -> int:
    # Staff user mode
    if (user_mode == 1):
        while (True):
            print("")
            print("             Set brightness - Staff view")
            print("")
            print("Instructions: Set the brightness on the scale of 1-100 %.")
            print("")
            feed = input("Brightness (1-100): ")
            if (feed.isnumeric()):
                brightness = int(feed)
                if (brightness >= 1 and brightness <= 100):
                    confirm = input(f"Confirm setting the brightness to {brightness} %. Press y/n: ")
                    if (confirm.lower() == "y"):
                        return brightness
                    elif (confirm.lower() == "n"):
                        break
                    else:
                        print("Unknown option.")
                else:
                    print("Input out of range (1-100)")
            else:
                print("Please type in a numerical value in the range 1-100.")
            
    # Guest user mode
    elif (user_mode == 2):
        print("Guest mode in progress.")

def set_brightness():
    print("In progress")

def main():
    main_menu()
    return None

if __name__ == "__main__":
    main()
