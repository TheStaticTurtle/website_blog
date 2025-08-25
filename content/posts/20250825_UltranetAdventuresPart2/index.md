---
slug: ultranet-adventures-part-2
title: "Ultranet adventures part 2: Rebranding & Stagebox!"
draft: true
featured: false
date: 2025-08-25T00:00:00.000Z
image: "images/cover.jpg"
tags:
  - electronics
  - open-source
  - diy
  - audio
  - concerts
authors:
  - samuel
thanks: 
  - christian-noeding
  - geoffrey
  - romain
  - david
  - yuki
  - quentin
---

Continuing the ultranet adventure by building a fully functional 8 channel stagebox.

<!--more-->

{{< warn >}}
This is a continuation of an already stupidly long adventure, you can read <a href="/ultranet-adventures-part-1/">part 1 here</a> but you'll need probably some time to really read it. If you are here just for the demo of the end product you can click <a href="#demo">here</a>!
{{< /warn >}}

Welcome back! 

In the last article, I heavily focused on understanding & reverse-engineering Ultranet and getting a proof of concept working on FPGA. That was mostly about the protocol side: understanding the physical side, how data flows, timings, and wrestling with bits until both transmitter and receiver behaved correctly. 

With that milestone reached, it's time to shift gears and design a product that I would actually use in live production.

The whole point of this project is to create 8 channel stagebox for auxiliary audio lines that I will use in my live production. I recently received the dates and song list for the 2026 "tour" so timelines on multiple projects got very real 🤩! 

