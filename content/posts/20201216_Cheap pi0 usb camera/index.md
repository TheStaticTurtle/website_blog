---
title: "Dirt cheap DIY USB Camera"
date: 2020-12-16T15:24:42.000Z
draft: false
featured: false
image: "images/cover.jpg"
tags:
    - DIY
authors:
    - samuel
---

A little after that every blog was popping with the uvc-gadget script to turn your pi4/pi0 into a high quality USB camera. [...] And so at 2am it was decided I was making a webcam

<!--more-->


A while ago I have seen all the excitement over the pi camera HQ but at around €50 it was still a bit too expensive to justify buying it just because I could. Shortly after that of course the pandemic hit and there was a massive shortage of USB cameras. A little after that every blog was popping with the uvc-gadget script to turn your pi4/pi0 into a high quality USB camera. 

I have to agree that for the price of around €60 you could get a superb USB camera compared to the other options on Amazon for example. (That was still too expensive for me mind you)

I had a pi0 lying around for a while now, an old pi camera v1 that bought out of AliExpress for really cheap (it was like 5-7€) I also had an old 70 mm CCTV camera lens from old projects. 

And so at 2am it was decided I was making a webcam, the software part was really simple, install Raspbian and install the uvc-gadget. I personally followed this tutorial:

{{<og "https://www.jeffgeerling.com/blog/2020/raspberry-pi-makes-great-usb-webcam-100">}}

Now having everything (cables and all) hanging around isn't pretty, so I spend some time and design a nice case for everything

{{< gallery >}}
images/dl_SLDWORKS_2020-12-16_13-36-59.png
images/dl_SLDWORKS_2020-12-16_13-37-34.png
{{< /gallery >}}

After some 15h of printing here's what I got:

{{< gallery >}}
images/dl_IMG_20201215_165508-1.jpg
images/dl_IMG_20201215_190526-1.jpg
images/dl_IMG_20201215_191925.jpg
{{< /gallery >}}

After struggling quite a bit to glue, solder and fix everything in place I had this wonderful case:

{{< gallery >}}
images/dl_IMG_20201215_191937.jpg
images/dl_IMG_20201216_023114.jpg
images/dl_IMG_20201216_023022.jpg
{{< /gallery >}}

Works pretty great, the pi0 get a little warm hence I left the heat sink apparent on the backside. I also left a groove to put some addressable LEDs to light up whatever I'm recording (haven't received it yet).

The little jig that I 3d printed to adjust the assembly works pretty well, I would however, should have it a little more thick, tends to bend a little. I tested it on my microphone stand where I can do stupid things like put it +2m high.

Here's my "BOM"
| Item | Price |
|------|-------|
| Pi0 | 5€ |
| PiCamera V1 + Pi0 Flex cable | ~8€ |
| Random screw found in my drawer | Free |
| Filament | ~100g |
| Lens | Free (Found one for ~10€ tho) |
| **Total** | **~25€** |

All in all I think this camera is great if you're in a pinch but isn't ideal, the pi camera v2 would be a better choice for example and maybe a better lens.

However, considering the cost I can't find a real alternative with 1080p 30fps with a 70 mm zoom.

This is a really short post, but it's the first one in the camera space for which I have a **lot** more ideas that I'll probably write and the introduction of uvc-gadget helped me quite a bit for the next camera project. This space is evolving a lot, so it might be awhile until the next camera post.
