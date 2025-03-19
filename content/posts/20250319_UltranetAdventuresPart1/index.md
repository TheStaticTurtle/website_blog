---
slug: ultranet-adventures-part-1
title: "Ultranet adventures part 1: Working prototype!"
draft: false
featured: false
date: 2025-03-19T09:00:00.000Z
image: "images/cover.jpg"
tags:
  - electronics
  - opensource
  - diy
  - audio
  - concerts
authors:
  - samuel
thanks: 
  - christian-noeding
  - geoffrey
  - romain
---

Deep-diving into ultranet and re-implementing both a receiver and transimtter on FPGA.

<!--more-->

{{< warn >}}
This is a stupidly long article, it details the different phases thoroughly, you'll need probably some time to really read it
{{< /warn >}}

## Why

In my last article about the opensource SDI to fiber converter, I briefly talked about my brand new MPO-12 cable with 12 OM3 fibers.
I've also hinted that I might use the two spare fibers I had for audio.

When I first started this project there were three "mainstream" ways I thought I could do this:

- [S/PDIF (Sony/Philips Digital Interface)](https://en.wikipedia.org/wiki/S/PDIF) (or it's proffestional big brother [AES/EBU](https://en.wikipedia.org/wiki/AES3)) is a type of digital audio interface. The signal is transmitted over various connectors, or even fibre-optic cables. This would be the most obvious option, AES3 can already be transmitted over fiber so it wouldn't be that difficult to adapt it to OM3 with an SFP module for example.
    - The main upside is that there are plenty of modules that already exist to convert analog to digital and vice-versa
    - The main downside is that it is only two channels per link
- [ADAT Lightpipe](https://en.wikipedia.org/wiki/ADAT_Lightpipe) Lightpipe uses the same connection hardware as S/PDIF: fiber optic cables (hence its name) to carry data, with Toslink connectors and optical transceivers at either end. The main difference stems from the fact that ADAT supports up to 8 audio channels at 48 kHz, 24 bit.
    - The main upside is that 8 channels is plenty
    - The main downside is that from some quick reasearch there isn't a recent IC or implementation that exists and devices that implement the protocol cost way too much for my use.
- [Dante](https://en.wikipedia.org/wiki/Dante_(networking)) / [AES67](https://en.wikipedia.org/wiki/AES67), they are a combination of software, hardware, and network protocols that delivers uncompressed, multi-channel, low-latency digital audio over a standard Ethernet network using Layer 3 IP packets.
    - The main upside is that there are plenty of channels (max 512), it's easy to **use** and it's implemented on a bunch of devices
    - The main downside is that implementing it to get low latency is going to be a nightmare


I didn't really like any of these, I did try to build a prototype ADAT board based on the AL1401/A1L402 ICs but I didn't have any luck.

Then the universe dropped this gem from Christian Noeding:

{{< og "https://www.youtube.com/watch?v=c7VGjq9yp8g" >}}

And this is really what kickstarted the whole thing. From the video, it seemed that Ultranet is somewhat based on two AES3 signals each containing 8 channels.
This would mean either 8 channels bi-directional or 16 uni-directional. 
Moreover I do have (limited) access to hardware that can send and receive ultranet so I can easilly test my implementation.

Pretty good so lets get started.

*Note: for the story's sake events and discoveries aren't neccesarally in chronological order.*

## Research

As always I did some research, this part also contains discoveries I made along the project.

### AES/EBU

I mentioned that ultranet is based on AES/EBU so let's start there, how the hell does this work.
Well AES3 is a standard, related standards include IEC60958 and AES-2id

{{<todo>}} More information is need on the specification other documents {{</todo>}}

#### Electrical

AES3 can by transmitted over two main kinds of connections:
- **IEC60958 Type I**: It uses balanced, three-conductor, 110-ohm twisted pair cabling with XLR connectors. Type I connections are most often used in professional installations and are considered the standard connector for AES3
- **BNC connectors**: AES/EBU signals can also be run using an unbalanced 75-ohm coaxial cable. The unbalanced version has a very long transmission distance as opposed to the 150 meters maximum for the balanced version. The AES-3id standard defines a 75-ohm BNC electrical variant of AES3

{{<todo>}} More information is need on voltages and impedances of the different methods {{</todo>}}

#### Encoding

AES3 was designed primarily to support stereo [PCM](https://en.wikipedia.org/wiki/PCM) encoded audio in either [DAT](https://en.wikipedia.org/wiki/Digital_audio_tape) format at 48 kHz or [CD](https://en.wikipedia.org/wiki/CD) format at 44.1 kHz. No attempt was made to use a carrier able to support both rates; instead, AES3 allows the data to be run at any rate, and encoding the clock and the data together using [biphase mark code (BMC)](https://en.wikipedia.org/wiki/Biphase_mark_code).

Biphase mark code also known as differential manchester encoding, is a method to transmit data in which the data and clock signals are combined to form a single two-level self-synchronizing data stream. Each data bit is encoded by a presence or absence of signal level transition in the middle of the bit period (Known as time slot for AES3), followed by the mandatory level transition at the beginning. The code is also insensitive to an inversion of polarity

![Differential_manchester_encoding](images/Differential_manchester_encoding_Workaround.svg.png)

Unlike the diagram on top, AES uses the BMC variant where the codes makes a transition for 1 and no transition for 0.

Differential Manchester encoding has the following advantages:
- A transition is guaranteed at least once every bit, for robust clock recovery.
- If the high and low signal levels have the same magnitude with opposite polarity, the average voltage around each unconditional transition is zero. Zero DC bias reduces the necessary transmitting power, minimizes the amount of electromagnetic noise produced by the transmission line, and eases the use of isolating transformers.

These positive features are achieved at the expense of doubling the clock frequency needed to encode the data stream.

{{<todo>}} This chapter needs re-writting to make it easier to understand {{</todo>}}

#### Blocks, frames, time slots

Now that we know of bits flows let's talk about what those bits actually mean!

AES3 is composed of what is called `Audio blocks` these audio blocks are composed of 192*`Frames` each frame containes 2*`Subframes` which in turns contain 32*`Time slots`

![](images/SPDIF_AES_EBU_protocol_colored.svg.png)

{{<todo>}} Needs better graphics to explain this {{</todo>}}

A subframe is composed of:

| Time slot     | Name                        | Description                                                                                                                    |
| ------------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| 0–3           | Preamble                    | A synchronisation preamble                                                                                                     |
| 4–7           | Auxiliary sample            | A low-quality auxiliary channel used as specified in the channel status word.                                                  |
| 8–27          | Audio sample                | Audio sample stored MSB last. Can be extented to use the auxiliary sample to increase quality                                  |
| 28            | Validity (V)                | Unset if the audio data are correct and suitable for D/A conversion. .                                                         |
| 29            | User data (U)               | Forms a serial data stream for each channel.                                                                                   |
| 30            | Channel status (C)          | Bits from each subframe of an audio block are collated giving a 192-bit channel status word.                                   |
| 31            | Parity (P)                  | Even parity bit for detection of errors in data transmission. Excludes preamble; Bits 4–31 need an even number of ones.        |

The preamble can be one of three values:

|  Name  | Bits (Last was 0) | Bits (Last was 1) | Function                                                                     |
|:------:|:-----------------:|-------------------|------------------------------------------------------------------------------|
| Z or B |      11101000     |      00010111     | Marks a word for channel A (left) at the start of an audio block             |
| X or M |      11100010     |      00011101     | Marks a word for channel A (left), other than at the start of an audio block |
| Y or W |      11100100     |      00011011     | Marks a word for channel B (right).                                          |

#### Practical example 

That's a lot to take in so let's look at a practical example from my logic analyser:

![Logic analyser capture of an AES3 signal](images/DSView_2025-03-19_16-07-30_cee0854c-4d4e-4325-bd1f-56633cf9dca8.png)

Let's see what we can figure out:
- This subframe starts with the B preamble, this tells us that it's the **start of an audio block** and that it's the **left** channel.
- We are going to consider that the auxiliary bits are use for audio, if we change the bit order from LSB-first (AES3) to MSB-first (what is generally used for audio) the 24bit **audio data is 0xffffb5**
- Even tho we have data the validity bit tells us that **this frame is invalid** and that it shouldn't be played
- Then comes the user bit with an undefined structure
- The is the channel status word, this tells us that the first bit of the word is **a 0 indicating S/PDIF data**
- Finnaly the parity bit **is 0** because the number of asserted **bits in the 4-30 range is already an even number of 1s**

And that's it really, the M preamble will then be used for the rest of the left channel subframes and the W will be used for the right channel. 
Then after 384 subframe, there will be an other B preamble signaling a new block.

### Ultranet

Now how does ultranet differs from AES3?

{{<warn>}}As there is no official documentation that is publicly availible (or any leaks for that matter), everything that not straight out of a product sheet is informed speculation, reverse-engeinerring and trial & error and might not reflect excatly the actual protocol{{</warn>}}

#### What we know from product sheets:

- **Digital Processing**
  - **A/D conversion:** 24-bit, 44.1 / 48 kHz sample rate
- **System**
  - **Signal:** 16 channels, plus bus-power for P16-HQ
  - **Latency:** <0.9 ms (from P16-I to P16-HQ)
- **Cabling**
  - **Connectors:** RJ45
  - **Cables:** Shielded CAT5
  - **Cable length:** max. 246 ft / 75 m recommended


#### What we know from reverse-engeenering and probing 🍑

AES3 The hardware interface is usually implemented using RS-422 line drivers and receivers.



## Building a dev-board
### Board bring-up & mistakes

## Blind implementation
### Transmitter
### Receiver
### Alllll the channels
### It's working ?

## Testing on real hardware
### Transmitter
### Receiver
### Transmitter again
#### Oh, f---, that was the issue!
### It's working (encore) ?

## What's next

## Conclusion
