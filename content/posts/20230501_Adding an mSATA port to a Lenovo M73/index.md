---
title: Adding an mSATA port to a Lenovo M73
slug: adding-an-msata-port-to-a-lenovo-m73
date: 2023-05-01T02:02:02.000Z
draft: false
featured: false
image: "images/cover.jpg"
tags:
    - Homelab
    - Servers
    - Electronics
    - DIY
authors:
    - samuel
---

Adding a mSATA port to the motherboard of a Lenovo ThinkCenter M73 to enable me to add High Availability to my homelab.

<!--more-->

The Lenovo M73p is part of the ThinkCenter line of business-oriented desktop computers designed, developed by Lenovo. ThinkCentre computers typically include mid-range to high-end processors, options for discrete graphics cards, and multi-monitor support.

Generally, business-oriented desktop computers have different sizes for each model. I'm particularly interested in the tiny ones.
They have been made popular by the [Tiny/Mini/Micro](https://www.servethehome.com/introducing-project-tinyminimicro-home-lab-revolution/) project published on [ServeTheHome](https://www.servethehome.com/).

To summarize, the idea is that there are plenty of technologies where one would want several physical nodes. In my case, the end goal is a HA setup for Proxmox VE.

Aside from the fact that having multiple nodes is obviously better for HA, theses small servers usually don't use a lot of energy, which today is a pretty good thing 💰. My four M73p consume somewhere between 60-85 WH depending on the load. Way better than one server powerful which might not be enought for everything that will consume +150 WH and won't have any HA 😕.

They also can be found for very cheap, I bought my nodes for somewhere between €60 and €90 each.

Of course, they have some downside:
- Small, means that you don't fit a lot in there:
	- 2.5” drive for older models, NVMe only for newer ones
	- Some models have a PCIe interface use for a dedicated GPU and. [A user managed to fit a 10GbE network card](https://www.reddit.com/r/homelab/comments/sfkz8b/incredibly_happy_with_my_completed_sff_home_lab/), but models that do have this interface are often 2x / 3x the price of what I paid for my nodes
- Limited upgradability:
	- The M73 has only two Mini-DIMM slots for ram
	- Only one SATA port
	- Some models (including the M73) have CPU sockets, **but** they don't accept every CPU, and some are locked
- Only one 1 GbE Ethernet.

That being said, they are very capable machines, way more than I need for my homelab, especially if I have 4 of them.

In my homelab I'm planning to experiment with Ceph, or maybe GlusterFS which means data will be on the nodes themselves.

High Availability, however, requires at least two things that this computer lacks:
 - Two disk  (one for the OS, on for the data), there is a trick to run Ceph on a disk partition, but I would like something “stable”
 - High-speed networking, for me, I don't think I require that much IOPS, So I think I'll go with 1Gbe for the proxmox cluster and 2.5Gbe for the Ceph cluster.

In this article, I'll fix the two disk issue.

## Options for multiple disks
There are multiple options that I considered, I wanted to leave the internal SATA port for a SSD for the data of Ceph cluster. That didn't leave many options for the OS:
 - USB 2.0 Key bodged to an internal header
 - USB 2.0 SSD bodged to an internal header
 - USB 3.0 Key plugged in the back
 - USB 3.0 SSD Plugged in the back 

I canned the USB Key solution pretty quickly, unlike OSes like Unraid where there is barely anything written to disk, Proxmox writes quite a lot which would destroy the key very fast.

I also wanted to avoid using the USB3 port because I planned to use these (or at least one of these) for the Ceph network and didn't want to have to share the bandwidth.

The last solution was the USB 2.0 SSD bodged to an internal header, which would work, and I would have probably done it if I didn't notice the mSATA  port 🤔.

##  mSATA?
When you look at the M73 motherboard, you can see an obviously missing footprint marked MSATA1 right next to the Wi-Fi slot:
![M73 Motherboard M-SATA port](images/dl_pn_2022-12-30_00-29-55_2b332c9f-56d0-4747-a1dd-108fa297efe8.png)

Which got me thinking. Could it be as simple as soldering a connector and plugging in an SSD?
Tried soldering one and of course it didn't work 😑, that would be too easy.

## Adding the mSATA Slot
After some research, I found that there are some M73 models that have a mSATA port, which makes this possible. So, I dug a little more.

I first [found a video from someone who successfully modded the motherboard](https://www.youtube.com/watch?v=jEt6l2MREfc) and IT WORKED, I got really excited and dug even more. I then found what, I believe, is the source of this mod: https://kknews.cc/digital/earlzm4.html. Turns out, all it needed was a few more passives and moving a resistor.

### Parts list
| Designation | Value| Package |
|-------------|-------|-------|
| C1, C2, C3 | 0.1uF | 0402 |
| C4 | 220uF | 6.3 mm |
| C5 | 330pF | 0402 |
| R1 | 8.2k | 0402 |
| R2,R3,R4,R5,R6,R7 | 0 Ohm | 0402 |
| Q1 | 2N7002/MOS-N | SOT-23 |
| L1 | 1uH | 0603 |
| MSATA1 | TE Connectivity 1775838-2| Mini PCIe, 52 Contacts, 0.8 mm, Receptacle, Surface Mount, 2 Rows |

### Top side
On the top side, there are only three components. The inductor is pretty easy to solder, the cap, however, was a nightmare, I could not solder to that ground plane. The mSATA connector looks painful but with some solder paste, hot air, and a bit of rework with a fine point tip, flux, and solder wick, it's actually pretty easy
![Motherboard top-side components.](images/dl_DSC00540.JPG)

### Bottom side
Bottom side is pretty easy, even for 0402, I replaced 0 Ohm resistor with wire bridges and swapped the resistor with some hot air. Not the prettiest job, but it should work.
![Motherboard bottom-side components.](images/dl_DSC00558.jpg)

## Testing
 After everything was soldered, I put a 128 GB SSD in the new slot, plugged a VGA cable and power and quickly hopped in the BIOS
 ![SSD Installed in the motherboard.](images/dl_DSC00528.JPG) 

![SSD detected in the BIOS](images/dl_DSC00610.JPG)

I made sure the SSD was detected AND IT WAS 🥳 and quickly powered it off again because I didn't have the cooler installed.

I then put everything back together and also took the opportunity to clean the cooler and changed the thermal paste.

Finished by installing proxmox and that was it:
![Disk list in proxmox](images/dl_chrome_2022-12-30_02-07-42_dabdd681-b815-404e-9059-4510d3acbda4.png)

Booted just fine, both disks are detected. To finish things off, I did some benchmarks: 
```
root@pve4:~# hdparm -Tt /dev/sdb
/dev/sdb:
 Timing cached reads:   17150 MB in  1.99 seconds = 8597.18 MB/sec
 Timing buffered disk reads: 428 MB in  3.01 seconds = 142.02 MB/sec
```
```
root@pve4:~# dd if=/dev/urandom of=/tmp/output bs=16k count=10k; rm -f /tmp/output
10240+0 records in
10240+0 records out
167772160 bytes (168 MB, 160 MiB) copied, 1.17751 s, 142 MB/s
```

## Conclusion
I'm very pleased with this mod 😀, seems a bit dodgy but if the soldering's good, there is no reason it will pose any issue. Moreover, ⁣`142.02 MB/s` read and `142 MB/s` write not bad at all, way better than what a USB 2 key will do 🤣.

Now I just have to do the same mod to the 3 other thinkcenter 😭.