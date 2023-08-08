---
title: Creating a custom component for home assistant
slug: creating-a-custom-component-for-homeassistant
date: 2020-08-18T21:25:17.000Z
draft: false
featured: false
image: "images/cover.png"
tags:
    - Diy
    - Homelab
authors:
    - samuel
---

So after building a reliable enough software for my open433 board, I wanted to make add my project as a platform for home assistant. 

<!--more-->

So after building a reliable enough software for my open433 board, I wanted to make add my project as a platform for home assistant. However, I found official documentation by homeassistant.io very shitty when you don't know the inner workings of the platform so here's my take on it:

To create a home assistant component you need to create a folder named custom_components folder in the home assistant configuration directory (same one as the configuration.yaml) then in this older you need to create a folder with the name of your integration.

In this folder create a file name manifest.json this is where we will be declaring information about you integration:

```json
{
  "domain": "open433",
  "name": "Open433 board",
  "documentation": "https://github.com/TheStaticTurtle/Open433",
  "requirements": ["pyserial==3.4"],
  "codeowners": ["@TheStaticTurtle"]
}
```

In here you specify the domain of your integration then the description the documentation of the project the requirements needed by you program (in my case pyserial) and then the GitHub usernames of who made the code

Then in the same folder create a file named __init__.py in this file you will need to declare the configuration needed by your integration. So first import some constants / libraries:

```py
import logging
from homeassistant.const import EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
import threading
from . import rcswitch
```

in my case I have the library that I made in the same folder (named rcswitch.py). Then you need to declare some stuff like the domain (the name of your integration) , the name of the parameters used by the configuration and finally the configuration schema:

```py
_LOGGER = logging.getLogger(__name__)

DOMAIN = "open433"

CONF_COMPORT = "port"
CONF_COMSPEED = "speed"

REQ_LOCK = threading.Lock()
CONFIG_SCHEMA = vol.Schema(
	{
		DOMAIN: vol.Schema({
			vol.Required(CONF_COMPORT): cv.string,
			vol.Optional(CONF_COMSPEED, default=9600): cv.positive_int,
		})
	},
	extra=vol.ALLOW_EXTRA,
)
```

So for me the configuration could look like this:

```yaml
open433:
  port: COM3
```

That's it for declaring the constants now you need to declare the actual setup function my one looks like this:

```python
def setup(hass, config):
	conf = config[DOMAIN]
	comport = conf.get(CONF_COMPORT)
	comspeed = conf.get(CONF_COMSPEED)

	rf = rcswitch.RCSwitch(comport, speed=comspeed)
	rf.libWaitForAck(True, timeout=1)

	def cleanup(event):
		rf.cleanup()

	def prepare(event):
		rf.prepare()
		rf.startReceivingThread()
		hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, cleanup)

	hass.bus.listen_once(EVENT_HOMEASSISTANT_START, prepare)
	hass.data[DOMAIN] = rf

	return True
```

To break it down first we get the configuration from home assistant config for the current domain (line 2) then we retrieve the config (line3-4). Then specific to me I initialize my library (line6-7) then we define function for home assistant to execute while it start stops (line9-17) and then I store the instance of my library into home assistant data for the specific domain.

And that all for the `__init__.py`

After all this you need to add the component for the platform as my project controls ac rf switches I wanted to make a switch component, to do that simply create a switch.py in the same folder

