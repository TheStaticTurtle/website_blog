---
slug: diy-opensource-bidirectional-sdi-to-fiber-converter
title: "Building an opensource Bidi SDI to Fiber converter"
draft: false
featured: false
date: 2024-02-17T12:00:00.000Z
image: "images/cover.jpg"
tags:
  - electronics
  - opensource
  - diy
  - video
  - concerts
authors:
  - samuel
---

Building a very affordable and opensource bidirectional 3G-SDI to Fiber converter.

<!--more-->

**WARNING: This is a stupidly long article, it details the concept, design, and construction phases thoroughly, you'll need probably more than 45 min to really read it**

Every once in a while, I have the pleasure of working with my local choir. Every few years they perform on stage featuring around 3 hours of music. In the past, my involvement was mostly behind the scenes, helping out wherever I could. However, last year, I decided to take on a more ambitious role and conduct an experiment that would elevate the entire performance.

I took every piece of video equipment I could get my hands on and set out to not only record the shows but also provide live Image Magnification (IMAG) of the band. This was a significant step up from previous years, where recording had been outsourced with mixed results. The idea was to bring a new level of engagement for both the audience and the performers, while also creating a high-quality record of the event.

The experiment turned out to be a resounding success. The live IMAG was enthusiastically received by both the singers and the audience, adding a dynamic visual element that enhanced the overall experience. It allowed those seated further back to see the intricate work of the musicians. As for the recording, the quality far exceeded my expectations, surpassing in many ways what had been achieved in previous years.

## Why

Last year's show was pretty awesome, but I always want to improve things. Something that's been bugging me in my video setup is, that, it was kind of a mess. I mean, we had HDMI cables here, SDI there, some RTSP streams, and even NDI feeds. Talk about a tech salad!

Don't get me wrong, it worked... mostly. But I had to run custom scripts before the show and more than once the IMAG showed the blank elgato logo or a freezed frame. So I kept thinking, "There's gotta be a better way to do this." 

The issue always had been the budget, I was at the time an apprentice in a different field with no contacts or knowledge in the AV production world. Video isn't exactly cheap, and it evolves very quickly, the quality always need to increase.

So for next show, I want to do one thing: simplify the heck out of my video system, specifically transport.

I started digging into different options and, there are a few contenders:

  - **NDI:** This system is pretty slick. But there is a catch, you either need fancy cameras that speak NDI right out of the box or you gotta shell out for converters that will set me back at least 300 euros a pop. Ouch!
  - **RTSP:** Now, this one's tempting. It's really good, but it's got a bit of a lag issue. And, you still need converter boxes. They're a bit cheaper though.
  - **HDMI:** It's pretty reliable but has severe length issue unless you use active cables.
  - **SDI:** Now we're talking! This is like the goldilocks of video options for me. It's not dirt cheap, but compared to the others, it's a steal. You can find affordable converters to and from HDMI, and it's used all over the place in pro setups.

But wait, it gets better! SDI's got a neat trick up its sleeve - you can easilly convert it to fiber. 

My idea is the following: an MPO-12 breakout (fancy connector with 12 fibers) and an armored MPO-12 cable. Throw in a DIY stage box, and boom! We're in business.

This setup would be like the Swiss Army knife of video transport. I'm looking at 2 fibers for 10Gb ethernet, at least 8 for video feeds, and I've even got 2 spares that I'll use for audio (maybe). 

However, the cost of fiber converters can be a hurdle, almost as much as IP converters (NDI/RTSP). For example, Blackmagic offers a 12G SDI to fiber converter priced at around 155 EUR: 

{{< og "https://www.blackmagicdesign.com/fr/products/miniconverters/techspecs/W-CONM-29" >}}

While this is a reliable and professional option, the price tag is a bit hefty for a project that’s meant to be low-cost and accessible. I don't really need 8k video, 1080p60 is more than fine for IMAG so 3G sdi will do.

Unfortunatly I couldn't find a cheaper alternative even for lower data rates. I was on the lookout for more budget-friendly alternatives, and purely by chance, I stumbled upon this post by twi_kingyo.

{{< og "https://x.com/twi_kingyo/status/1446102240633049094" >}}

The post was a game-changer for me. It showed a very crude, DIY approach to 3G-SDI to fiber conversion that was both affordable and in line with what I had been envisioning. 

As I read a bit more I immediately was like, `wait a minute, this is exactly what I want to do`

## Research

