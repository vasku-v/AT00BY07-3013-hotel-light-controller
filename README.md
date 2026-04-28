# RoomLight Hotel Light Controller - Project Overview

## Vision Statement

#### _A hotel room light controller - design the lighting once, sync to every room._

## Project Description

**RoomLight** is a CLI-based prototype for a centralized hotel lighting control
system. The program's core idea is to eliminate repetitive manual work by
establishing a single control point for lighting configuration.

In this implementation, **brightness** and **light color temperature** are
managed through a hierarchical domain model. Instead of adjusting individual
fixtures, the system allows for mass-synchronization across the entire hotel, an
area and room categories.

The system features two distinct interfaces, a **staff menu** for comrehensive
hotel management and a rextricted **guest menu** for individual room control.
Data persistence is handled through JSON, ensuring that the data is preserved
when restarting the system.

## The Why

1. Operational efficiency: Managing dozens or even hundreds of rooms manually is
   cost-prohibitive. RoomLight enables hotel staff to update the entire
   building's lighting within seconds.

2. Brand integrity: Automation ensures that every "Suite" or "Lobby" maintains a
   consistent lighting profile, that is in line with the brand standards.

3. Role-based control: The system provides staff with control over the entire
   hotel while giving guests a private interface to manage their own room's
   lighting.

## Requirements

REQ-001 The lighting scheme can be designed once and synced to every room
through one control system.

- _Status: Fully implemented_. The system uses a centralized `ControlSystem` to
  push changes to all registered rooms simultaneously.

REQ-002 Different areas can be synced to different lighting schemes.

- _Status: Fully implemented_. Rooms include _Area_ and _Categories_ metadata,
  allowing the system to apply setting changes to specified functional groups.

REQ-005 Lighting changes can be scheduled from the visual interface.

- _Status: Partially implemented_. Individual tasks can be scheduled within the
  current session. Persistent task storage and recurring schedules (e.g., daily
  cycles) are currently out of scope.

REQ-010 RoomLight's visual interface has different control panels for hotel
staff and guests.

- _Status: Fully implemented_. Clear separation between administrative (staff)
  and individual user (guest) access levels.

REQ-013 All lighting controls can be accessed by staff from a single unified
view

- _Status: Fully implemented_. The staff interface provides a real-time overview
  of the whole hotel lighting configuration as well as a unified command hub to
  manage all scopes (Room, Area, Category, All) from a single menu.

## Architecture and SW Design overview

The RoomLight system follows a modular design where tasks have been divided
between thee distinct main layers: **domain logic**, **user interface** and
**data management**. This separation ensures that the core domain logic is
independent from how the data is displayed and stored.

#### Hiererchical domain model (domain.py)

The system's core is built using OOP (Object-oriented programming). It utilizes
a hierarchical structure which mirrors a physical hotel environment.

**HIERACHY**

- `ControlSystem` manages `Area` and `Room` objects. Serves as the single point
  of entry for global commands.
- `Area`: A logical grouping of `Room` instances that mirrors the hotel area
  structure.
- `Room` includes metadata such as `Area` and `Category` it belongs to as well
  as the lighting hardware.
- `LighFixture` the lowest level of hierarchy representing the lighting
  hardware. Store the brightness and light color temperature values.

All lighting configuration, synchronization and scheduling happens through the
`ControlSystem`. As the domain layer is completely independent from the user
interface, it is scalable and can be unit-tested quite easily.

#### Procedural UI (menu.py)

The UI layer of the software has been implemented procedurally. The decision was
based on the need for a linear, menu-style CLI. The design decision allows the
system to provide a clear execution path to the user.

The UI layer's responsibility is to handle user input, visualize the hotel
state, and trigger the appropriate methods in the domain layer.

#### Data and Persistence (data.py & hotel.py)

The initial state of the hotel is configured through hotel.py. The initial
states of the rooms, areas and light fixtures are generated if no previously
saved data has been detected.

Data.py is responsible for saving the lighting configurations in JSON-format. By
saving and loading configurations, the system ensures data persistence accross
sessions.

## Test plan

#### Scope

Core requirements verification

- Syncing, scheduling and role-based access

Data integrity:

- Ensuring the lighting configuration persist between sessions

Input validation:

- Handling incorrect menu choices and value ranges (e.g., 10-100)

#### Phase 1: Manual system testing

- Environment: Terminal (Windows), Python 3.10+
- Method: Execute main.py, navigate through staff/guest menus, make changes to
  lighting settings, verify results visually

#### Phase 2: Automated testing

- Tool: pytest
- Method: Unit tests for domain.py and data.py to ensure that the core logic of
  the program works without the visual interface

**Examples:**

- test_room_initialization → verify `LightFixture` objects are generated with
  correct IDs and default values (80 % brightness, 4000 K light color
  temperature)
- test_add_room_validation → ensure `ValueError` is raised if `Room` is added to
  the `ControlSystem` without its `Area` being defined first
- test_category_setting_change → Apply a setting to the "public" category and
  assert that only rooms containing "public" in their category list are updated
- test_scheduler_logic → Assert that calling `schedule_setting_change()` appends
  correctly formatted dictionaries to the `scheduled_tasks` list
