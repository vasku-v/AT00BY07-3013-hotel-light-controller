# File: components.py
# Author: Vasilissa Vilkki
# Description: Classes for lighting scheme adjustments

# physical location a room belongs to
class Area:
    def __init__(self, name: str, categories: list):
        self.name = name
        self.rooms = []

# individual rooms wthin an area
class Room:
    def __init__(self, name: str, area: object, categories: list, fixture_count: int):
        self.name = name
        self.area = area
        self.categories = categories
        self.fixtures = []
        self.scheme = None

        # Generating a light fixture list
        for i in range(fixture_count):
            fixture_id = f"{name}-{chr(65 + i)}"
            self.fixtures.append(LightFixture(fixture_id, 80, 4000))

# light fixtures whose brightness and temp is changed
class LightFixture:
    def __init__(self, id, brightness, temperature):
        self.id = id
        self.brightness = brightness
        self.temperature = temperature

# ready-to-go presets through which quick changes to the lighting can be applied
class Preset:
    def __init__(self, name, brightness, temperature):
        self.name = name
        self.brightness = brightness
        self.temperature = temperature

# control system through which all the changes are made
class ControlSystem:
    def __init__(self):
        self.areas = []
        self.rooms = []
        self.schemes = []
    
    def add_area(self, area: object):
        self.areas.append(area)
    
    def add_room(self, room: object):
        self.rooms.append(room)
        room.area.rooms.append(room)

    # Helper function to avoid repetition when setting the brightness or the temperature of the light
    def _change_light_setting(self, room, attr, value):
        for fixture in room.fixtures:
            setattr(fixture, attr, value)
    
    # Public API
    def set_brightness(self, target, value):
        self._set_value(target, "brightness", value)
    
    def set_temperature(self, target, value):
        self._set_temperature(target, "temperature", value)
    
    # Core brightness and temperature setting logic
    def _set_value(self, target, attr, value):

        # The whole hotel
        if (target == "all"):
            for room in self.rooms:
                self._change_light_setting(room, attr, value)
            return
        
        # A single room
        if isinstance(target, Room):
            self._change_light_setting(target, attr, value)
        
        # A specific area
        if isinstance(target, Area):
            for room in target.rooms:
                self._change_light_setting(room, attr, value)
            return
        
        # A specific category of rooms
        if isinstance(target, str):
            for room in self.rooms:
                if (target in room.categories):
                    self._change_light_setting(room, attr, value)
            return
        
        raise ValueError("Unknown target type")
