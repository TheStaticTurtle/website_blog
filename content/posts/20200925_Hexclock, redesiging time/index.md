---
title: "HexClock: Redesigning time"
date: 2020-09-25T08:39:56.000Z
draft: false
featured: false
image: "images/cover.png"
tags:
    - 3D
    - DIY
    - Electronics
    - IOT
authors:
    - samuel
---

Iterating over a pre-existing design to make it better and have cool clock 

<!--more-->


First credit where credit is due. This isn't my idea I based my build around [Mukesh Sankhla](https://www.youtube.com/channel/UCFYguRGMmGpH493PDX5WmBA) design:

However, I didn't like his design: way to thick and relatively small. I own a cr-10, so I opened SolidWorks and started by drawing a 30 cm hexagon.

I slimmed down his version to a 2.5 cm thick version and the result look like this:

![](images/dl_unknown.png)
(Before printing I added some fillets and rounded some edges)

After printing and removing a lot of support it looked like this:

![](images/dl_20200906_132520.jpg)

![](images/dl_IMG_20200906_123628.jpg)

![](images/dl_IMG_20200906_123632.jpg)

I then painfully soldered 96 ws2812b in each hole. As the power supply I'm using the only one I could find and that is an old PS2 power supply delivering 8.5v at 5amps, so I separated the clock into 3 sections with 3 buck converter to step it down to 5v.

I choose the esp8266 on a wemos d1 mini as a controller because it has Wi-Fi and it's great, however if I need more power I'll switch it to an esp32.

Next was coding, for me it was start of school again and I didn't want to bring what looked like a bomb at my university, so I created a python simulator that allowed me to create animation at school:
![](images/dl_Screenshot_20200908_134225.png)
Converting the python code base to c++ wasn't that hard and most of the coding for the esp was done on [twitch](https://www.twitch.tv/thestaticturtle) with most of them saved here: [https://www.youtube.com/playlist?list=PLgOTbM7xj9ggbPVsv--_13v2cieBVQZOv](https://www.youtube.com/playlist?list=PLgOTbM7xj9ggbPVsv--_13v2cieBVQZOv)

After one week of looking at a non diffused piece of plastic I cut a plexiglass sheet and sanded the side to make a diffuser

![](images/dl_IMG_20200907_203913-1.jpg)

![](images/dl_video.png)

It still isn't perfect that's why I order some white acrylic samples to use as a diffuser and if one of them is better than what I have now I'll order a pre-cut hexagon. I might also experiment with putting some lenses on top of the LED to spread the light even more. But the best solution might just be to add a bit of thickness back to increase the currently ~5 mm space between the LED and the acrylic.

The clock connect to my Wi-Fi and respond to home-assistant via MQTT. I've set it up so that you can control the time and background part separately to allow sleeping next to the thing.
![](images/dl_Screenshot_20200915_223139.png)
Apart from that there is still a few things that need to be improved like the power distribution when using the 96 LEDs at full white and write some more animation / static backgrounds. And one led with a brightness delta to fix.

As with most of my projects it's open source so here is the code: 

{{<og "https://github.com/TheStaticTurtle/HexClock">}}
