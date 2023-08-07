---
title: "Let's turn lights on with the computer the 433Mhz way"
date: 2020-06-09T19:58:00.000Z
draft: false
featured: false
image: "images/cover.jpg"
tags:
    - DIY
    - Electronics
    - Home Automation
authors:
    - samuel
---

A while ago I started using home assistant on a pi and bought some inexpensive 433Mhz ac wireless switches. However, after one month of intense use the Raspberry Pi didn't have enough power, so I bought a cheap computer of eBay.

<!--more-->

It worked well expect that I didn't have control over my switches. Sure I could have use the raspberry in conjunction with the computer but that would be overkill, so I started designing an Arduino on a stick with USB and 433Mhz tx and rx. The first design I made was way too optimistic I planed to use a rf switch to switch between rx and tx and use a single sma port for the antenna but that didn't go so well and neither tx nor rx was working, so I just gave up for a few weeks and then made version two.

## Hardware

Version two is smaller and have two coiled antennas instead of a sma port and it works well enough. It's still based around an atmega328 running at 16MHz with the Arduino UNO bootloader and a CH340 USB to Serial converter. As it's so versatile in its operation, I also added expansion port for SDA / SCL / A0 / Pin8 (PD0) in addition to the iscp header with the spi bus so that the board could be used as standalone transmitter to send sensor values for example.

So here are some photos of the v2 board:
![](images/dl_chrome_2020-06-16_01-04-59.png)![](images/dl_chrome_2020-06-16_01-05-11.png)![](images/dl_IMG_20200616_010949.jpg)
Unfortunately as I'm an idiot I put the resistor for the power led on the wrong side of the board, so I couldn't solder it up and corrected it for v2.1

## Software

As I had good luck with the rcswitch library I wanted to use this library on the Arduino side and wanted to make a python library (for future integration with home assistant) resembling as much as possible as rcswitch. To make the board communicate with the software I was a first thinking a serial communication of the type "SEND:2523794944:32:2:700" but that's way too complicated and I wanted to try struct serialization so that what I did I made 4 structs for configuration / packet sent / packet received / acknowledgment and all prefixed by a char[17] for the packet type ("rcswitch_conf" / "send_decimal" / "receive_signal" / "ack") and the use this code to extract the raw bytes that I read from the serial port:

    char type[17];  //Create a tmp buffer to store the type of packet received
    memcpy (&type, &data_buffer, 17); //Copy only the first 17bytes to the tmp buffer (See ptype in each struct in packet.h)
    

Basically when the computer sends a command it toggles the rx led turn on the tx one do the action toggle backs the leds and sends an ack packet with sendAck();

On the python side of things I use struct to unpack the data coming from the board example for the Signal received packet:

    class ReceivedSignal(object):
    	"""docstring for received_signal_packet_t"""
    
    	def __init__(self):
    		super(packets.ReceivedSignal, self).__init__()
    		self.format = "<17sIIHHH"
    
    		self.time = -1
    		self.decimal = -1
    		self.length = -1
    		self.delay = -1
    		# self.raw     = None
    		self.protocol = 0
    
    	def __str__(self):
    		return "<ReceivedSignal time=" + str(self.time) + " decimal=" + str(
    			self.decimal) + " length=" + str(
    			self.length) + " delay=" + str(self.delay) + " protocol=" + str(self.protocol) + ">"
    
    	def parse(self, raw):
    		unpacked = struct.unpack(self.format, bytearray(raw))
    		self.time = unpacked[1]
    		self.decimal = unpacked[2]
    		self.length = unpacked[3]
    		self.delay = unpacked[4]
    		self.protocol = unpacked[5]
    		return self
    

The library ins't finished yet but look like this

    import rcswitch
    
    mySwitch = rcswitch.RCSwitch("COM3")
    time.sleep(2)
    
    # for packet in mySwitch.listen():
    # 	print(packet)
    
    packet_on  = rcswitch.packets.SendDecimal(value=2523794944, length=32, protocol=2, delay=700)
    packet_off = rcswitch.packets.SendDecimal(value=2658012672, length=32, protocol=2, delay=700)
    mySwitch.setRepeatTransmit(5)
    
    while True:
    	mySwitch.send(packet_on)
    	mySwitch.receive_packet(timeout=0.1)
    	time.sleep(1)
    
    	mySwitch.send(packet_off)
    	mySwitch.receive_packet(timeout=0.1)
    	time.sleep(1)
    

{{<og "https://github.com/TheStaticTurtle/Open433">}}
