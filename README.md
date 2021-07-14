# homeassistant-doorman

Major rewrite of https://github.com/espenfjo/homeassistant-doorman


Home assistant addon
Custom component for the Yale Doorman lock(s) via the Yale Smart HUB.

Supports:
 * Reading current state
 * Reading past state via the report API (Same as the history in the app)
 * Lock

Unsupported:
 * Unlock is integrated but pincode need to be sent as a kwarg "code" to the unlock function for it to work, support for function needs to be integrated into home assistant


Tested with the V2N lock.

## Installation

Place the `custom_components` folder in your Home Assistant configuration folder.

add the following to configuration.yaml

```
lock:
  - platform: doorman
    username: 'xxxx@xxx.com'
    password: 'xxxxxxxxxxxx'
```
