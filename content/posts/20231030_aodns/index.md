---
slug: aodns-the-monstrosity-that-now-exists
title: "AoDNS - The monstrosity that now exists"
draft: false
featured: false
date: 2023-10-30T12:00:00.000Z
image: "images/cover.png"
tags:
  - audio
  - open source
  - experiments
authors:
  - samuel
---

AoDNS, is a monumental monstrosity specifically designed to spread chaos among network engineers by streaming live audio via DNS queries

<!--more-->

## Why ????

The story about how I thought that tunneling audio over DNS and how I actually started working on it is idiotic.

A few weeks ago, I went on an 8h flight to the US for work 🛫. 3 Days before I reminded myself that I needed to find a solution for me to be able to listen to music on the plane.
My phone is pretty old, it's an OnePlus 5T 64g version, and, unfortunately, this model does not support SD cards and currently has less than 1g of free space, a complete pain.

I listen to all my music on Spotify and with less than a gigabyte of free space I wasn't about to download my playlist locally 😥.

Just as was about to leave work that day, I remembered that many airplanes (especially international ones) offer an internet service. 
When you connect to their Wi-Fi it will ask you to either log in or purchase an internet plan and I thought, there's no way they are blocking DNS queries even if you don't pay 🤔.

That's when I thought, maybe, just maybe, if I were to encode audio and put it in DNS records I would be able to stream audio. I then messaged a few friends about this idea, and, as expected, they agreed that it was stupid and then left work and got in my car.

But then because my brain is weird, I couldn't stop thinking about how I could implement it, and at the end of the ride I had a pretty good idea how to implement AoDNS.

But then, my brain, still being peculiar, decided that it would be better to write code for 7h straight to write a proof of concept and go to bed at 4am while having work in the morning instead of going to sleep 💤.

## How does it work
I'll spare you all the details because between my 7h rush and the actual version, quite a few things changed and improved. 

Most of the code is written in such a way that it would be straightforward to implement new functionalities like, for example, encryption 💪.

Here is how I made everything work:

### Audio & Compression
I needed a simple way to get audio in and out and, as I wrote this in python I chose the easy way and used pyaudio. However, all the audio collection happens in a class that inherits from a base class, meaning that it would be trivial to add another way of inputting or outputting audio assuming that it supports arbitrary raw pcm frame lengths.

