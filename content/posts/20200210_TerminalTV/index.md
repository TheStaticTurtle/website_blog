---
title: "Terminal TV - Watching videos on the terminal"
date: 2020-02-10T20:11:00Z
draft: false
featured: false
image: "images/cover.png"
tags: []
authors:
    - samuel
---
Playing video in the terminal using ANSI codes

<!--more-->

## Intro

I'm currently in college, and we all are using Linux computers with ssh enabled. There is a miss configuration issue that allows me to write into the terminal of other peoples (Not reading it interestingly). We also have crappy system course that no one perticularly likes. And you probably see where I'm going with this.

## How

I first started by making a python prototype of the things but it was terribly slow a 1080p video ran at around 5fps with a terminal size of around 49x189. So I decided time to make a "useful" c++ program.

I choose to use OpenCV for the vast amount of input sources that I take with still having a lot of image processing already in place.

IoCtl is used to get the terminal size, then I use opencv to resize it to the terminal size, then I get the individual rgb colors. Then I use ansi escape code to set the background color of a space.

```cpp
void draw_frame(Mat frame,int termWitdh,int termHeight) {
	int channels = frame.channels();
	uint8_t* pixelPtr = (uint8_t*)frame.data;

	for (int y = 0; y < termHeight-2; y++) {
		for (int x = 0; x < termWitdh; x++) {
			int b = pixelPtr[x*frame.cols*channels + y*channels + 0]; // B
			int g = pixelPtr[x*frame.cols*channels + y*channels + 1]; // G
			int r = pixelPtr[x*frame.cols*channels + y*channels + 2]; // R
			printf("\033[48;2;%d;%d;%dm ",r,g,b);
		}
		if(y != termHeight-2) {cout << "\n";}
	}
	printf("\033[0;0;H");
	printf("\033[48;2;0;0;0m");
	printf("\033[38;2;0;0;0m");
}
```

I messed a bit with unicode characters to try do double the resolution but it isn't working really well

![](images/dl_68747470733a2f2f692e696d6775722e636f6d2f66696551615a492e706e67.png)

{{<og "https://github.com/TheStaticTurtle/terminal_tv">}}

{{<og "https://youtu.be/YMIr55X8WbQ">}}