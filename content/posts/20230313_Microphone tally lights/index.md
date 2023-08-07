---
slug: microphone-tally-lights
title: "Microphone tally lights"
draft: false
featured: false
date: 2023-03-13T11:00:00.000Z
image: "images/cover.jpg"
tags:
  - concerts
  - electronics
  - audio
  - M32 
  - diy
  - web
  - 3D
authors:
  - samuel
---

Creating a microphone holder with tally lights for a live show and integrating it to the MIDAS M32 mixing console

<!--more-->

**WARNING: This is a stupidly long article, it details the concept, design, and construction phases thoroughly, you'll need probably more than 45 min to really read it**

Every once in a while, I work in my local choir. Every few years, they do a tour singing music for around 3h. This year there are more than 25 singers and 15 microphones. Add microphones for the drums, bass, guitar, saxophone, trumpet, ..... and you reach the maximum 32 channels of our MIDAS M32 console quite fast.

You may notice that 25 is greater than 15 🤔, that's because we have one or two techs who hand out the mics according to the all mighty “mic-sheet”. 

Basically, this sheet is a grid of every song and every microphone with the performer's name if they need one. It gets fine-tuned over time during rehearsals so that when the first real concert comes, the mic transitions between performers are as smooth as possible. This is fine and worked for over a decade, but we are still human and sometimes mistakes happen. For example, someone might grab the wrong mic and go on stage, or maybe the microphone has become magically invisible 👻.

Combine that with my love for problem-solving 🤓, and I decided that I would do a system that can do multiple things:
  - Keep the microphones neatly organized
  - Connect to the MIDAS M32 and retrieve mute & fader values
  - Display mute status to the backstage techs
  - Determine if a microphone is in the holder or in someone's hand
  - Display this in the mixing booth so that we can figure out what the hell is going on if something is wrong

One problem that could still happen is that someone could put the wrong microphone in the wrong holder, we would have no way of knowing which one is the right one. But my guess is that it's more likely that the mics run out of battery than someone misreading two numbers (one on the mic and one on the holder) 🤷‍♂️.

## Microphone holders

I thought about using RFID tags on each mic to solve the "wrong holder" issue, and that would indeed make sure that the right microphone is in the proper holder. But, that brings me to the 2nd thing that this project needs to be: **cheap!** 💰 The thing is that I'm doing everything myself and don't want to spend 20 EUR per holder, especially knowing that one could break in the chaos of the backstage. No, I want it to be as cheap as possible. 
 
But, I still need to have 15 of them connected to a controller capable of talking to the M32.

That took some though 🤔 as I originally wanted to do use a single bus or a daisy-chaining approach, where all holders would have an IN and an OUT port to simplify wiring.

### Connecting 15 holders together

Single bus/daisy-chaining for the LEDs is easy, a few WS2812B in each holder will do just fine, and they already work with daisy-chaining ✅. 

The input for the microphone detection was a bit trickier though, I first looked at one wire IO extenders like the [DS2408](https://www.analog.com/media/en/technical-documentation/data-sheets/DS2408.pdf) or the [DS2413](https://www.analog.com/media/en/technical-documentation/data-sheets/DS2413.pdf), but they are respectively 8 EUR and 3 EUR for a single chip in the quantities I need. Far too expensive 💸.
At the same time I started this project, I had an ongoing PCB order, I thought that I could potentially put a full RP2040 block in each holder, but that would also be 2 - 5 EUR per holder in the quantities I require.

So short of doing some analog trickery to make the thing work on one wire 😐, I said f- that and committed to a star topology. That means I have to bring a cable from the controller to each holder that contains these signals:
  - Ground
  - LED In
  - +5V
  - LED Out
  - Microphone detection OUT

The LED out of each holder is wired to the LED in of the next one, and the "Microphone detection" button goes to a GPIO of the controller.

### Detecting the microphone

The first thing anyone would think of is a simple switch. While that could work, being on a budget also means that we don't have the same microphone, some are smaller than others, and I wanted to avoid doing two weeks of cad to try to make a holder compatible with everything (especially since I didn't even have access to the microphones at the start).

