---
title: "Experimenting with the OpenGraph protocol"
date: 2020-05-10T19:58:00.000Z
draft: false
featured: false
image: "images/cover.png"
tags:
    - Research
    - Security
    - Web
authors:
    - samuel
---

Some time ago I remembered about the opengraph protocol

<!--more-->

> The [Open Graph protocol](http://ogp.me/) enables any web page to become a rich object in a social graph. For instance, this is used on Facebook to allow any web page to have the same functionality as any other object on Facebook. While many different technologies and schemas exist and could be combined together, there isn't a single technology which provides enough information to richly represent any web page within the social graph. The Open Graph protocol builds on these existing technologies and gives developers one thing to implement. Developer simplicity is a key goal of the Open Graph protocol which has informed many of [the technical design decisions](http://www.scribd.com/doc/30715288/The-Open-Graph-Protocol-Design-Decisions).

However, this can be easily exploited to create phishing attacks. For instance, imagine that a friend ask you about a wikipedia article and for some reason you want him to go to your website (steal login for example).

I'm going to put screenshots of discord because it react very well with thi attack.

Imagine a simple html page:

    <html>
     <head>
       <title>Title</title>
     </head>
     <body>
       <center><h1>YOLO</h1></center>
     </body>
    </html>
    

Will give you a message like this, not very clickbaity
![](images/dl_xnxKw33.png)
Now lets add the OpenGraph protocol (See [doc](https://ogp.me/#metadata))

    <html prefix="og: http://ogp.me/ns/video#">
        <head>
            <title>LOL</title>
            <meta property="og:site_name" content="Wikipedia">
            <meta property="og:type" content="website" />   
            <meta property="og:title" content="The Flash (2014 TV series)" />  
            <meta property="og:description" content="The Flash is an American superhero television series developed by Greg Berlanti, Andrew Kreisberg, and Geoff Johns, airing on The CW. It is based on the DC Comics character Barry Allen / Flash, a costumed superhero crime-fighter with the power to move at superhuman speeds. It is a spin-off from Arrow, existing in the same fictional universe known as Arrowverse. The series follows Barry Allen, portrayed by Grant Gustin, a crime scene investigator who gains super-human speed, which he uses to fight criminals, including others who have also gained superhuman abilities." />  
            <meta property="og:image" content="------------/-----/writeup/image.jpg" />   
            <meta property="og:url" content="https://en.wikipedia.org/wiki/The_Flash_(2014_TV_series)" />
        </head>
        <body>  
            <center>
                <h1>YOLO</h1>
            </center> 
        </body>
    </html>
    

This very simple code will give you this:
![](images/dl_zLkyXEM.png)
Much better someone will be more likely to click the link however the real article dosen't look like this and maybe your friend is a book head and will spot the difference, the real one looks like this:
![](images/dl_vYMgakC.png)
So how can we solve this? As it turn's out, you can tell opengraph the size of the image:

- `og:image:width` - The number of pixels wide.
- `og:image:height` - The number of pixels high.

so lets try that here's the code so far:

    <html prefix="og: http://ogp.me/ns/video#">
        <head>
            <title>LOL</title>
            <meta property="og:site_name" content="Wikipedia">
            <meta property="og:type" content="website" />
            <meta property="og:title" content="The Flash (2014 TV series)" /> 
            <meta property="og:description" content="The Flash is an American superhero television series developed by Greg Berlanti, Andrew Kreisberg, and Geoff Johns, airing on The CW. It is based on the DC Comics character Barry Allen / Flash, a costumed superhero crime-fighter with the power to move at superhuman speeds. It is a spin-off from Arrow, existing in the same fictional universe known as Arrowverse. The series follows Barry Allen, portrayed by Grant Gustin, a crime scene investigator who gains super-human speed, which he uses to fight criminals, including others who have also gained superhuman abilities." />   
            <meta property="og:image" content="------------/-----/writeup/image.jpg" />  
            <meta content="400" property="og:image:width">  
            <meta content="225" property="og:image:height">  
            <meta property="og:url" content="https://en.wikipedia.org/wiki/The_Flash_(2014_TV_series)" />
        </head> 
        <body>   
            <center>
                <h1>YOLO</h1>
            </center> 
        </body>
    </html>
    

![](images/dl_oIWDHdB.png)
Well that didn't change much. As it turn's out Twitter has it's own version of opengraph called Cards and discord follow both converting to Twitter opengraph is simple just change `og:` to `twitter:`**.** You will also need to say that's it's actually a card with the `card` attribute. So lets test this:

    <html prefix="og: http://ogp.me/ns/video#">
        <head>  
            <title>LOL</title>  
            <meta property="og:site_name" content="Wikipedia">
            <meta property="og:type" content="website" /> 
            <meta content="summary_large_image" name="twitter:card"> 
            <meta property="og:title" content="The Flash (2014 TV series)" />
            <meta name="twitter:title" content="The Flash (2014 TV series)" >  
            <meta property="og:description" content="The Flash is an American superhero television series developed by Greg Berlanti, Andrew Kreisberg, and Geoff Johns, airing on The CW. It is based on the DC Comics character Barry Allen / Flash, a costumed superhero crime-fighter with the power to move at superhuman speeds. It is a spin-off from Arrow, existing in the same fictional universe known as Arrowverse. The series follows Barry Allen, portrayed by Grant Gustin, a crime scene investigator who gains super-human speed, which he uses to fight criminals, including others who have also gained superhuman abilities." />  
            <meta name="twitter:description" content="The Flash is an American superhero television series developed by Greg Berlanti, Andrew Kreisberg, and Geoff Johns, airing on The CW. It is based on the DC Comics character Barry Allen / Flash, a costumed superhero crime-fighter with the power to move at superhuman speeds. It is a spin-off from Arrow, existing in the same fictional universe known as Arrowverse. The series follows Barry Allen, portrayed by Grant Gustin, a crime scene investigator who gains super-human speed, which he uses to fight criminals, including others who have also gained superhuman abilities." >  
            <meta property="og:image" content="------------/-----/writeup/image.jpg" />  
            <meta name="twitter:image" content="------------/-----/writeup/image.jpg" >   
            <meta content="400" property="og:image:width"> <meta content="225" property="og:image:height">  
            <meta property="og:url" content="https://en.wikipedia.org/wiki/The_Flash_(2014_TV_series)" />   
            <meta name="twitter:url" content="https://en.wikipedia.org/wiki/The_Flash_(2014_TV_series)" > 
        </head> 
        <body>  
            <center>
                <h1>YOLO</h1>
            </center> 
        </body>
    </html>
    

![](images/dl_LFU4mr9.png)
**Bingo.**

The message now resemble exactly the original. Now if you don't have a domain like en.wikipedia.org.example.com/wiki/The_Flash_(2014_TV_series) to put your page and sent it to your friend just use a url shorter like bitly and it will work fine:
![](images/dl_1oYzt0O.png)
This should obviously not be used for phishing but makes a very good entry point

Resources:

- [https://ogp.me/](https://ogp.me/)
- [http://developers.facebook.com/tools/debug/](http://developers.facebook.com/tools/debug/)