As raw pcm takes quite a bit of space, if I wanted to even have hope of making this work, I needed to compress/decompress it 📚, my default choice (and the one I stuck with) is to use opus. [Opus](https://opus-codec.org/) is an open audio codec design for transmitting audio over the internet. It can use very low bitrates and a wide variety of sample rates & frame sizes. As a bonus, it's super simple to use.

If the audio is voice only, [Codec2](http://www.rowetel.com/?page_id=452) might also be an adequate option for even lower data usage. A quick calculation result in 163 bytes for 1sec of audio 😲.

Most codecs require a specific frame size, opus for example, is calculated like this: `60 * rate // 1000`. This is why it cannot be changed. Instead, it's queried during initial setup and re-used by the audio streamers.

What will adjust the amount of data collected is the sample rate and channel count. Theses are configurable when starting the example.

My goal for this project was to get 8kHz 1ch working. As you can see in the following table, compressing data to Opus is pretty good, in general, the output is only 6% of the input.
One thing to note is that, for Opus, the size of the compressed data isn't fixed and varies following the input signal 🔊.

| Codec | Activity | Sample rate | Channels | Data size - PCM | Data size - Compressed | Ratio |
|-------|-------|-------------|----------|-----------------|------------------------|-------|
| Opus  | ❌   | 8000 Hz     | 1        | 960 bytes       | 39 bytes               | ~0.04  |
| Opus  | ❌   | 8000 Hz     | 2        | 1920 bytes      | 93 bytes               | ~0.048 |
| Opus  | ❌   | 16000 Hz    | 1        | 1920 bytes      | 75  bytes              | ~0.039 |
| Opus  | ❌   | 16000 Hz    | 2        | 3840 bytes      | 134 bytes              | ~0.034 |
| Opus  | ✅   | 8000 Hz     | 1        | 960 bytes       | 52 bytes               | ~0.054 |
| Opus  | ✅   | 8000 Hz     | 2        | 1920 bytes      | 120 bytes              | ~0.062 |
| Opus  | ✅   | 16000 Hz    | 1        | 1920 bytes      | 94  bytes              | ~0.048 |
| Opus  | ✅   | 16000 Hz    | 2        | 3840 bytes      | 231 bytes              | ~0.06  |


## Storing the data

As I said, the plan is to store the audio data in TXT queries. To keep everything compatible with the outside world, I choose to store the data as ASCII 👨‍💻. There's also some option to consider here:

| Algorithm | Input size | Output size | Ratio |
|-----------|------------|-------------|-------|
| Base16    | 256 bytes  | 512 bytes   | x2    |
| Base32    | 256 bytes  | 416 bytes   | x1.63 |
| Base64    | 256 bytes  | 344 bytes   | x1.34 |
| Base85    | 256 bytes  | 320 bytes   | x1.25 |
| Base91    | 256 bytes  | 315 bytes   | x1.23 |

To maximize the amount of data I could store in one record, I decided to use base91. It's not too obscure and still does a pretty good job.

One issue I stumbled on early is that TXT strings are limited to a max of 255 characters. Which, for me, roughly equates to 200 bytes of data after the base91 step.

The DNS server can easily bypass this limitation by simply answering multiple TXT strings 😏. My local responder (Windows server 2022) could handle around 3 KB of data in one record before it simply stopped responding.

One issue that arises when sending multiple strings is that the first answer you get from the responder might be ordered correctly, but, at least with Windows server, the second one won't be and instead will be in a randomized< order 😭. 

To solve this, I added an incrementing prefix to each string. The prefix is separated from the actual data by using `'''` which is one ASCII char that is not used in the base91 table.

After all of these steps, you can query a record and get a response like this one:
```dig
# dig +ttlunit TXT seq_49680.music.example.com

;; ANSWER SECTION:
seq_49680.music.example.com. 21s IN TXT  "003'''8U|7E/J`Cc82|8XLpLk^T__5uf~F8PN7~Mfa(E^>WsjNBHV(<2AF|H<us_*}Dyt68)v%:^`<w?&OxM}_ZUf6S&KTbCtFQp$sD!]*a\""
seq_49680.music.example.com. 21s IN TXT  "001'''8U{OOU8]UVh.PiU!N=6WJ3k@>+fl&&<`>SnpY4Tzo_%W(Z_rs)@jzY1x|abYVng=d^vUg5cY\"+K~@OsihU3cxIyz+&MMQu!m,>=dHbsaD"
seq_49680.music.example.com. 21s IN TXT  "004'''rXSKF[23x}`Z!lP@HP8lDSWPhw^ViX!^CZHUgV9m=p}~kb5yk89@f*4/%Kk_!c2[{|\"d,~?B:u|RltK]Ce]t0zf5S{h6H;W"
seq_49680.music.example.com. 21s IN TXT  "005'''8Uy]!Pn!e%1J&xz;V,~d@7J%Ca#ct]D7B^U?u4|],2IE]7ZuE$9;2n;V~{UmwB8P;)=cU/LSdxGvNn>{PoBFUHx:&4]jrS^aDu{ve7)\"EU"
seq_49680.music.example.com. 21s IN TXT  "006'''8Uy]jZ/.]MJLfG%lrc[5FJuJ8$Ixk9VfRjLsLg*Hc`P!x1sHSZpIv5%Rf%|DfXm]%Lr}B%$lRn1oYmOZ+C|sM9bZi6&H+$NipeyS<>|bVvT"
seq_49680.music.example.com. 21s IN TXT  "007'''8Uq&l<\"!uR/i})@E]<TsXZ%0&ulQ%YB|p97tmV)mA|8[+M3;~G`XSu*cKo^Yg`Mq:JAiR{W*x`9mHe>e&?LfsL1!boJ^&\"[PPER0.("
seq_49680.music.example.com. 21s IN TXT  "008'''rX%=qo9rl2P@`BC!>T,O>(+ZU?hp}]WQT^MGki99SL18Ho[!yUL4]6jgEM*5eqkhMLs}fIwx&5N*^&XJv#0zG:5@vtC8|>[cO(.U_^WeFNFB"
seq_49680.music.example.com. 21s IN TXT  "009'''rX%=Ai]%`3:7z5swE1HMB9BS+7Wv@7\"w+nYNl&\"M_Z*6=T<p>Zp?Kwo|M},B;$Uwf`c~UrkLbUDuk8H69%},V}X>Ja~QRD"
seq_49680.music.example.com. 21s IN TXT  "010'''rXKK!74bs7GWw.mBS/@NVj7gCgGy_@sv*9+]tTvB;6a|*N*6Lr.fDcyb&sH2(f=_#zV?^Tb@H)De]<j^.4?3])hA"
seq_49680.music.example.com. 21s IN TXT  "011'''rXSK]\"hAk4R.zCnc{\";RBm[~,Kgl`kB]sxx^b=9PW&n.sK~1MWbOd[E:IdL`6Y%*3@>?`M2Sh^cmAH~3]3;[uJl`>5ITZUK5\"m!C"
seq_49680.music.example.com. 21s IN TXT  "012'''rX%=M5c+YU5JS`di#g7xy=;n~TrBLt*5FFhWpQ\"S#li//^[1xA*Wgsd]l+K~F1znI;<y30[Y2!A\"OlDY:d[)8_DAC"
seq_49680.music.example.com. 21s IN TXT  "013'''rXn;Erky{T>_HKk<OV2UD?wyYfEWMgbsJ?/HV;nMW,]`<O9Z*Wp[}<Z0n0.J4(KmD:(by2/187?oOsuL3_3}bUE2`xNjX[E1h4v%r\""
seq_49680.music.example.com. 21s IN TXT  "014'''8U{O%;Nl>EKbAo.w2?@(HJzsf(Ip9|Ac`rg1>hS!7tS(Uw68%gO#8M(Vf7>EZ.yN;zElg[Ga7(?_lMw%0y#d:oAa&)|6T3A>lB"
seq_49680.music.example.com. 21s IN TXT  "015'''}AP;v[(v.gHQHsjlM/I{`60)WHD9^ia*<Lgq&5.iY9lM8$::#;zCp)06W<lE>xi9.T;]hd3$!aKaCmhG8G7wR#D[<nZZJ<WP$"
seq_49680.music.example.com. 21s IN TXT  "016'''rX%=Nm;nn6uRG<,JM:A5/sQJ~>qB/<o:iu^\"sX]Z`n)oHv9lzqP%VEM5OsBW8LEP1mK\"CLAcDrK.|8%s)~)V%h33Kr,8$ba|KvB"
seq_49680.music.example.com. 21s IN TXT  "017'''rX$gRf8^ooNsOpLYL5Zy@(5%,j^*qG3K|L}/]G&#^1#;o]mRRiH13zyw_^jZ#w2%s`6Qg.wQDR<h?MAQ6!`43ov]+Ez&75b<?k0BH34QE"
seq_49680.music.example.com. 21s IN TXT  "018'''8U+O@Nv/(&nR|5&kW$m6}laH`p<Zp|LCx{t_lc1;!U6:.k!>.7I8`<y?*a#?(SvK@gRwV&WYs@gdzNOHc4<cst4>cBHw[/oG*E9@FZ=CN"
seq_49680.music.example.com. 21s IN TXT  "000'''8U{O#xvTKUK{a)`$*k0t`OwPP$B+(Ogky5*um7:PR2$UN1Q.{J!NZGWJ1~n=].^osw7&qGSY=sw)]WptNCJ;fO4e}d4ybQIXTTt]on*E"
seq_49680.music.example.com. 21s IN TXT  "002'''8U4}l=%kj@6Ph3j9aZJO*qQ,2R*m2z[Kp.;h:%m6);/CR)8J4l}Im9IU5)H+KGLT4T`,(Jt}JwBmEqxMw7[pCUYPO,8>T^9jl.[:w6)EG"
```

The above example is 19 frames of 16kHz 1ch 16bit audio, which stores just a bit more than 1sec of audio 🎶. Perfect.

## Generating the records

As you saw in the `dig` query above, the subdomain is `seq_49680`. Obviously, storing 49680 sequences is impractical and would consume a shit ton of space on each resolver. 

This is why there is a special subdomain called `sequence` that will respond with a single TXT string that holds all the available sequence numbers separated by a comma.

However, due to the max length of 255 imposed by TXT strings, the string is compressed with zlib and then base91 encoded. 

The issue is that even with this protection, there is a possibility that if the server is left running for long enought, the sequence number would grow so high that it will still overflow and take too much space. This will cause the server to crash 😕.

As the sequence numbers are linear on the server side, this could be improved by sending the first sequence number available and number of available records.

## TTL

TTL is a big issue, especially if the server is behind resolvers which might not respect low TTLs 🕖.

The TTL of the `sequence` record is fixed to 10 seconds. This is done to ensure that it will be somewhat up-to-date before the client will ever run out of sequences. While I have not tested this extensively, 10sec should be high enought to work somewhat decently on the public internet 😅.

On the other hand, the TTL of sequence subdomains is dynamically calculated to be around 80% of the total length of audio data stored in all the records. The formula looks like this: 

```python
seq_duration = (codec_frame_size * frame_count) / (sample_rate * channels * 2)
ttl = int(seq_duration * sequencer.max_concurrent_numbers * 0.8)
```

Which at 16kHz, 1 channel and a queue of 75 sequence domains in the generator gives a TTL of around 23sec.

## Demo

Here is a demo of AoDNS running a 16kHz 1 channel:

{{< og "https://www.youtube.com/watch?v=OxLp7QJcwbs" >}} 

## Conclusion

While this project was done purely as a tinkering experiment to test the feasibility of using DNS as a non-standard mechanism to move data around, I think it turned out pretty well 😃.

One thing that I didn't discus yet and what a friend mentioned to me, is the potential for free speech and public communication 👨‍👩‍👧‍👦. If the server chain is properly implemented and extended with encryption & DNSSEC & DoTLS or DoHTTPS, I think it would be pretty difficult to actually censor / modify the audio feed.  If the validity of the responses is checked correctly, the worst possible outcome would be a DoS 🔇. 

I think that it would be easier to find a DNS server that resolves to the full internet (which could be forwarded to AoDNS the server)  rather than trying to establish TCP sessions on filtered networks 🌐. Especially since the traffic will look like normal DNS queries.

Since setting up DNS resolvers is mostly effortless, you could even set up many to act as load balancers / region separator.

This is of course pretty far-fetch and far from reality. But, overall pretty happy with this project :smile:.

Note that when I finished the code I was less than 12h from my flight and still didn't have a solution 😅. (Ended up flashing the latest lineage on my old phone and installed Spotify 🤷‍♂️)

{{< og "https://github.com/TheStaticTurtle/AoDNS" >}} 
