# File: hotel.py
# Author: Vasilissa Vilkki
# Description: RoomLight hotel light controller hotel initialization. Sets uo the intitial
#              state for the RoomLight control system.

# CATEGORIES = ["public", "corridor", "guest", "basic", "suite"]

from domain import ControlSystem, Area, Room, CATEGORIES


# Factory function that creates the hotel lighting system.
def create_hotel() -> ControlSystem:
    control_system = ControlSystem()

    # -- Define areas of the hotel
    floor1 = Area("First floor")
    floor2 = Area("Second floor")
    floor3 = Area("Third floor")
    areas = [floor1, floor2, floor3]

    # Add areas to the control system
    for new_area in areas:
        control_system.add_area(new_area)
    
    # -- Define rooms
    # Floor 1
    lobby = Room("Lobby", floor1, [CATEGORIES[0]], 8)
    restaurant = Room("Restaurant", floor1, [CATEGORIES[0]], 10)
    spa = Room("Spa", floor1, [CATEGORIES[0]], 8)

    corridor1 = Room("Corridor 1", floor1, [CATEGORIES[0], CATEGORIES[1]], 6)

    # Floor 2
    room_201 = Room("Basic 201", floor2, [CATEGORIES[2], CATEGORIES[3]], 3)
    room_202 = Room("Basic 202", floor2, [CATEGORIES[2], CATEGORIES[3]], 3)
    room_203 = Room("Basic 203", floor2, [CATEGORIES[2], CATEGORIES[3]], 3)
    room_204 = Room("Basic 204", floor2, [CATEGORIES[2], CATEGORIES[3]], 3)

    corridor2 = Room("Corridor 2a", floor2, [CATEGORIES[0], CATEGORIES[1]], 6)

    # Floor 3
    room_301 = Room("Basic 301", floor3, [CATEGORIES[2], CATEGORIES[3]], 3)
    room_302 = Room("Basic 302", floor3, [CATEGORIES[2], CATEGORIES[3]], 3)
    room_303 = Room("Suite 303", floor3, [CATEGORIES[2], CATEGORIES[4]], 5)
    room_304 = Room("Suite 304", floor3, [CATEGORIES[2], CATEGORIES[4]], 5)

    corridor3 = Room("Corridor 3a", floor3, [CATEGORIES[0], CATEGORIES[1]], 6)

    # Add rooms to the control system
    rooms = [lobby, restaurant, spa, corridor1,
             room_201, room_202, room_203, room_204, corridor2,
             room_301, room_302, room_303, room_304, corridor3]
    
    for room in rooms:
        control_system.add_room(room)
    
    return control_system
