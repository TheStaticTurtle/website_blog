---
layout: portfolio
language: en
translationKey: "portfolio-technologies"
---

## Technologies

This page is about the various technologies & hardware I used at some point.

**The main thing you NEED to remember about this list is that it is not exhaustive. It's there as an indication of what tools and solutions I worked with in my personal, professional or associative projects and activities.**

That being said, if you need clarification or the context in which I used a specific software/hardware, shoot me an email at samuel@tugler.fr I'll make sure to respond and update the page.

### Software development
#### {{< mdi "mdi-database" >}}  Technologies
 - Languages:
   - Preferred: ``Python``, or ``C`` / ``C++``
   - Worked with: ``C#`` / ``PHP`` / ``Javascript`` / ``Java`` / [``E-Basic``](https://support.pstnet.com/hc/en-us/articles/115012937148-SCRIPTING-Introducing-E-Basic-22871-)
   - Scripted with: ``Bash`` / ``Batch`` / ``Powershell``
 - Frameworks / Libraries
   - Web frontend: [``VueJS``](https://vuejs.org/) (with [``Vuetify``](https://vuetifyjs.com/en/)) / [``DTL`` <small>(Django)</small>](https://docs.djangoproject.com/en/4.2/ref/templates/language/) / [``Jinja2`` <small>(Flask)</small>](https://jinja.palletsprojects.com/en/3.1.x/) / [``Twig`` <small>(Symfony)</small>](https://twig.symfony.com/)
   - Web backend: [``Django``](https://www.djangoproject.com/) / [``Flask``](https://flask.palletsprojects.com/en/2.3.x/) / [``FastAPI``](https://fastapi.tiangolo.com/) / [``Express``](https://expressjs.com/) / [``Symfony``](https://symfony.com/)
   - UI: [``PyQT5``](https://pypi.org/project/PyQt5/) / [``PySide5``](https://pypi.org/project/PySide5/) / [``SDL``](https://www.libsdl.org/)
 - Databases / Caches: 
   - SQL: [``SQLite3``](https://www.sqlite.org/index.html) / [``MariaDB``](https://mariadb.org/) / [``Postgresql``](https://www.postgresql.org/)
   - NoSQL: [``MongoDB``](https://www.mongodb.com/)
   - Cache: [``Redis``](https://redis.com/)
 - Messengers:
   - Pub Sub: [``MQTT``](https://mqtt.org/) (traditional and with Websockets) / [``ZMQ``](https://zeromq.org/)
 - Windows fuckury:
   - Custom [SNMP agent extension](https://learn.microsoft.com/en-us/windows/win32/snmp/snmp-functions) to add monitoring to a software
   - Per user local policy based on registry configuration applied at logon


#### {{< mdi "mdi-code-braces" >}}  Software
 - IDEs / Editors:
   - Preferred: [``Jetbrains IDEs``](https://www.jetbrains.com/) / [``VSCode``](https://code.visualstudio.com/)
   - Worked with: [``Visual Studio 2019 (and up)``](https://visualstudio.microsoft.com/) / [``Sublime Text``](https://www.sublimetext.com/) / [``NP++``](https://notepad-plus-plus.org/) / [``Thony``](https://thonny.org/) / [``E-Prime``](https://pstnet.com/products/e-prime/)
 - Source control: [``Git``](https://git-scm.com/)

### Hardware / 3D
#### {{< mdi "mdi-cpu-64-bit" >}}  Chips
 - SBC:
   - Raspberry Pi: ``Raspberry pi 0,1,2,3,4`` / ``Compute module 4``
   - Orange pi: [``Orange Pi Zero LTS``](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/details/Orange-Pi-Zero-LTS.html)
 - SOM:
   - Onion: [``Omega2``](https://onion.io/omega2/)
 - MCU:
   - Atmel: [``Atmega328``](https://www.microchip.com/en-us/product/atmega328)
   - STMicro: [``STM32F103``](https://www.st.com/en/microcontrollers-microprocessors/stm32f103.html#:~:text=STM32F103%20microcontrollers%20use%20the%20Cortex,full%2Dspeed%20interface%20and%20CAN.)
   - Raspberry Pi: [``RP2040``](https://www.raspberrypi.com/documentation/microcontrollers/rp2040.html)
   - Espressif: [``ESP32``](https://www.espressif.com/en/products/socs/ESP32) / [``ESP8266``](https://www.espressif.com/en/products/socs/esp8266) / [``ESP8285``](https://www.espressif.com/sites/default/files/documentation/0a-esp8285_datasheet_en.pdf)
 - IC:
   - Audio: [``CC85XX``](https://www.ti.com/product/CC8520) / [``RDA1846s``](https://datasheetspdf.com/pdf/1473066/RDA/RDA1846/1)
   - Ethernet:  [``W5500``](https://www.wiznet.io/product-item/w5500/) / [``LAN8720a``](https://www.microchip.com/en-us/product/LAN8720A)
   - Wireless: ``NRF24L01`` / [``CC1101``](https://www.ti.com/product/CC1101) / [``NEO-M8N``](https://www.u-blox.com/en/product/neo-m8-series)
   - Lighting: ``WS2811`` / ``WS2812``
   - Other: Signal converters (i.e., ``MAX485``), Interfaces (i.e., ``FT232``), etc.

#### {{< mdi "mdi-desktop-classic" >}}  Software
 - IDEs / Editors:
   - Preferred: ``VSCode`` (with the appropriate module: [``ESP-IDF``](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/)/[``Pico-SDK``](https://github.com/raspberrypi/pico-sdk)/[``PlatformIO``](https://platformio.org/))
   - Worked with: [``Stm32CubeIDE``](https://www.st.com/en/development-tools/stm32cubeide.html) / [``Arduino IDE``](https://www.arduino.cc/en/software/)
 - Languages:
   - ``C`` / ``C++``
   - [``Micropython``](https://micropython.org/) / [``Circuitpython``](https://circuitpython.org/)

#### {{< mdi "mdi-printer-3d" >}}  3D
 - CAD:
   - [``SolidWorks``](https://www.solidworks.com/)
   - Basic [``OpenSCAD``](https://openscad.org/)
 - Slicing: [``Cura``](https://ultimaker.com/software/ultimaker-cura/)

### Audio visual
#### {{< mdi "mdi-light-flood-down" >}} Lighting
 - Traditional [DMX](https://en.wikipedia.org/wiki/DMX512) network (desing and deployment)
 - [``Sunlite suite 2``](https://www.sunlitepro.com/en/sunlite.htm)
 - [``Freestyler``](https://www.freestylerdmx.be/)
  
#### {{< mdi "mdi-audio-input-rca" >}} Audio
 - Traditional analog consoles
 - [``Midas M32``](https://www.midasconsoles.com/product.html?modelCode=P0C7R)
   - Mixing
   - Configuration / Interfacing ([Midas OSC protocol](https://wiki.munichmakerlab.de/images/1/17/UNOFFICIAL_X32_OSC_REMOTE_PROTOCOL_%281%29.pdf) / Midi)
 - Multi-track recording with [Reaper](https://www.reaper.fm/)
 - Audio over [``AES50``](https://en.wikipedia.org/wiki/AES50) / [``VBAN``](https://vb-audio.com/Voicemeeter/vban.htm)
  
#### {{< mdi "mdi-video" >}} Video
 - Live video production with [``vMix``](https://www.vmix.com/)
   - Quintuple multicam setup used in both live and recording simultaneously
   - [IMAG](https://en.wikipedia.org/wiki/IMAG)
   - Synchronization: [``LTC``](https://en.wikipedia.org/wiki/Linear_timecode) 
   - Transports: [``SDI``](https://fr.wikipedia.org/wiki/SDI) / [``NDI``](https://ndi.video/) / [``SRT``](https://www.haivision.com/products/srt-solutions/) / [``MPEG-TS``](https://en.wikipedia.org/wiki/MPEG_transport_stream) 
 - Easy to use multicam conference setup:
   - Blackmagic [Atem Mini Pro](https://www.blackmagicdesign.com/products/atemmini) mixer
   - [AIDA Imaging](https://aidaimaging.com/) camera
   - [RGBLink TAO 1 Tiny](https://www.rgblink.com/productsinfo.aspx?id=227) UVC → HDMI Converter
 - [``OBS``](https://obsproject.com/)
 - [``FFMpeg``](https://ffmpeg.org/)
 - Editing:
   - [``Adobe Premiere Pro``](https://www.adobe.com/fr/products/premiere.html) (basics)
   - [``Davinici resolve``](https://www.blackmagicdesign.com/products/davinciresolve) (basics)
   - [``Kdenlive``](https://kdenlive.org/en/) (basics)

#### {{< mdi "mdi-tune" >}} Control surfaces
  - OSC: [``TouchOSC``](https://hexler.net/touchosc)
  - Midi: [``BCF2000``](https://www.behringer.com/product.html?modelCode=P0246)

### System administration

#### {{< mdi "mdi-desktop-tower-monitor" >}} Infrastructure
 - Clustered PVE
 - 1G/10G Networking
 - Fiber networking
 - Automated deployments:
   - [``Ansible``](https://www.ansible.com/) / [``Chef``](https://www.chef.io/)
   - [``Github Actions``](https://github.com/features/actions)

#### {{< mdi "mdi-server" >}} Virtualization
 - Proxmox:
   - [``Proxmox VE``](https://www.proxmox.com/en/proxmox-ve) (VM + LXC)
   - [``Proxmox BS``](https://www.proxmox.com/en/proxmox-backup-server)
 - VMWare  (basics):
   - [``vCenter``](https://www.vmware.com/products/vcenter.html)
   - [``vMotion``](https://www.vmware.com/products/vsphere/vmotion.html)
 - Microsoft  (basics):
   - [``HyperV``](https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/about/)

#### {{< mdi "mdi-network" >}} Networking
 - Hardware:
   - [``Mikrotik routers & switches``](https://mikrotik.com/)
   - ``Cisco switches``
   - ``SonicWall (TZ300)``
 - VPNs:
   - [``Wireguard``](https://www.wireguard.com/)
   - SSL-VPN based solutions:
     - [``OpenVPN``](https://openvpn.net/)
       - Manual install
       - [``Pritunl``](https://pritunl.com/)
     - [``SonicWall Net-Extender``](https://www.sonicwall.com/products/remote-access/vpn-clients/)
   - L2TP/IPsec with IKEv2

#### {{< mdi "mdi-harddisk" >}} Storage
- Platforms:
  - [``Synology``](https://www.synology.com/en-global)
  - ``Truenas`` ([``Core``](https://www.truenas.com/truenas-core/) + [``Scale``](https://www.truenas.com/truenas-scale/))
- Technologies:
  - [``ZFS``](https://en.wikipedia.org/wiki/ZFS)
  - [``Ceph``](https://docs.ceph.com/en/quincy/) (basics)
- Sharing protocols: [``iSCSI``](https://fr.wikipedia.org/wiki/ISCSI) / [``NFS``](https://en.wikipedia.org/wiki/Network_File_System) / [``SMB``](https://fr.wikipedia.org/wiki/Server_Message_Block) / [``S3``](https://aws.amazon.com/s3/) (and compatibles like [minio](https://min.io/))

#### {{< mdi "mdi-apps" >}} Software solutions
 - Time sync: [``ntpd``](https://linux.die.net/man/8/ntpd) / [``chrony``](https://en.wikipedia.org/wiki/Chrony)
 - DNS: [``bind 9``](https://www.isc.org/bind/) / [``pihole``](https://pi-hole.net/) (HA with [``gravity-sync``](https://github.com/vmstan/gravity-sync))
 - Mail:
   - MTA: [``postfix``](https://www.postfix.org/) (including LDAP auth, spam rejection, relays, DKIM, …)
   - IMAP: [``dovecot``](https://www.dovecot.org/) (including LDAP auth)
   - Clients: [``roundcube``](https://roundcube.net/)
 - Security:
   - Authentication:
     - SSO: [``Keycloak``](https://www.keycloak.org/) / [``Authelia``](https://www.authelia.com/)
     - Domain: [``Active directory Domain Services``](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/active-directory-domain-services-overview)
   - Local certification authority with the [``step-ca``](https://smallstep.com/docs/step-ca/) acme server
   - Remote access: [``Guacamole``](https://guacamole.apache.org/)
 - Web servers: [``Caddy``](https://caddyserver.com/) / [``Apache``](https://httpd.apache.org/) / [``NGINX``](https://www.nginx.com/)
 - Monitoring: [``Observium``](https://www.observium.org/) / [``SNMP``](https://en.wikipedia.org/wiki/Simple_Network_Management_Protocol) / [``inetd``](https://en.wikipedia.org/wiki/Inetd) / [``CheckMK``](https://checkmk.com/) / [``Zabbix`` ](https://www.zabbix.com/)
 - Code management: [``Gitlab``](https://about.gitlab.com/) / [``Gitea``](https://about.gitea.com/)
 - Voice:
   - [``FreePBX``](https://www.freepbx.org/) (With a SPA3102 and soft phones)
 - Document handling & Documentation:
   - [``Paperless-NGX``](https://github.com/paperless-ngx/paperless-ngx)
   - [``Kiwix``](https://www.kiwix.org/)
   - [``Docuwiki``](https://www.dokuwiki.org/dokuwiki) (including theme development)

### Radio & Space 
#### {{< mdi "mdi-radio-tower" >}} Radio
 - Basic knowledge of radio communications
 - [``AX.25``](https://en.wikipedia.org/wiki/AX.25) data links
 - [``SLIP``](https://fr.wikipedia.org/wiki/Serial_Line_Internet_Protocol) / [``PPP``](https://en.wikipedia.org/wiki/Point-to-Point_Protocol) networks over lora
  
#### {{< mdi "mdi-space-station" >}} Satellites
 - Meteorology:
   - [``NOAA``](https://www.noaa.gov/satellites) Series (Analog [``APT``](https://www.sigidwiki.com/wiki/Automatic_Picture_Transmission_(APT)) reception)
   - [``Meteor-M``](https://en.wikipedia.org/wiki/Meteor_(satellite)#Meteor-M) Series ([``LRPT``](https://en.wikipedia.org/wiki/Low-rate_picture_transmission) reception)
 - Ham radio
   - [``QO-100``](https://amsat-uk.org/satellites/geo/eshail-2/)

#### {{< mdi "mdi-star-shooting" >}} Space & Astrophotography
 - Basic photography & stacking