As discussed in part 1, there are many options on the market ([ADAT](https://en.wikipedia.org/wiki/ADAT_Lightpipe), [MADI](https://en.wikipedia.org/wiki/MADI), [Dante](https://en.wikipedia.org/wiki/Dante_%28networking%29), ...) but those are locked down and expensive. Re-using an existing protocols (like Behringer's Ultranet) is an easy way to design a futureproof(-ish) system while ensuring compatibility with many existing devices all the while learing about the intricaties of system. This makes you more aware of the limits of a setup and let's you understand why things go wrong and how to bodge said things when it breaks 1h before go-time 😢.

{{< warn >}}
Due to various reasons, I will stop reffering about my implementation as ultranet.
As it is based on AES3 which is an open standard, I doubt I will annoy Berhinger too much by publishing this project under a different name. 😅
Therefore, please welcome to the stage: <b>HyperNet</b> 🥁
{{< /warn >}}


## Quick recap

### How

As a reminder AES3 was designed primarily to support stereo [PCM](https://en.wikipedia.org/wiki/PCM) 📊 encoded audio encoded using [biphase mark code (BMC)](https://en.wikipedia.org/wiki/Biphase_mark_code).

> Biphase mark code, also known as differential Manchester encoding, is a method to transmit data in which the data 💾 and clock 🕓 signals are combined to form a single two-level self-synchronizing data stream. Each data bit is encoded by a presence or absence of signal level transition in the middle of the bit period (known as time slot for AES3), followed by the mandatory level transition at the beginning of the period.

AES3 is composed of what is called audio blocks, these audio blocks are composed of 192 frames, each frame contains 2 subframes, which in turns, contain 32 time slots. Each subframe contains a preamble, 24bit audio, 3 status bit and a parity bit.

![AES3 Block structure](diagrams/aes3-block-structure.drawio.png "AES3 Block structure")

Under the hood Ultranet/HyperNet is very close to AES3, just repackaged to fit 8 channels instead of 2 in the same timespan:

![Ultranet frame structure](diagrams/ultranet-block-structure.drawio.png "Ultranet frame structure")


{{< todo >}}
Reword and add links
{{< /todo >}}

### Where I left off

At the end of part 1, everything was technically working, but not exactly production-ready: 
- 🧮 Channel indexing is still an issue, for some reason real ultranet receiver are still not fully compatible with Hypernet.
- 🔌 The audio frontend of the DACs and ADCs were at best mediocre.
- 🧩 The PCB layout design was oriented mor as a devboard than a real product
- 📦 The project was a bare PCB without any case


## What's new ?

After wrestling with the implementation in Part 1, it was time to clean up the move beyond the spaghetti. This round of changes is all about making the design more robust, modular, and rack-friendly. In short: less "prototype held together with hopes and prayers" more "something I can actually trust".  

When I did my last PCB order I snuk-in a devboard for the [DIX9211](https://www.ti.com/lit/ds/symlink/dix9211.pdf), a `216-kHz Digital Audio Interface Transceiver`. This chip is similar to the AK4114 that's being used for almost every Ultranet product. It has some issue we'll talk about later but the sheer amout of features that this chip offer basically meant that it was a no brainer to use.

The next thing on the list is: bye-bye to the PLL1707 👋. This chip was responsible for generating the 24.576MHz system clock that the FPGA used to decode and genrate the AES3 data streams. Again, we'll talk about it later but this has been replaced by the DIX9211 which can output a bufferd clock from it's crystal!

Also new, are new modular DAC and ADC boards with proper analog frontends. This ensure flexibility, upgradability and reparability within the system. Imagine haveing to rebuild the whole board because someone blew-up an input 🤦

I'm also indroducing a small supervisor MCU. It will be used to setup everything to their proper state and interface between the FPGA and other components. This project is at it's core a 8-in 8-out signal processor so it could be used for much more than that!

A much needed improvement is a proper 1U case and CAD models to fit everything properly (okay, okay you got me, a shelf with 3d printed faceplates, I promise it looks good and feels solid 😉)

The last thing I need to mention is the move from fully opensource implementations to using built-in IPs inside my FPGA, specifically the transmitter is now using the [Gowin SPDIF TX](https://www.gowinsemi.com/en/support/ip_detail/194/) IP. While I do belive that a fully open implementation would be preferable. I also belive that using the best tools for the job is the better route to take. I'm still very novice in the FPGA world and while I could probably fix the previous implementation to make it do what I want, it's just easier to use something that already works. Also while this IP is proprietary it is free so ... 🤷

{{< todo >}}Reword{{< /todo >}}

## Electronics redesign
### DAC
For the outputs I decided to stick with the same DAC chip as in the prototype. It performed well for my application and integrated nicely with the FPGA. The big change is moving from single-ended outputs to a fully balanced design. That means cleaner audio, lower noise, and better compatibility with professional gear, especially when running long cables on stage or in a studio.

{{< todo >}}
Use of the NE5532 for single ended to blanaced 
{{< /todo >}}

### ADC
The input side follows the same philosophy: keep the same ADC chip, but redesign the analog front-end for balanced operation. As said before, balanced inputs are essential to reject interference and ground noise. This redesign transforms the prototype from a "proof it works" board into something that can actually handle real-world signals.

{{< todo >}}
Use of the OPA1677DR for blanaced to single ended
{{< /todo >}}

#### Adding phantom power

Since balanced inputs are in place, the next logical step was adding phantom power. While the new board doesn't feature any pre-amplifier to boost microphones and whatnot, I figured that adding phantom power couldn't hurt.

If I don't need it I can simply disable it, but if I want to use microphones I can simply use inline pre-amplifiers like the [Klark Teknik Mic Booster CT1](https://www.thomann.de/lu/klark_teknik_mic_booster_ct1.htm) which is a `compact dynamic microphone booster with high-quality preamps`. Super easy and pretty cheap!

It does adds some complexity (especially for the PCB which had to stay the same size to avoid re-designing CAD models), extra power regulation, proper protection circuit but it opens up much more flexible use cases. 

{{< todo >}}
Quick explaination on phatom
{{< /todo >}}

### Mainboard
#### Digital interface transciver: DIX9211
#### Supervisor MCU

## HDL redesign
### Clocks & Sync
### Receiver
#### DIX Interface
#### Demux and output ports
### Transmitter
#### I2S Receiver
#### FIFO & Gowin SPDIF TX

## Firmware design
### Reset system
### I2C bus
### DIX Configuration

## CAD Design
### Using a shelf
### DAC Holder
### ADC Holder
### Main board

## Demo
### Hypernet to Hypernet
### Hypernet to Ultranet
### Ultranet to Hypernet

## What's next
## Conclusion