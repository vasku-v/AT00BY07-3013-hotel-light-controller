# File: data.py
# Author: Vasilissa Vilkki
# Description: Storing the hotel lighting setup data in json form.

import json
from domain import Room, Area, CATEGORIES, ControlSystem

ROOMS_FILE = "room.json"
SCHEDULED_TASKS_FILE = "scheduled_tasks.json"

def save_rooms_to_json(control_system):
    data = {"rooms": []}

    for room in control_system.rooms:
        fixture = room.fixtures[0]

        data["rooms"].append({
            "name": room.name,
            "area": room.area.name,
            "categories": room.categories,
            "fixture_count": len(room.fixtures),
            "brightness": fixture.brightness,
            "light_temp": fixture.light_temp
        })
    
    with open(ROOMS_FILE, "w") as file:
        json.dump(data, file, indent=4)

def load_rooms_from_json():
    try:
        with open(ROOMS_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        return None
    
    # -- Create Area objects from data
    area_objects = {}
    for room_data in data["rooms"]:
        area_name = room_data["area"]
        if (area_name not in area_objects):
            area_objects[area_name] = Area(area_name)
    
    # -- Create control system and add Areas
    control_system = ControlSystem()
    for area in area_objects.values():
        control_system.add_area(area)
    
    # -- Create Room object from data
    for r in data["rooms"]:
        area = area_objects[r["area"]]

        room = Room(
            r["name"],
            area,
            r["categories"],
            r["fixture_count"]
        )

        # -- Apply saved settings
        room.fixtures[0].brightness = r["brightness"]
        room.fixtures[0].light_temp = r["light_temp"]

        control_system.add_room(room)
    
    return control_system

def find_room_by_name(control_system, name):
    for room in control_system.rooms:
        if room.name == name:
            return room
    return None
