---
title: "TI-NSpire SMS Shield"
date: 2018-01-25T20:11:00Z
draft: false
featured: false
image: "images/cover.jpg"
tags: 
    - DIY
    - Electronics
    - IOT
authors:
    - samuel
---
Connecting my Ti-Nspire to the world of sms

<!--more-->

## Why and how

It all started in a German class I had. I was talking to a friend, and we said that it could be awesome to send sms with our TI. After one-two months, I started to do some digging and found out about some "shield" that could be snapped into the bottom connector of the nSpire. After googling a bit I found out that a few people actually did research on this, so this is what I did and here are the 4 pins that I'm interested in:

![](images/dl_ob_299a6c_dockconnectorw.jpg)

After quickly soldering some wires to it and connecting a FTDI breakout board to it, I reset the calculator, and it started dumping out the boot log, so that told me that this could actually work. Now I need a way to access it in software. I searched a bit and found ndless. It's mainly used to play games, but a full SDK to cross compile c for the nSpire. Next I found the nspire-io lib after testing I found that sending was ok the receiving was a pain due to some compatibility issue with different models of TI. After speaking to the author and some nice peoples on the codewalr forum, I modified the source code and it worked. After re-creating a function, it allowed me to receive data until a newline (\n)

```c
char* uart_getsn(char* str, int num) {
        int i = 0;
        int max = num-1;
        while(1 && releasefunc()) {
                while(uart_ready() && isKeyPressed(KEY_NSPIRE_ESC)) {
                        if(i == max) {
                                str[i] = 0;
                                return str;
                        }
                        char c = uart_getchar();
                        str[i] = c;
                        if(c == '\b'){  i -= 2; }
                        else if(c == '\r')      { str[i] =0; return str; }
                        i++;
                }
        }
}
```

After doing some CAD I had it all working and well. Here are source ode link and cad files: [GITHUB](https://github.com/TheStaticTurtle/nspire-communication)

## Photos

{{< gallery >}}
images/IMG_20180422_230404.jpg
images/IMG_20180422_230429.jpg
{{< /gallery >}}