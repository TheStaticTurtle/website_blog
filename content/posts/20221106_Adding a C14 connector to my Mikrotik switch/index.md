---
title: "Adding a C14 connector to my Mikrotik switch"
date: 2022-11-06T12:00:00Z
draft: false
featured: false
image: "images/cover.jfif"
tags: 
    - homelab
    - diy
    - electronics
    - tutorials
authors:
    - samuel
---
Recently, I bought some used mikrotik CRS326-24G-2S+RM
These switches are remarkable 1g switches for the price, but they have one flaw: they use an external power adapter
So, I decided to add an IEC C14 connector to it.

<!--more-->

Recently, I bought some used mikrotik CRS326-24G-2S+RM

{{<og "https://mikrotik.com/product/CRS326-24G-2SplusRM">}}

These switches are remarkable 1g switches for the price, but they have one flaw that some sysadmins consider a pretty big one: they use an external power adapter

## Feasibility
Mikrotik also has the same version which is a bit smaller and not rack mounted (the [CRS326-24G-2S+IN](https://mikrotik.com/product/crs326_24g_2s_in)) which makes me think the motherboard in the rack mounted version is the same :sweat_smile:

The back of the switch has an IEC C14 cutout in the metal, it's like one of their engineer knew someone was going to do this :rofl:
![enter image description here](images/dl_DSC00138.JPG)

The power adapter itself is a 24v 1.2amp one
![enter image description here](images/dl_DSC00134.JPG)
And the input on the switch specify a range of 10v to 28v, so it should be pretty easy to find a replacement power supply

Adding the IEC C14 connector was a no-brainer really, I only needed the connector and power supply.

## Parts
After a quick Amazon search, I choose this adapter, mainly because it matched the original one pretty well and was the fastest delivery one: https://www.amazon.fr/gp/product/B08P8S4SY6 
![enter image description here](images/dl_DSC00129.JPG)
I also bought these connectors: https://www.amazon.fr/gp/product/B07YTZYSTT
![enter image description here](images/dl_DSC00131.JPG)

## Wiring everything
I got some wires from an old 220v cable, soldered them to the C14 connector added some heat shrink and screwed the other side to the power supply input
![enter image description here](images/dl_DSC00136.JPG)
![enter image description here](images/dl_DSC00135.JPG)


As I predicted, 1/3 of the case is empty, leaving more than enough space for the power supply
![enter image description here](images/dl_DSC00141.JPG)
![enter image description here](images/dl_DSC00143.JPG)
![enter image description here](images/dl_DSC00142.JPG)


So, I went on and broke the little tabs, screwed in the C14 connector and connected the power supply:
![enter image description here](images/dl_DSC00144.JPG)

To actually power the switch, I hesitated between soldering straight to the board and making a wire+connector come out of the case. As the switch is already out of warranty, so I decided to solder directly to the board.

Fortunately, the PCB has some holes that I can use properly instead of soldering to the connector tabs:
![enter image description here](images/dl_DSC00145.JPG)
![enter image description here](images/dl_DSC00146.JPG)

I also added the earth from the IEC C14 to a screw that touched the chassis:
![enter image description here](images/dl_DSC00148.JPG)
![enter image description here](images/dl_DSC00149.JPG)

After a quick test to confirm, it still lighted up :fire: :
![enter image description here](images/dl_DSC00150.JPG)

I added a little piece of tape between the original connector and the case so that I wouldn't accidentally power it from here:
![enter image description here](images/dl_DSC00151.JPG)
![enter image description here](images/dl_DSC00152.JPG)

## Finishing up

And finally, I closed everything and put it back to work on my desk:
![enter image description here](images/dl_DSC00153.JPG)
![enter image description here](images/dl_DSC00154.JPG)
![enter image description here](images/dl_DSC00157.JPG)
![enter image description here](images/dl_DSC00162.JPG)

## Conclusion

All in all, this is an effortless mod that solves a relatively big issue, and I'll repeat it to the other two switches I own :smile: