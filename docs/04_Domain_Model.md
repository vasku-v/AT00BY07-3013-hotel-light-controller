# RoomLight Domain Model

Below is a written list of the central domain concepts, and their relationships
to each other.

### Hotel

The environment where the lighting system operates.

→ A hotel _has many_ **areas**  
→ A hotel _has many_ **rooms**  
→ A hotel _is controlled_ through **Staff UI**  
→ A hotel _can have_ a general **lighting scheme** applied

### Area

A grouping of rooms, such as floor or a suite category. Areas can have their own
lighting configuration that differs from the rest of the hotel.

→ An area _contains many_ **rooms**  
→ An area _is controlled_ through **Staff UI**  
→ An area _can have_ a **lighting scheme** applied

### Room

Each room can have the general lighting settings of the hotel or the area it
belongs to, or have its own configuration. Guest rooms reset to default lighting
between guests.

→ A room _belongs_ to an **area**  
→ A room _has many_ **light fixtures**  
→ A room _is controlled_ through **Guest UI** or **Staff UI**  
→ A room _can have_ a **lighting scheme** applied

### Light Fixture

A physical light unit that is installed in a room or an area, that supports
adjustable properties such as brightness and color temperature.

→ A light fixture _belongs to_ a **room** or an **area**  
→ A light fuxture _supports_ changes in **brightness** and **temperature**  
→ A light fixture _is controlled_ by the **control system**

### Control System

The central system that controls and automatically applies all lighting accross
the hotel. Provides separate interfaces for staff and guests. Handles
synchronization, scheduling and configuration.

→ The control system _provides_ **staff UI**  
→ The control system _provides_ **guest UI**  
→ The control system _manages_ **lighting schemes**  
→ The control system _manages_ **schedules**

### Staff UI

A unified interface that provides full control over all rooms and areas. Allows
to apply lighting schemes and settings, scheduling changes, as well as to
monitor the lighting of the entire hotel.

→ Staff UI _is part of_ the **control system**  
→ Staff UI _is used_ to set lighting changes in **rooms**, **areas** and the
**hotel**

### Guest UI

A simplified interface for the room-level adjustments.

→ Guest UI _is part of_ the **control system**  
→ Guest UI is _is used_ to set lighting changes in guest **rooms**

### Lighting Scheme

A reusable configuration that defines brightness and color temperature. Can be
customized through the staff UI. Schemes can be applied to individual rooms,
different areas or across the hotel.

→ A lighting scheme _can be applied_ to **rooms**, **areas** and the **hotel**  
→ A lighting scheme _can be configured_ through **staff UI** and **guest UI**  
→ A lighting scheme _can be triggered_ by a **schedule**

### Schedule

A timed feature that allows for light changes at specific moments. Used for
dimming and preparing rooms for events.

→ A schedule _modifies_ a **lighting scheme**  
→ A schdule _can be set_ through the **staff UI**  
→ A schedule _is executed by_ a **control system**

### Automatic Light

Automatic behavior that resets the guest room lighting between guests.

→ Automatic light _affects_ **rooms** and **light fixtures**  
→ Automatic light _is managed by_ the **control system**

### Brigthness

A property of a lighting scheme that defines light intensity.

→ Brightness _is configured_ in **lighting scheme**  
→ Brigthness _is controlled_ through **guest UI** or **staff UI**

### Light Temperature

A property of a lighting scheme that defines the warmth or coolness of the
light.

→ Light temperature _is configured_ in **lighting scheme**  
→ Light temperature _is controlled_ through **guest UI** or **staff UI**