The second option I thought of 💡 is an IR proximity sensor. Those are also pretty cheap, [15eur for a pack of twenty](https://www.amazon.fr/dp/B08DR1W3BK) is pretty good. So, I went ahead and ordered a pack, I could always find a use for it elsewhere if it didn't work out.

Once I got them I discovered a fatal flaw in my plan, the microphones are black and round ⚫ which doesn't really reflect the light from the sensor very well if at all. After some thinking and even trying to go back to the switch option, I realized the detection could be "normally closed" and use the microphone to block the path of the IR beam instead of reflecting it.

Perfect, I now have a cheap way of determining whether the microphone is in the holder or not 👍.

### CAD
I still needed an actual solid piece of plastic to hold the microphone. The holder needs to satisfy these requirements:
 - Holding a wide variety of microphones
 - Able to be screwed to a piece of wood
 - Able to hold a label for the microphone number
 - A way to display and diffuse the LED light
 - Enought space for IR LEDs in the holder arms 
 - Flexible enought to accommodate even bigger microphones if necessary

After some revisions (some of which happened while I was already printing) 🤫, I ended up with this design which is printed upright in two parts (holder and led diffuser):
{{< gallery >}}
images/dl_SLDWORKS_2023-02-27_17-01-34_1a44898c-4a17-4f2d-9c47-e3b53fc68dc0.png
images/dl_SLDWORKS_2023-02-27_17-02-01_bbebc3dd-72b8-4af6-bad8-e9b331f6c86a.png
{{< /gallery >}}

The LEDs are inserted in the sidearms, in retrospect, it would probably have been better to order modules with 3 mm LEDs instead of 5 mm ones since they stick out a bit, but it doesn't need to be perfect, it just needs to work. It's going to get beat up anyway 🙄. The cable for the LEDs get routed in a small channel in the arm, which then comes out in the back, where I can put the rest of the components.
![Microphone holder clip](images/dl_SLDWORKS_2023-02-27_17-04-21_9da479a1-a599-4488-a3d5-e359dd1ae75a.png)
Once the LEDs are inserted, a small piece of heat-shrink with a hole is placed over the LED to secure it in place:
![](images/dl_signal-2023-03-05-154217_002_crop.jpeg)

![Microphone holder LED channels](images/dl_SLDWORKS_2023-02-27_17-03-31_94090686-b99d-4937-a28f-a372fcfec0a8.png)

To make it easier to build the 16 modules, I chose to use a classic LED strip, I cut out 6 LEDs and jammed them in a little recess that I put in the design.

{{< gallery >}}
images/dl_SLDWORKS_2023-02-27_23-27-26_547684df-6f3d-46d3-8c26-a26b1bf7cacf.png
images/dl_signal-2023-03-05-152528_028_cropped.jpeg
{{< /gallery >}}

Finally, the PCB of the IR module gets attached with a piece of double-sided tape on the back and everything gets soldered together.

![](images/dl_signal-2023-03-05-152528_027_cropped.jpeg)

I then spent 4 days printing everything (I printed 4 modules at the same time, which kept the printer busy for around 18h 😴). The assembly was actually straightforward once I got the hang of it, but I'm glad it's done.

Now that everything is assembled, I printed some LED diffusers and stuck some labels with the microphone number printed on it:
![](images/dl_signal-2023-03-05-152528_008_eddited.jpeg)

#### Flaws and improvement
If I were to re-design this, I would probably do the following:
- Manufacture two PCBs:
	- One that follows the shape of the arms with side mounted IR LEDs and photodiode,
	- One that I could put on the back with some side mounted [WS2812B-4020](https://www.lcsc.com/product-detail/Light-Emitting-Diodes-LED_Worldsemi-WS2812B-4020_C965557.html) instead of an LED strip. In addition, use some sort of interconnect with the side arms PCB,
- Maybe print the holder out of a semi-flexible material and not PLA (at least for the arms). Because while I did print them at 100% infill, I fully expect at least one to break at some point. A hard TPU seems like a better bet. Unfortunately, I don't think my printer will handle it well, especially in the winter.

This would make the holder slimmer and sturdier. It might even be possible to print this hypothetical version in metal.

### Wiring
Originally, I wanted to have a cable going out the bottom of each holder with the JST connector and the same cable going to the controller. That would have resulted in a big mess of cables, especially at the start 😵.

Once everything was printed, we began shopping for a piece of wood that could holder everything. By pure luck, we found a [U-Shaped channel of MDF](https://www.leroymerlin.fr/produits/menuiserie/panneau-bois-tablette-etagere-tasseau-moulure-et-plinthe/moulure-champlat-baguette-angle/nez-de-cloison-medium-mdf-pour-cloison-de-70-mm-11-x-73-mm-l-2-5-m-70180530.html) that would be:
- Tall enough for the holders,
- Long enough for 16 of them,
- Deep enough to route the cable behind.

![U-Shaped channel of MDF](images/dl_3b273619-b4d4-4662-92de-be146b45277a.webp)

So, my dad and I started by drilling the two screw holes for each holder, plus a 20 mm hole for the cable to pass to the back. We choose to leave 2.5 cm of space between each holder to leave enough room to grab the mic easily, and something like 15 cm of space on each side for the controller.

Unfortunately, the +2 m piece of MDF wasn't very stiff, and the thing was flapping like crazy 🤔. I'll come back to that. To pile up on the bad news, the screws we chose were a bit too long by something like 5 mm. 

Fortunately, we found some aluminum channels that are 20 mm deep and the perfect width. These aluminum extrusions are typically used on the side of flight cases. Mine looks a bit like this one: 
https://www.thomann.de/fr/adam_hall_6102_schliessprofil.htm
![](images/dl_9185483.jpg)

It was perfect 😄. The board looks super nice, the screws are not too long any more and as the bonus, the board is super stiff now:
![First test of all the holders on the board](images/dl_signal-2023-03-01-164250_009.jpeg)

You can see that the bottom screw is barely short enough, but it will actually be very helpful later to hold the cable harness 😏:
![Backside of the board](images/dl_signal-2023-03-01-164250_008.jpeg)

I then proceeded by cutting a ton of wires for power distribution and for the addressable LEDs data line 😫. Instead of soldering everything manually, I choose to use these wonderful heat shrink pieces that already have some solder in them: [https://fr.aliexpress.com/item/1005003878417358.html](https://fr.aliexpress.com/item/1005003878417358.html).
![LED Cable harness heat shrink pieces](images/dl_signal-2023-03-01-164250_004.jpeg)

The white cable you can see is the connection of the IR module. To connect this one, I cut a 16 conductor by +2 m long piece of ribbon cable, separated the cable where required and soldered the same heat shrink pieces everywhere.

This made for a very nice cable harness to put in the back (The photo is missing the ribbon cable)  👍.
![LED Cable harness](images/dl_signal-2023-03-01-164250_003.jpeg)

To fix everything in place, I printed some big washer that I placed on the screw post of the holder with the cable underneath. After that was done, everything was nice and neat:
![](images/dl_signal-2023-03-01-164250_011.jpeg)

## Controller
Now that I have 15 holders and a spare, I need something to control them. Originally, I wanted to use an ESP32 and fully integrate everything. 

The controller needs to be able to do a few basic things:
 - Connect to the M32 OSC protocol and get mutes/fader values,
 - Drive the WS2812B,
 - Read all the 15+1 inputs.
 
Alongside that, a few other things need to be considered when being in a "pro" context:
 - Stability: The thing should start fast, can withstand a power cut, handle potential network disconnects, etc.
 - Reliability: The thing has to stay connected and work for hours without interruption.

That meant Wi-Fi was out of the question because there are too many issues when numerous people are connected, and I don't have the time/budget to set up a proper Wi-Fi network 📡.

Fortunately, we already have a wired network planned, which means: let's go with Ethernet.

I actually figured out quickly how to get Ethernet working on the ESP32. While I did make some progress fairly fast, I figured that I couldn't reach the required stability and reliability level by the start of the first concert. It's just too much work to re-implement everything manually for a quick project.

So, I dug out a now very rare PI Zero 2, and decided that I was going to use it 🤷‍♂️.

### Reading inputs
At first, I thought of a whole plan to use IO extender to read all the inputs. Then I looked closely at the PI and I realized that the thing has GPIO, I never used them to the point where I just forgot that they existed 😓.

A minimal issue is that my signal from the holders are +5V, and I need them to be ≤3.3V. This can be taken care of with a resistor divider, I chose 10K/10K because that's all I had in hand, which gave me 2.5V, not quite 3.3V but still above the threshold, perfect 👍.

### LEDs
Well, there is not a lot to say here. The ws2812b is a single pin, so I just used one that was available and called it a day 😅

### Ethernet

I have some cheap Ethernet dongles. I cut one up and soldered it up to the D+/D- test pads of the PI Zero, that gives me Ethernet connectivity

![PI0 2W Test pads description](images/dl_Raspberry-Pi-Zero-2-W-Test-Pad%20%281%29.png)

### Wiring

To make things easier, I decided that I would use a PCB. The issue is that, again, that I needed this thing as soon as possible ⏱, so I can't do a pre-made PCB and wait a week for shipping. I decided that I would, instead, use a perfboard and do some manual soldering.

There really isn't a lot to say, I soldered in some headers, the resistors for the dividers and some terminal blocks for power and the LEDs data.

I also soldered some DuPont connectors to the D+ and D- of the Raspberry Pi for the Ethernet card instead of using a USB to OTG adapter.

### CAD
I spent some time making the PCB and the Raspberry Pi fit inside a very basic box
![Controller box](images/dl_SLDWORKS_2023-03-03_14-17-44_c818f447-b903-49a9-8e36-a8189312d429.png)

Added some holes for power, and status LEDs:
![Controller box with LEDs and power holes](images/dl_SLDWORKS_2023-03-03_14-19-21_2e9fe2e9-38e9-4a9c-ab72-a7aa6c88dec7.png)

I then added a place for the network card
![Controller with the network card slot](images/dl_SLDWORKS_2023-03-03_14-19-44_7d8352f2-927a-42f0-b1e2-a8b90358382d.png)

Once that got printed, I put the PCB, network card (which I had to hot glue in to secure it), LEDs and the power connector in it. And, finally, wired the 16 inputs from the wire harness and screwed in the power cables and LED data cable.
{{< gallery >}}
images/dl_signal-2023-03-13-224316_006.jpeg
images/dl_signal-2023-03-13-224316_004.jpeg
{{< /gallery >}}

After securing it on the MDF board, it looked perfect.
{{< gallery >}}
images/dl_signal-2023-03-13-224316_010.jpeg
images/dl_signal-2023-03-13-224316_009.jpeg
{{< /gallery >}}

## Software
As I needed it to work as soon as possible 🐇, I went with something I knew for sure and used python 🐍.

The first thing I did was test out the LEDs and inputs. I used the circuit python libraries because it just works. Didn't have to fiddle to make something work correctly. And, sure enough, everything worked right away, nice 👍.

Initially, I did everything in one big script, but that became an issue when I had multiple loops and a web server.

I then thought that it might be better / easier to write a few interconnected modules than to write a big one 🤔. There are a few options for connecting multiple parts together. ZMQ and MQTT are pretty popular, I then remembered that MQTT has a web socket version (which I could easily use for a Web UI later 🌐) and went with it.

### MQTT Server
I chose to use the mosquito mqtt server, installing it was pretty straightforward:
```shell
sudo apt update
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto.service
```
Then, I just need to enable anonymous access, traditional MQTT and Websocket support in the config:
```conf
listener 1883
listener 8080
protocol websockets
allow_anonymous true
```
*Note: using authentication here wouldn't be very useful, since the credentials could have been easily recovered in the source code of the webui* 🤷‍♂️


After a quick test with the MQTT explorer app on my computer to check that it was working. So, I went ahead and started working on the global config.

### Configuration
The `config.py` file of x32_tally contains several variables that I can configure to alter the way the tool works. This includes:
- The address of the X32,
- The address of the MQTT server,
- Log levels for every module,
- Colors for the tally lights:
	- Muted / Active,
	- Muted blinking ON / Active blinking ON,
	- Muted blinking OFF / Active blinking OFF.
- Pin for the neopixels,
- List of input channels with:
	- The status (enabled or not),
	- The list of LEDs for the tally lights,
	- The pin for the "on-stand" detection.

### IO Configuration
The `io.py` file contains definitions for the `LedController` and `InputController` classes. These act as a wrapper for the Adafruit libraries, this allows me/someone to easily change the input/output method without the need to rewrite every module 😏.

```python
class LedController:
	def __init__(self):
		highest_pixel_id = 0
		for ch_n, ch in config.input_channels.items():
			if "tally_leds" in ch:
				highest_pixel_id = max(highest_pixel_id, *ch["tally_leds"])
		self.pixels = neopixel.NeoPixel(config.tally_neopixel_pin, highest_pixel_id + 1, auto_write=False)

	def update(self):
		self.pixels.show()

	def set(self, leds, r, g, b):
		for led in leds:
			self.pixels[led] = (r, g, b)
```
```python
class InputController:
	def __init__(self):
		self.buttons = {}

	def get(self, pin):
		if pin.id not in self.buttons:
			self.buttons[pin.id] = digitalio.DigitalInOut(pin)
			self.buttons[pin.id].direction = digitalio.Direction.INPUT
		return self.buttons[pin.id].value
```

This file also contains a function for creating MQTT clients. It takes a name and returns the client:
```python
def get_mqtt_client(client_id):
	client = mqtt.Client(
		client_id=client_id,
		reconnect_on_failure=True
	)

	client.enable_logger(logging.getLogger("MQTT"))
	client.connect(config.mqtt["host"], config.mqtt["port"], 60)
	return client
```

Finally, this module also broadcasts the input channel config every time it's loaded. This is only for the Web UI, as it obviously doesn't have access to the `config.py` file.


### 1st module: MIDAS M32 to MQTT bridge

As the headline suggests, the most important thing is to forward messages from the M32 to the MQTT server so that other modules can access it.

As a request from the sound engineer, **I purposefully did not implement the MQTT to M32 side to avoid something writing to the console and causing something bad 😕** (That being said, it would be trivial to implement).

The MIDAS M32 uses a custom implementation of the [OSC](https://ccrma.stanford.edu/groups/osc/index.html) protocol. OSC is wonderful, works super well, and it's widely used. It's no wonder they used it.

One tiny annoying thing about their implementation is that you need to send packets to the port `10023` of the console. But it does not respond to you on `10023`, instead it responds to whatever ephemeral port the system decided to use to send the packet. This means that you need to keep the same socket.

It's a small inconvenience, but it also means that you don't have to select a different port for each app 👍.

Somebody did an incredible job of reverse engineering what each command does and published a [ton of software for the X32](https://sites.google.com/site/patrickmaillot/x32#h.p_rE4IH0Luimc0). Including an emulator, which is helpful when you don't have the 3600 EUR console next to you. He also published a [spec sheet](https://drive.google.com/file/d/1Snbwx3m6us6L1qeP1_pD6s8hbJpIpD0a/view) of OSC commands which is very useful.

Turns out that to query a setting of the console you just have to send the same command that you would normally send for setting it but without the parameters.

Essentially, that would mean that I need to send `/ch/XX/mix/on` and `/ch/XX/mix/fader` every few hundreds of a second to poll the status. That would be quite resource intensive for both devices 😓.

Instead, the engineers over at Behringer/Midas added the `/xremote` command, this command will subscribe you to every update happening                                                                     on the console (except VU meters for which there is a special command). The only thing is that you need to resubscribe every few seconds to keep receiving updates 👍.

To recap, I send:
-   Every few seconds (read 5):
    -   The `/xremote`  command to subscribe to console updates.
-   Every 60sec to force update of the values as a sanity check:
    -   The `/ch/XX/mix/on`  query to get the mute status of the channel XX,
    -   The `/ch/XX/mix/fader` query to get the fader value of the channel XX,
    -   The `/ch/XX/config/icon` query to get the icon of the channel XX,
    -   The `/ch/XX/config/name`  query to get the name of the channel XX,
    -   The `/ch/XX/config/color` query to get the color of the channel XX.

Unfortunately, after some testing with the real thing (as I started the development with an emulator), it turns out that the `/xremote` command doesn't send every fader update when changing cues, and it meant I had to wait for the forced update to refresh the status 😕.

To solve this, I had to dive into how the `/formatsubscribe` command works. This command allows the reception of regular updates for a topic. In this case, I subscribed to mute and fader values.

Note that this command did not work on the emulator, hence why I didn't use it from the start 🤷‍♂️.

On a tangent, I also looked at the `/showdump`, `/-prefs/show_control`, `/‐show/prepos/current` and `/-show/showfile/show/name` commands that allow me to get the show, its cues and the current position of cues.

So, how does that work in code. I used the `pythonosc` module to parse and build the OSC messages. I then wrote a class that inherit from `threading.Thread` to keep receiving the messages in the background. This is probably not necessary, but I wanted to be able to re-use this lib somewhere else if needed. I started by creating a few helper functions. 

#### Sending data

I first wrote a "send" function that wouldn't make the module crash if, for some reason, the network was not working.
```python
    # Wrapper function use to send data to the console.
    # The function tries to send the message but does not raise an error if it fails (it just logs it).
    # This can happen if the network card is not up yet
    def _send(self, data: bytes):
        try:
            self._socket.sendto(data, self._address)
        except OSError as e:
            self._log.warning(f"Tried to send data but got: {e}")
        except Exception as e:
            self._log.error(f"Tried to send data but got: {e}")
```
Next, I wrote wrappers around the OSC commands of the x32 that I'll often use. 
```python
    def _x32_format_subscribe(self, alias, addresses, start_i, end_i, interval=20):
        message = OscMessageBuilder("/formatsubscribe")
        message.add_arg(alias)
        for address in addresses:
            message.add_arg(address)
        message.add_arg(start_i)
        message.add_arg(end_i)
        message.add_arg(interval)
        self._send(message.build().dgram)

    def _x32_renew(self, alias):
        message = OscMessageBuilder("/renew")
        message.add_arg(alias)
        self._send(message.build().dgram)

    def _x32_xremote(self):
        message = OscMessageBuilder("/xremote")
        self._send(message.build().dgram)

    def _x32_info(self):
        message = OscMessageBuilder("/info")
        self._send(message.build().dgram)

    def _x32_showdump(self):
        message = OscMessageBuilder("/showdump")
        self._send(message.build().dgram)
```

Followed that with a function to force query the status of the fader and to dump the whole show.

```python
    def _query_channel(self, channel):
        self._send(OscMessageBuilder(f"/ch/{channel:02}/mix/on").build().dgram)
        self._send(OscMessageBuilder(f"/ch/{channel:02}/mix/fader").build().dgram)
        self._send(OscMessageBuilder(f"/ch/{channel:02}/config/icon").build().dgram)
        self._send(OscMessageBuilder(f"/ch/{channel:02}/config/name").build().dgram)
        self._send(OscMessageBuilder(f"/ch/{channel:02}/config/color").build().dgram)

    def _query_show(self):
        self._x32_showdump()
        self._send(OscMessageBuilder(f"/-prefs/show_control").build().dgram)
        self._send(OscMessageBuilder(f"/‐show/prepos/current").build().dgram)
        self._send(OscMessageBuilder(f"/-show/showfile/show/name").build().dgram)
```

Next, I did the re-sync and resubscribe functions. These functions are called respectively every 60 sec and every 5 sec.

The goal of the `_re_sync` is to be damn sure that our information is sync with the console. It also forces a `/formatsubscribe` command instead of a `/renew`.

The goal of the `_re_subscribe` command is to send the `/renew`, `/xremote` and `/info` commands to make sure we keep the update coming.

```python
    # Resync function. This function is executed every 60sec to make sure the internal status is up-to-date with the console
    def _re_sync(self):
        self._log.info("[TX] Forced queried infos and subscribed")
        self.last_resync = time.time()

        for i in range(1, 33):
            self._query_channel(i)

        self._x32_format_subscribe(
            alias="/subscribed/faders",
            addresses=["/ch/**/mix/on", "/ch/**/mix/fader"],
            start_i=1, end_i=32,
            interval=20
        )

        self._query_show()

    # Resubscribe function. This function is executed every 5sec to subscribe to updates from the console
    def _re_subscribe(self):
        self.last_resubscribe = time.time()
        self._log.info("[TX] Renewed subscriptions")
        self._x32_xremote()
        self._x32_info()
        self._x32_renew("/subscribed/faders")
```
#### Receiving data & handlers

Now that we can send messages, we need to receive them. I started by writing a handler for all messages. This function receives an OSC message and forward it to the appropriate internal or external handler.

```python
    # Internal OSC message handler
    def handle_message(self, message):
        self.last_incoming = time.time() # Reset the last incoming timer

        if message.address == "/subscribed/faders":
            self.handle_message__subscribed_faders(message)
            return  # Subscribed aliases are internal message no need to forward it

        if message.address == "/node":
            self.handle_message__node(message)
            return  # Can't forward node responses

        # If the address is "/info" retrieve the server version/name and the console model/version and trigger the connection handlers
        if message.address == "/info":
            self.handle_message__info(message)

        # The message to every other handler
        for handler in self.handlers:
            handler(message)
```

The `/info` handler is basic. It simply extracts the information, stores it and calls every "connection" handler.

```python
    def handle_message__info(self, message):
        self.x32_server_version = message.params[0]
        self.x32_server_name = message.params[1]
        self.x32_console_model = message.params[2]
        self.x32_console_version = message.params[3]
        for handler in self.connection_handlers:
             handler(self.has_connection)
```
The handler for `/node` responses is a bit more complex. The node messages are basically an OSC message converted to a string and terminated by a newline. The only (string) argument looks a bit like this `/-prefs/iQ/01 none "Linear" 0\n`. To parse it, I used the `shlex` module to do lexical analysis of the received text (because the quoted text might contain space, I can't use a simple split). Using this method, the address is the first element, then I check if every parameter is a float or an int, if not, it defaults to a string. Then, I call the `handle_message` recursively to redistribute the message.
```python
    def handle_message__node(self, message):
        data = shlex.split(message.params[0][:-1])
        msg = OscMessageBuilder(data[0])
        for param in data[1:]:
            msg.add_arg((int(float(param)) if float(param).is_integer() else float(param)) if _is_number_tryexcept(param) else param)
        self.handle_message(msg.build())
```
The `/formatsubscribe` command will send one binary blob message instead of multiple messages for everything subscribed. Since I subscribe to `/ch/**/mix/on` and `/ch/**/mix/fader` with a start of `1` and an end of `32` the console sends a binary blob consisting of 32 int32 for the mute status and 32 float32 for the fader values. Decoding this is straightforward thanks to the `struct` module and this format `<i32i32f`. Then I again call the `handle_message` recursively with "fake" messages
```python
    def handle_message__subscribed_faders(self, message):
        if len(message.params[0]) != (4 + 4 * 32 + 4 * 32):
            self._log.warning("Messaged recevied by the /subscribed/faders handler that doesn't have the right size ({len(message.params[0])} != 260)")
            return
        data = struct.unpack(f"<i32i32f", message.params[0])[1:]  # Ignore first byte which is the length
        # Fake messages to maintain compatibility
        for i, value in enumerate(data[:32]):
            msg = OscMessageBuilder(f"/ch/{i+1:02}/mix/on")
            msg.add_arg(value)
            self.handle_message(msg.build())
        for i, value in enumerate(data[32:]):
            msg = OscMessageBuilder(f"/ch/{i+1:02}/mix/fader")
            msg.add_arg(value)
            self.handle_message(msg.build())
```
#### Main loop
This loop is responsible for:
- Calling the `_re_sync` function every 60sec 
```python
             if self.last_resync + 60 < time.time():
                self._re_sync()
```
- Calling the `_re_subscribe` function every 5sec
```python
             if self.last_resubscribe + 5 < time.time():
                self._re_subscribe()
```
- Checking that it's still connected to the X32
```python
            # Connection status check
            if last_connection_status != self.has_connection:
                last_connection_status = self.has_connection
                # Notify handlers
                for handler in self.connection_handlers:
                    handler(self.has_connection)
                # Force a resync if we just connected
                if self.has_connection:
                    self._re_sync()
```
- Receiving data from the socket
```python
            try:
                # A while loop here will ensure that if there is still data incoming it will be read before processing re-syncs
                # recvfrom will throw an error if there isn't anything thus exiting the loop
                while True:
                    # Receive data from the socket
                    data, peer = self._socket.recvfrom(1024)

                    # If data is present, and it's an OSC message, send it to the internal handler
                    if data and OscMessage.dgram_is_message(data):
                        self.handle_message(OscMessage(data))
                    # The message might also be a "/node" message from the console. These message don't start with / and thus don't comply with the OCS standard.
                    # Manually correct the address and send it to the internal handler
                    elif data.startswith(b"node"):
                        data = data.replace(b"node\x00\x00\x00\x00", b"/node\x00\x00\x00")
                        self.handle_message(OscMessage(data))
                    # If data is present, and it's an OSC bundle, unpack it and send all message to the internal handler
                    elif data and OscBundle.dgram_is_bundle(data):
                        for message in OscBundle(data):
                            self.handle_message(message)
                    else:
                        self._log.error(f"Received invalid data: {data}")
            except BlockingIOError:
                # Ignore BlockingIO errors
                pass
```
Quick note on the `/node` message: Unfortunately, Midas/Behringer didn't fully follow the OSC spec and the `node` messages don't start with the `/` 😕, they are padded properly though, so all it takes is a simple `.replace` before handling the message 🎉.

In the ``__main__`` of the module, I simply start an MQTT client and the M32 client and forward every incoming message OSC to MQTT with the topic prefixed by `modules/osc`:
```python
def forward_to_mqtt(message: OscMessage):
    client.publish(
        topic=f"modules/osc{message.address}",
        payload=json.dumps(message.params),
        retain=True
    )


# Define the function that sends out the status of the module
def publish_connection_status(is_connected):
    client.publish(
        topic=f"modules/osc/status",
        payload=json.dumps({
            "connected": is_connected,
            "x32_server_version": x32.x32_server_version,
            "x32_server_name": x32.x32_server_name,
            "x32_console_model": x32.x32_console_model,
            "x32_console_version": x32.x32_console_version,
        }),
        retain=True
    )


x32 = X32(x32_address)
x32.handlers.append(forward_to_mqtt)  
x32.connection_handlers.append(publish_connection_status)
x32.start()
```
Note that the message is published with the `retain=True` this means that the server will keep a copy of the last message and will send the last value every time a client subscribes to the topic

### 2nd module: Inputs

That module is dead simple, t's only job is simple to send out any updates to the MQTT server:

```python
while True:
    for ch, input_channel in config.input_channels.items():
        # Get (if possible) the value of the buttons, Defaults to None if the channel does not have a button
        channel_value = None
        if "on_stand_button" in input_channel:
            channel_value = inputs.get(input_channel["on_stand_button"])

        # If the status has changed, publish the values over MQTT
        if ch not in last_channel_values or last_channel_values[ch] != channel_value:
            last_channel_values[ch] = channel_value
            client.publish(
                topic=f"modules/stand_buttons/{ch:02d}/status",
                payload=json.dumps({
                    "enabled": input_channel["enabled"],
                    "has_button": "on_stand_button" in input_channel,
                    "value": channel_value,
                    "last_update": time.time()
                }),
                retain=True
            )
            client.publish(f"ONSTAND_DETECTION/ch/{ch:02d}/is_on_stand", last_status[ch], retain=True)
```

It loops through all channels that have input configured and check if the microphone is in the holder. Only if the current value is different from the old value, it sends an update to the `modules/stand_buttons/XX/status` with a JSON dict containing:
- If the channel is enabled,
- If it has a button,
- The value of said button,
- The last time it was updated.

Same as before, the message is published with the `retain=True` which means that the server will keep a copy of the last message.

### 3rd module: LEDs
This module is basic but a bit more involved as it needs to keep a history of the messages received.
In simple terms, every time a message is received, it's put in a dict with the key being the topic.
```python
message_history = {}

def on_message(client, userdata, msg):
	global message_history
	try:
		message_history[msg.topic] = json.loads(msg.payload)
	except json.decoder.JSONDecodeError as e:
		pass
		
client.on_message  =  on_message

def try_get(obj, topic):
	if topic in obj:
		return obj[topic]
	return None
```

To avoid iterating over a channel that doesn't have LEDs, I added a filter that creates a dict with only channels that have LEDs:
```python
input_channels_with_leds = {
	ch: input_channel
	for ch, input_channel in config.input_channels.items()
	if "tally_leds" in input_channel
}
```

Then there are two functions. 
One will do an animation with the LEDs and is used when the OSC module reports that it cannot connect to the M32. This animation is a simple ping-pong style animation with LEDs.

The more interesting function is the `do_tally_lights` function. This one is responsible for looping over every channel with an LED:
```python
def do_tally_lights():
    # Loop over every channel that have LEDs
    for ch, input_channel in input_channels_with_leds.items():
        # Set the default color to black
        color = [0, 0, 0]
```
Getting the vales from the history
```python
        # Get the mute, fader and is_on_stand values from the history
        x32_on = try_get(message_history, f"modules/osc/ch/{ch:02d}/mix/on")
        x32_fader = try_get(message_history, f"modules/osc/ch/{ch:02d}/mix/fader")
        module_is_on_stand = try_get(message_history, f"modules/stand_buttons/{ch:02d}/status")
```
Checking that the channel is actually enabled
```python
        # If the channel is enabled
        if input_channel["enabled"]:
            # If the value stored in the history for the mute and fader values are not None
```
Checking that there is, a history for either the `fader` or the `mute` status, If there isn't that either means that the channel doesn't exist or wasn't updated yet. I then set the LEDs to black in this case.

On the other hand, if I have a value I then determine if the channel is active, meaning unmuted and a fader being at more than 8%. If it's active, I turn the LEDs green and set the LEDs to red if inactive.
```python
            if x32_on is not None and x32_fader is not None:
                # Calculate if the channel is active
                is_active = x32_on[0] and x32_fader[0] > 0.08

                # Set the channel color
                color = config.tally_colors["active"] if is_active else config.tally_colors["muted"]
```
Then, it checks if there is a history for the "is on stand" value. If the microphone is **on the holder** but **is active** or if the microphone is **not** on the holder and **inactive**, I blink the LEDs brightness to signal an issue.
```python
                # if the value stored in the history for the is_on_stand is not None
                if module_is_on_stand is not None:
                    # If the channel is active and in the stand or not active and not in the stand
                    if module_is_on_stand["value"] == is_active:
                        # Math tricks to make it blink slower
                        if int(time.time() * 5) % 2 == 0:
                            # Set the bright color to the channel
                            color = config.tally_colors["active_in_stand_on"] if is_active else config.tally_colors["muted_not_in_stand_on"]
                        else:
                            color = config.tally_colors["active_in_stand_off"] if is_active else config.tally_colors["muted_not_in_stand_off"]
```
Then to finish, I set the color and set the LEDs:
```python
    leds.set(leds=input_channel["tally_leds"], r=color[0], g=color[1], b=color[2])
```

Then in the main loop, I check the status of the OSC module, choose the correct animation and update the LEDs
```python
while True:
    # Get the OSC module status
    osc_status = try_get(message_history, f"modules/osc/status")

    # Test if the OSC module is connected and execute the proper function
    if osc_status is None or not osc_status["connected"]:
        do_disconnected_animation()
    else:
        do_tally_lights()

    # Update the leds
    leds.update()
    time.sleep(0.05)
```


I might do a third color if the channel is unmuted, but the fader is down. This would signal that the sound engineer is ready for the next part, and is about to enable them.

### 4th "module": Web interface

One thing that would be very useful is the ability to see the status of the microphones in the mixing booth. To accomplish that, I wrote a basic app based on Vue.js that uses MQTT thanks to Websockets and the `mqttjs` library.

The web app subscribes to the data of all 32 channels (meaning name, icon, mute status and fader value) from MQTT and displays it nicely. The On stand detection is also synced from MQTT if available and will stay gray otherwise.

As a sidenote, getting these stupid icons was not fun, while they are in the spec sheet of the unofficial M32 OSC doc, it's one big image not 70+ individual images. I had to dig out some old OpenCV code to detect the 64×64 black squares and extract them manually. Then, thanks to ImageMagick, I applied a black to alpha filter to get rid of the background. *The individual images can be found in the GitHub repo.*

#### Screenshot
Thanks to Vuetify, I didn't need to do a lot of CSS, just for the strips themselves. Once this UI placement was finished, I had a very nice read-only UI that even works on phone (kind of, you need to scroll a lot since I chose to force the cue list open on every device):

![](images/dl_pn_2023_03_06_09-27-32_p4w6vFiaUD.png)

A strip surrounded in blue means that someone has the microphone in his/her hand, but it's still muted. Meanwhile, a yellow border means that it's unmuted on the stand. If a strip doesn't match any of these conditions, the strip reflects the color stored in the X32.

#### Web server
I then built the project to get only static files and started the configuration of the web server.
I went with Caddy because it works, it's simple, and the docs are pleasant, and I'm familiar with it.

After following the Debian install instruction from https://caddyserver.com/docs/install#debian-ubuntu-raspbian, I edited the config file as `/etc/caddy/Caddyfile` it now looks like this:

```caddy
:80 {
	root * /opt/x32_tally/x32_tally/spa_webui/dist/
	reverse_proxy /mqtt 127.0.0.1:8080
}
```

By default, it uses the files located in `/opt/x32_tally/x32_tally/spa_webui/dist/` (where the built files are) and also proxies `/mqtt` to the mosquito Websocket server

### Running as services
All services are pretty similar, for example, the OSC module looks like this:
```ini
[Unit]
Description=X32Tally OSC module
After=syslog.target network.target mosquitto.service

[Service]
Type=simple

User=root

WorkingDirectory=/opt/x32_tally
ExecStart=python -m x32_tally.osc

Restart=on-failure

[Install]
WantedBy=default.target
```
I'm aware that running scripts as root is not the best idea ever. However, I wanted to avoid fiddling with making GPIOs accessible to non-root users, it was just easier this way.

It's something that I would definitively improve have I had more time.

### Read-only file system
As I mentioned before, the system needs to withstand power cuts. The poor SD card isn't the best thing for the job in the first place, so I choose to make the system read-only. I followed this nicely written guide at https://medium.com/@andreas.schallwig/how-to-make-your-raspberry-pi-file-system-read-only-raspbian-stretch-80c0f7be7353

## Functional diagram

Now that I had finished, I spent some time doing a diagram that shows how everything interconnects
.
![Functional diagram](images/dl_diagram.drawio.png)


## And in use?
Last week was the first time this system was actually used in production:
{{< gallery >}}
images/dl_signal-2023-03-01-172743_003.jpeg
images/dl_DSC00762_crop.jpg
{{< /gallery >}}

And it worked perfectly. 

Or that's what I would have said were it not for that stupid network card I used 🤬. That thing worked for 1h and decided to completely stop working right when everyone started to come in.

I don't know the issue for sure, but someone mentioned that it might be due to a potential difference between the power I used, and the one used for everything else. It shouldn't really happen because Ethernet is supposed to be isolated, I guess it wasn't 🤔.

I had to carve out a hole in the controller box to be able to plug a micro USB OTG adapter and plugging a better network card in. I'll re-print everything with a different slot for another network card. Hopefully, that won't happen again.

**Apart from that, everything was perfect. Some responses I got range from good to super awesome. 🥳😃**

It allowed everyone in the mixing booth to see if we kept a mic open or if forgot to open someone. Backstage, it allowed techs to more easily visualize which microphone was taken at a glance. It also alerted them immediately if there were discrepancies from the mic-sheet.

## Conclusion
This system is wonderful, it facilitates the job of the backstage techs and gives more info in the mixing booth. I bet there are quite a few places where this could be very useful.

I think it would even be possible to implement some kind of auto-mixer where it would unmute automatically channels when the microphone is in someone's hand.

I do think that the biggest improvement I could make is using a custom PCB for the holders and printing it in a different material.

Overall, very pleased with this project 😄.

**Thanks to:** [Yuki](https://yukiisbo.red/), [Romain](https://romainmunier.fr/), [Dastan21](https://github.com/Dastan21), [David](https://www.tugler.fr/) and Geoffrey for proofreading this massive article.