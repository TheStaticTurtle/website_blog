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

Every once in a while, I work in my local choir. Every few years, they do a tour singing music for around 3h. With previous shows I simply help wherever I could. Last year however, I decieded to run an experiment, I took every piece of video equipment I had, and recorded the shows. I also provided live IMAG of the band.

The experiement went very well. The IMAG was well received by both the singers and public. The recording also went very well and way better than what was out-sourced previous years.


## Why

For next shows, I want to do better. One of the way I plan to do that is video transport. The way I did previously was completly random, I had a mix of HDMI, SDI, RTSP, and NDI. I want to simplify all of that.

To do that I have a few options:
  - **NDI** is a great option but you either need cameras that can output it directly or need converts, most of them costing at least 300eur
  - **RTSP** great option, free to use license but latency can be an issue and also need converter boxes (bit cheaper tho)
  - **HDMI** excellent but only for short distances
  - **SDI** cheap compared to other options, affordables converters to and from HDMI and used a lot.

SDI can also be converted to fiber which is a very good option for me. I'm planning to use an MPO-12 breakout and an armored MPO-12 cable with a DIY stage box.

That will give me 2 fibers for 10Gb ethernet and at least 8 fibers for video (with 2 spares).

However, the cost of fiber converters is quite prohibitive, blackmagic has a 12G converter for 155eur:

{{< og https://www.blackmagicdesign.com/fr/products/miniconverters/techspecs/W-CONM-29 >}}

That is still a bit much.
Compltly randomly I stumbled onto this X post:

{{< og https://x.com/twi_kingyo/status/1446102240633049094 >}}

And I imediatly was like, `waita minute, this is exactly what I want to do`

## Research

I then spent a good amount of time researching SDI, fiber, SFPs, ....

It turns out that the cheap 10Gb SFP+ transcivers I got for 8eur are relatively "passive" they take a 100Ohm differential pair for data in and data out + a few control and status pins.

As for SDI, it'a simple 75Ohm terminated singlened data stream.

All you really need is a cable equilizer for RX and a cable driver for TX. 

## First prototype

When I saw [@twi_kingyo](https://x.com/twi_kingyo) post about SDI I very quickly found the [LMH0397](https://www.ti.com/product/LMH0397) which looked prefect at first glance:

> 3G SDI bidirectional I/O with integrated reclocker

I very quickly designed a PCB and sent it to production:

**TODO**

And it worked, well partially worked.

### Stupid mistake

In my haste I didn't fully read the datasheet. While it is bi-directional in the sense that I can do both directions. It cannot however, do it a the same time.

Something that I would have seen if I read the f-ing datasheet:

![LMH0397 Simplified Block Diagram](./images/LMH0397_diagram.png)

**BUT**, I had a proof of concept 

## Second prototype
The second prototype was very cost minded my target was arround 25eur per converter
### Issues for longer distances

## Third prototype

### Issues for longer distances still present
### Possible fix for said issue?
### Oh, f---, that was the issue!

## Fourth prototype / Final versions

### "Normal" version
### "Reclocked" version