---
title: Using docker to contain projects
slug: using-docker-to-contain-projects
date: 2021-04-03T15:44:30.000Z
draft: false
featured: false
image: "images/cover.png"
tags:
    - Web
    - Docker
    - NodeJS
    - Servers
    - Tutorials
authors:
    - samuel
---

How I converted my own NodeJS s3 bucket caching system to a simple docker container for easy deployment of servers / scripts 

<!--more-->

About a year ago I moved all of my image storage to an S3-compatible api provided by OVH. What appealed me the most was the pricing €0.01 / per GB / per month there was however an added cost of €0.01 / per GB download which I didn't like, so I build a little tool that allowed me to cache the images / files stored on the bucket

The tool in question is available on my GitHub:
{{<og "https://github.com/TheStaticTurtle/NodeCached" >}}

The idea is to take the path of the image hash it download the image and rename it to this hash. Next every time we want to access said image the script will serve the cached version. I've also implemented a limit so that it doesn't fill my disk which would defeat the purpose.

The script worked great for a while and then there was the OVH incident where a datacenter caught fire. After the server was restarted I modified the script so that the old cached files could still be used (as the s3 api of my datacenter wasn't restarted yet).

But after 2-3 days I thought that I should have a plan in case something like this ever happened again. I wanted to have the main website (and core component lie the caching system) in one big docker-compose.yml file

So obviously next to come was to build a container of my caching system. The little script is made with NodeJS and first need some remodeling to accept configs in the form of environment variable.

Next I could create a file name Dockerfile at the root of the project with this content:

    FROM node:14
    
    WORKDIR /usr/src/app
    
    COPY package*.json ./
    RUN npm install
    
    COPY . .
    
    EXPOSE 2486
    CMD [ "node", "index.js" ]
    

Every Dockerfile starts with a FROM line stating from which container it should start with in my case since I built the project in NodeJS I choose the container node with the version 14

Next you need to say where your app will be located inside the container in my case I used /user/src/app

The next part is specific to NodeJS, I copied the package.json over in the container and run "npm install" to install my script dependencies (It would be approximately the same with pip and the requirements.txt file for a python project)

After that I copied the whole project in the directory.

I then stated that my app uses the port 2486 and that it should be exposed (to other containers or redirected to the host later)

Next I said that to run the container docker should do "node index.js"

Then in the directory of the Dockerfile I executed

`docker build -t thestaticturtle/nodecached .`

to build the container, you could next use "docker push" to send it to the docker hub

After all of this you can use your freshly build container in a docker-compose file for example:

    version: "3"
    services:
      object_proxy:
        image: thestaticturtle/nodecached:latest
        restart: always
        networks:
          - backend
        volumes:
          - ./data/object-proxy:/usr/src/app/cache/
        ports:
          - 2486:2486
        environment:
          cds__base_url: "url_of_your_s3_server"
    
    networks:
      backend:
        driver: bridge
    

Note that I also specified a volume, that is so that I can access the cached images of my app with going into the container itself

If you want to try it my container is available at: [https://hub.docker.com/r/thestaticturtle/nodecached](https://hub.docker.com/r/thestaticturtle/nodecached)
