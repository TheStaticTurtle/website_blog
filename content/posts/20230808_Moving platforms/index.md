---
slug: changing-blogging-platforms
title: Changing my blogging platform
draft: false
featured: false
date: 2023-08-08T10:00:00.000Z
image: "images/cover.png"
tags:
  - web
authors:
  - samuel
---

For a while now, I used ghost for my blog platform. A while ago, I decided that enought was enought I was going to migrate to another platform.
Hugo was selected and lots of development occured.

<!--more-->

For a while now, I used ghost for my blog platform. And, honestly, ghost is a remarkable piece of software, by far the best one I was able to find when I originally set up my blog.

It has some issues though, the biggest one for me is that while it does not natively support markdown and instead uses a custom JSON format.

This is an issue as I write **all** my posts in markdown. I find it way more convenient and easy to use for the kind of blogging I do than using ghost text editor. It does somewhat convert when copying and pasting, but not everything gets translated (especially code blocks).

This is when I decided to migrate to another platform.

At first, as a stupid software engineer, I tried to build my own blog platform with Django. You can probably guess that it never saw the light of day. It's still sitting in my internal git server, half working.

A good while ago, I decided that enought was enought I was going to make this change happen. I laid out a list of requirements for my new website (blog and portfolio).:
  - Static, don't want to deal with a database anymore
  - No JS except for giscus for comments.
  - Gets ALL information from Markdown files.

I tested countless static site generators (even tried to build my own). In the end, I chose Hugo.

## The move

I spent a lot of time writing a Hugo theme for this new website, and to be honest, I still don't understand how certain things work. 

You can find the source code here:
{{<og  "https://github.com/TheStaticTurtle/website_theme"  >}}
{{<og  "https://github.com/TheStaticTurtle/website_blog"  >}}
{{<og  "https://github.com/TheStaticTurtle/website_portfolio"  >}}

Two difficult things to do were image handling (mostly because I wanted to compress remote images as well as store them locally) and diagrams (because HUGO doesn't support on-build diagrams, only with JS).

But by far the most difficult one was to generate embed for links. Normally, it would pretty easy to parse out a web page and extract the opengraph tags. Try doing it in a go template 😭.
Took a while, but with some patience and many regexes I got it to generate nice embeds at build time.

## Conclusion
To conclude this tiny post, I'm pleased with this new solution and thanks to github actions it makes it even easier to write the blog posts easily.

The most important thing is that you'll probably never see any further adjustments if I migrate again, since I wrote the whole theme myself, and I'm pleased with it. It's mostly SCSS files and a few templates, so fairly easy to migrate to somewhere else.