I then spent a good amount of time researching SDI, fiber, SFPs, ....

It turns out that the cheap 10Gb SFP+ transcivers I got for 8eur are relatively "passive" they take a 100Ohm differential pair for data in and data out + a few control and status pins.

As for SDI, it'a simple 75Ohm terminated singlened data stream.

All you really need is a cable equilizer for RX and a cable driver for TX. 

## First prototype

When I saw [@twi_kingyo](https://x.com/twi_kingyo) post about SDI I very quickly found the [LMH0397](https://www.ti.com/product/LMH0397) which looked prefect at first glance. The description said `3G SDI bidirectional I/O with integrated reclocker`

I very quickly designed a PCB and sent it to production:

![LMH0397 Breakout prototype](images/chrome_2024_09_16_15-56-55_3rq8lhTxRE.png)

And it worked, well partially worked.

### Stupid mistake

In my haste I didn't fully read the datasheet. While it is bi-directional in the sense that I can do both directions. It cannot however, do it a the same time.

Something that I would have seen if I read the f-ing datasheet:

> The LMH0397 is a 3G-SDI 75-Ω bidirectional I/O with
integrated reclocker. This device can be configured
**either** in **input mode** as an adaptive cable equalizer **or**
in **output mode** as a dual cable driver, allowing
system designers the flexibility to use a single BNC
either as an input or output port to simplify HD-SDI
video hardware designs.

![LMH0397 Simplified Block Diagram](images/LMH0397_diagram.png)

If I read things more carfully I would have done things differently, but it worked and that meant I had a proof of concept.

## Second prototype
The second prototype was very cost minded my target was arround 25eur per converter

The LMH0397 is a great chip but it is 18.5eur per unit in low volumes and has redundant features not needed for a simple media converter.

I spent a while searching for alternative. First thing I did is to take the reclocker out of the equation. I now needed a simple cable equalizer and a cable driver. There are a few options, for instance Texas instrument or Semtech have some interesting chips.

But the ones I choose are from microchip, the [EQCO30T5](https://www.microchip.com/en-us/product/eqco30t5) and [EQCO30R5](https://www.microchip.com/en-us/product/eqco30r5).

While these chips are marketed as HD-SDI Transmitter/Receiver, they are capable of up to 3Gbps Video. They also seem to be able to be used for a data backchannel and power over coax. This won't be of any use for me tho.

### Schematic
The schematic (at least the intersting parts) is based on the typical application circuit of both schematic. 
Compared to the LMH0397, the EQCO30T5 and EQCO30R5 are super simple to connect.

![Version 2 prototype EQCO30T5 schematic](images/chrome_2024_09_16_16-20-12_7CZVtUYs49.png)
![Version 2 prototype EQCO30R5 schematic](images/chrome_2024_09_16_16-20-36_rW5pAelcwh.png)

### PCB
This is the first prototype with the appropriate dimentions, my plan was to fit everything into a 1U case (fiber splitter, converter modules, ...). This means it has to be at most 45mm tall but decieded that my target would be 35mm. This would leave enought space for the chassis, mounting & cables.

![Version 2 prototype render](images/chrome_2024_09_16_16-16-49_d7eqsZauTm.png)

### First test
Once I received the PCBs I imediatly soldered four chips on two separate boards. Powered them up and amazingly there wasn't any magic smoke! 

I then screwed in SMA to BNC adapters and connected my HDMI-SDI & SDI-HDMI converters. Same as before, to avoid destroying a SFP+ module, I took a 1m DAC cable and connected the two boards.

And it worked! I got a picture on my monitor!

**DEMO** **DEMO** **DEMO** **DEMO** 

### Issues for longer distances

Using a 1m DAC is fine and all but the goal is at least a 50m distance. 
To start things out, I used a 15m cable and it still somewhat worked !?

I used jellyfin to play videos on the output and misteriously, while I had the window in the foreground everything was fine, no issues at all! But, as soon as I clicked else-where, the link crashed and would not come back up.

**DEMO** **DEMO** **DEMO** **DEMO** 

While it did try to sync, using my 50m fiber didn't show any picture in any condition!

As I will discover later, this wasn't really caused by something I did (my bad PCB design I probably didn't help tho).
But at the time I thought it was the "cheap" chips I was using so I started a new prototype

## Third prototype



### Issues for longer distances still present
### Possible fix for said issue?
### Oh, f---, that was the issue!

## Fourth prototype / Final versions

### "Normal" version
### "Reclocked" version