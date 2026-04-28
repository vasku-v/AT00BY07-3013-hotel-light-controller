# File: domain.py
# Author: Vasilissa Vilkki
# Description:  RoomLight hotel light controller domain model. 
#               Core operation logic and entities for the lighting control system.

from datetime import datetime

DEFAULT_BRIGHTNESS = 80
DEFAULT_TEMP = 4000

CATEGORIES = ["public", "corridor", "guest", "basic", "suite"]

# The domain model entities

class Area:
    # -- Represents a physical zone in the hotel
    def __init__(self, name: str):
        self.name = name
        self.rooms = []

class Room:
    # -- Represents an individual hotel room containing light fixtures 
    def __init__(self, name: str, area: object, categories: list, fixture_count: int):
        self.name = name
        self.categories = categories
        self.area = area
        self.fixtures = []

        # -- Generating a light fixture list
        for i in range(fixture_count):
            fixture_id = f"LF-{name}-{chr(65+ i )}" # Gives the fixture id in the form "RoomID-X" where X is a letter starting from A →
            self.fixtures.append(LightFixture(fixture_id, DEFAULT_BRIGHTNESS, DEFAULT_TEMP)) # When initializing fixtures in a room, the default brightess and temp values are set

class LightFixture:
    # -- Represents an individual light source
    def __init__(self, id: str, brightness: int, light_temp: int):
        self.id = id
        self.brightness = brightness
        self.light_temp = light_temp

# REQ-013 All lighting controls can be accessed by staff from a single unified view/system
# -- Centralized system to manage areas, rooms, and lighting schedules.
class ControlSystem:
    def __init__(self):
        self.areas = []
        self.scheduled_tasks = []

    # -- Avoiding two separate rooms lists
    @property
    def rooms(self):
        for area in self.areas:
            for room in area.rooms:
                yield room
    
    def add_area(self, area: object):
        self.areas.append(area)
    
    def add_room(self, room: object):
        # -- Adds a room to its designated area.
        # -- Check if the area is in control system before adding
        if (room.area not in self.areas):
            raise ValueError("Area must be added to Control system before adding room.")
        room.area.rooms.append(room)

    # --------------- CHANGING THE LIGHTING SETTINGS ---------------
    def _apply_setting_to_fixture(self, room: object, setting: str, value: int):
        # -- Internal helper to apply values to a room's light fixtures.
        for fixture in room.fixtures:
            if (setting == "brightness"):
                fixture.brightness = value
            elif (setting == "light_temp"):
                fixture.light_temp = value
    
    def set_brightness(self, target, value):
        self._set_value(target, "brightness", value)

    def set_light_temp(self, target, value):
        self._set_value(target, "light_temp", value)
    
    # -- target = area / room / category / the whole hotel -> what the setting is applied to
    # -- setting = brightness / light temperature
    # -- value = the numerical value applied to the setting
    def _set_value(self, target, setting: str, value: int):

        # REQ-001 The lighting scheme can be designed once and synced to every room through one control system.
        # -- The whole hotel
        if (target == "all"):
            for room in self.rooms:
                self._apply_setting_to_fixture(room, setting, value)
            return
        
        # -- Apply changes to rooms in a category
        if (target in CATEGORIES):
            for room in self.rooms:
                if (target in room.categories):
                    self._apply_setting_to_fixture(room, setting, value)
            return
        
        # -- Apply changes to rooms in an area
        if (isinstance(target, Area)):
            for room in target.rooms:
                self._apply_setting_to_fixture(room, setting, value)
            return
        
        # -- Apply changes to a room
        if (isinstance(target, Room)):
            self._apply_setting_to_fixture(target, setting, value)
            return
        
        raise ValueError("Unknown target type")
    
    # --------------- CHANGING THE LIGHTING SETTINGS END ---------------

    # --------------- SCHEDULE SETTING CHANGE ---------------
    def schedule_setting_change(self, sch_time, target, setting, value):
        # REQ-005 Lighting changes can be scheduled from the visual interface.
        task = {
            "time": sch_time,
            "target": target,
            "setting": setting,
            "value": value
        }
        self.scheduled_tasks.append(task)
    
    def run_scheduled_tasks(self):
        # -- Matches system time against the task list.
        now = datetime.now().strftime("%H:%M")

        tasks_to_run = []

        for task in self.scheduled_tasks:
            if (task["time"] == now):
                tasks_to_run.append(task)

        for task in tasks_to_run:
            self._set_value(task["target"], task["setting"], task["value"])
            self.scheduled_tasks.remove(task)
    
    def remove_scheduled_task(self, index):
        # -- Scheduled tasks can be removed
        if (0 <= index < len(self.scheduled_tasks)):
            self.scheduled_tasks.pop(index)
            return True
        return False
    
    # --------------- SCHEDULE SETTING CHANGE END ---------------