```python
import logging

import voluptuous as vol

from homeassistant.components.switch import SwitchEntity, PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME, CONF_SWITCHES
import homeassistant.helpers.config_validation as cv
from . import DOMAIN, REQ_LOCK, rcswitch

_LOGGER = logging.getLogger(__name__)

CONF_CODE_OFF = "code_off"
CONF_CODE_ON = "code_on"
CONF_PROTOCOL = "protocol"
CONF_LENGTH = "length"
CONF_SIGNAL_REPETITIONS = "signal_repetitions"
CONF_ENABLE_RECEIVE = "enable_receive"

SWITCH_SCHEMA = vol.Schema(
	{
		vol.Required(CONF_CODE_OFF): vol.All(cv.ensure_list_csv, [cv.positive_int]),
		vol.Required(CONF_CODE_ON): vol.All(cv.ensure_list_csv, [cv.positive_int]),
		vol.Optional(CONF_LENGTH, default=32): cv.positive_int,
		vol.Optional(CONF_SIGNAL_REPETITIONS, default=15): cv.positive_int,
		vol.Optional(CONF_PROTOCOL, default=2): cv.positive_int,
		vol.Optional(CONF_ENABLE_RECEIVE, default=False): cv.boolean,
	}
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
	{
		vol.Required(CONF_SWITCHES): vol.Schema({cv.string: SWITCH_SCHEMA}),
	}
)
```

The start is very similar to the init file you import everything and define what the configuration will look like. This what my configuration looks like (the two first line are home assistant specific)

```yaml
switch:
  - platform: open433
    switches:
      switchA:
        code_on: 2389577216
        code_off: 2171473408
        protocol: 2
        length: 32
        signal_repetitions: 5
        enable_receive: true
```

Then you need to set up the platform

```python
def setup_platform(hass, config, add_entities, discovery_info=None):
	rf = hass.data[DOMAIN]

	switches = config.get(CONF_SWITCHES)
	devices = []
	for dev_name, properties in switches.items():
		devices.append(
			Open433Switch(
				properties.get(CONF_NAME, dev_name),
				rf,
				properties.get(CONF_PROTOCOL),
				properties.get(CONF_LENGTH),
				properties.get(CONF_SIGNAL_REPETITIONS),
				properties.get(CONF_CODE_ON),
				properties.get(CONF_CODE_OFF),
				properties.get(CONF_ENABLE_RECEIVE),
			)
		)

	add_entities(devices)
```

First I retrieve the rf instance that was stored earlier in the init, get the array of switches in the configuration iterate over them and then declare each device (the Open433Switch class) and tell home assistant about my entities. So about he Open433Switch:

```python
class Open433Switch(SwitchEntity):
	def __init__(self, name, rf, protocol, length, signal_repetitions, code_on, code_off,enable_rx):
		self._name = name
		self._state = False
		self._rf = rf
		self._protocol = protocol
		self._length = length
		self._code_on = code_on
		self._code_off = code_off
		self._signal_repetitions = signal_repetitions
		if enable_rx:
			self._rf.addIncomingPacketListener(self._incoming)

	def _incoming(self, packet):
		if isinstance(packet, rcswitch.packets.ReceivedSignal):
			if packet.length == self._length and packet.protocol == self._protocol:
				if packet.decimal in self._code_on:
					self._state = True
					self.schedule_update_ha_state()
				if packet.decimal in self._code_off:
					self._state = False
					self.schedule_update_ha_state()

	@property
	def should_poll(self):
		return False

	@property
	def name(self):
		return self._name

	@property
	def is_on(self):
		return self._state

	def _send_code(self, code_list, protocol, length):
		with REQ_LOCK:
			self._rf.setRepeatTransmit(self._signal_repetitions)
			for code in code_list:
				packet = rcswitch.packets.SendDecimal(value=code, length=length, protocol=protocol, delay=700)
				self._rf.send(packet)
		return True

	def turn_on(self, **kwargs):
		if self._send_code(self._code_on, self._protocol, self._length):
			self._state = True
			self.schedule_update_ha_state()

	def turn_off(self, **kwargs):
		if self._send_code(self._code_off, self._protocol, self._length):
			self._state = False
			self.schedule_update_ha_state()
```

Basically in the class the thing you need to worry about is the Open433Switch() that is expanding the SwitchEntity class, the should_poll propriety, the name propriety, the is_on propriety, the turn_on function and the turn_off function.

These function/ proprieties executes / get polled at different time. Example when you change the status in the dashboard the turn_on / turn_off function get executed. When the code executes self.schedule_update_ha_state() the proprieties get polled

And that's the basics

## Links

{{< og "https://developers.home-assistant.io/docs/creating_integration_file_structure" >}}