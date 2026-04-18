# File: hotel.py
# Author: Vasilissa Vilkki
# Description: Initialising hotel so that we can test the changes in the lighting settings

from control import ControlSystem, Area, Room, LightFixture

def create_hotel():
    control_system = ControlSystem()

    # Define areas of the hotel
    floor1 = Area("Floor 1")
    floor2 = Area("Floor 2")
    floor3 = Area("Floor 3")

    control_system.add_area(floor1)
    control_system.add_area(floor2)
    control_system.add_area(floor3)

    # Define rooms + categories
    # Floor 1
    lobby = Room("Lobby", floor1, ["lobby", "public"], 8)
    restaurant = Room("Restaurant", floor1, ["restaurant", "public"], 8)
    spa = Room("Spa", floor1, ["spa", "public"], 8)

    corridor_1a = Room("Corridor 1a", floor1, ["corridor", "public"], 8)

    # Floor 2
    room_201 = Room("201", floor2, ["guest", "basic"], 4)
    room_202 = Room("202", floor2, ["guest", "basic"], 4)
    room_203 = Room("203", floor2, ["guest", "basic"], 4)
    room_204 = Room("204", floor2, ["guest", "basic"], 4)

    corridor_2a = Room("Corridor 2a", floor2, ["corridor", "public"], 8)

    # Floor 3

    room_301 = Room("301", floor3, ["guest", "basic"], 4)
    room_302 = Room("302", floor3, ["guest", "basic"], 4)
    room_303 = Room("303", floor3, ["guest", "suite"], 6)
    room_304 = Room("304", floor3, ["guest", "suite"], 6)

    corridor_3a = Room("Corridor 3a", floor3, ["corridor", "public"], 8)

    # Add rooms to the control system
    for room in [floor1, floor2, floor3]:
        control_system.add_room(room)
