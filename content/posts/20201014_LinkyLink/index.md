---
title: "LinkyLink - Connecting myself to the French energy meter"
date: 2020-01-14T20:11:00Z
draft: false
featured: false
image: "images/cover.jpg"
tags: 
    - DIY
    - Electronics
    - IOT
    - Home Automation
authors:
    - samuel
---
Making a custom board to connect an esp8266 to the french energy meter

<!--more-->

## A bit of context

{{< gallery >}}
images/dl_4f7d74837884ae09d9a3a88a609faa01e80c6ea8-compteur-linky-teleinformation.jpeg
images/dl_e774561f541de60f5a360a97c188bf3412fc1ae2-compteurlinky-e15499842838113x.jpeg
{{< /gallery >}}

The Linky energy meter is "connected" energy meter it transmit the energy consumed by their user to the energy company (Enedis).

## The inner workings

The arrow on the second picture above show the user teleinfo port. Here the user is free to plug something like the "Linky ERL" or any device to monitor the meter

![](images/dl_Screenshot_20200121_222732.png)

The linky provides 3 "easy" to use ports I1 I2 and A. The actual data comes from the circuit I1 and I2 and you have an alimentation circuit between I1 and A. For reference P, N, P', N' are the mains connections C1 and C2 connection to a water boiler and T1 / T2 are I think for technicians and are locked.

The actual signal is a unidirectional serial connection with a 50kHz carrier. The documentation (available at the bottom) says that the signal is at 9600bps 7E1 but the signal is actually 1200bps at 7E1. Converting this signal is really simple I used the following circuit:

![](images/dl_Screenshot_20200121_224123.png)

The linky spits out frames composed of these lines (For the one I have):

```
ADCO <censored>
OPTARIF HC..
ISOUSC 30
HCHC 000582078
HCHP 000599002
PTEC HP..
IINST 005
IMAX 090
PAPP 01115
HHPHC A
MOTDETAT 000000
```

Here's a table to see what stands for what:

![](images/dl_Screenshot_20200121_225030-1@2x.png)

## Version 1 - Prototype

The documentation tells us how a frame is transmitted: First you have the char 0x02 there for each line start 0x0A and 0x0D the end of a line the end of a frame is signaled by the char 0x03 and a premature end of data by 0x04

```h
#define LINKY_START_FRAME           0x02
#define LINKY_END_FRAME             0x03
#define LINKY_START_LINE            0x0A
#define LINKY_END_LINE              0x0D
#define LINKY_END_DATA              0x04
```

As I wanted to make my module compatible with 3-phased devices I added all these in the code as well and here's my structure for holding the data:

```cpp
struct LinkyData {
  char   ADCO   [13];      //Adresse du compteur
  char   OPTARIF[ 5];      //Option tarifaire choisie
  int    ISOUSC;           //Intensitée souscrite
  int    BASE;             //Index option Base
  long   HCHC;             //Index option Heures Creuses - Heures Creuses
  long   HCHP;             //Index option Heures Creuses - Heures Pleines
  long   EJPHN;            //Index option EJP - Heures Normales
  long   EJPHPM;           //Index option EJP - Heures de Pointe Mobile
  long   BBRHCJB;          //Index option Tempo - Heures Creuses Jours Bleus
  long   BBRHPJB;          //Index option Tempo - Heures Pleines Jours Bleus
  long   BBRHCJW;          //Index option Tempo - Heures Creuses Jours Blancs
  long   BBRHPJW;          //Index option Tempo - Heures Pleines Jours Blancs
  long   BBRHCJR;          //Index option Tempo - Heures Pleines Jours Rouges
  long   BBRHPJR;          //Index option Tempo - Heures Pleines Jours Rouges
  int    PEJP;             //Préavis Début EJP (30 min)
  char   PTEC   [ 5];      //Période Tarifaire en cours
  char   DEMAIN [ 5];      //Couleur du lendemain
  int    IINST;            //Intensité Instantanée
  int    IINST1;           //Intensité Instantanée Phase né1 (Triphaser seulement)
  int    IINST2;           //Intensité Instantanée Phase né2 (Triphaser seulement)
  int    IINST3;           //Intensité Instantanée Phase né3 (Triphaser seulement)
  int    ADPS;             //Avertissement de DépassementDe Puissance Souscrite
  int    ADIR1;            //Avertissement de DépassementDe Puissance Souscrite Phase né1 (Triphaser seulement)
  int    ADIR2;            //Avertissement de DépassementDe Puissance Souscrite Phase né2 (Triphaser seulement)
  int    ADIR3;            //Avertissement de DépassementDe Puissance Souscrite Phase né3 (Triphaser seulement)
  int    IMAX;             //Intensité maximale appelée
  int    IMAX1;            //Intensité maximale appelée Phase né1 (Triphaser seulement)
  int    IMAX2;            //Intensité maximale appelée Phase né2 (Triphaser seulement)
  int    IMAX3;            //Intensité maximale appelée Phase né3 (Triphaser seulement)
  long   PMAX;             //Puissance maximale triphasée atteinte
  long   PAPP;             //Puissance apparente / Puissance apparente triphasée soutirée
  char   HHPHC;            //Horaire Heures Pleines Heures Creuses
  char   MOTDETAT[ 7];     //Mot d'état du compteur
  char   PPOT    [ 3];     //Présence des potentiels (Triphaser seulement) ("0X", X = coupures de phase phase n => bit n = 1)
}; 
```

Receiving the data is as simple as creating a new software serial with the right pins and the incoming byte by 0x7F to get only the 7 bits since arduino software serial can't strictly do 7E1 communications. Then I created a char array of the size of 100 (It will never be used completely) and incremented a variable at each valid char received to store it.

```cpp
void Linky::processRXChar(char currentChar) {
    if(currentChar == LINKY_START_FRAME) {
        memset(_buffer, 0, LINKY_BUFFER_TELEINFO_SIZE);
        _bufferIterator = 0;

    } else if(currentChar == LINKY_START_LINE) {
        memset(_buffer, 0, LINKY_BUFFER_TELEINFO_SIZE);
        _bufferIterator = 0;

    } else if(currentChar == LINKY_END_FRAME) {
        memset(_buffer, 0, LINKY_BUFFER_TELEINFO_SIZE);
        _bufferIterator = 0;

    } else if(currentChar == LINKY_END_LINE) {
        updateStruct(_bufferIterator);
        memset(_buffer, 0, LINKY_BUFFER_TELEINFO_SIZE);
        _bufferIterator = 0;

    } else if(currentChar == LINKY_END_DATA) {
        memset(_buffer, 0, LINKY_BUFFER_TELEINFO_SIZE);
        _bufferIterator = 0;

    } else {
        _buffer[_bufferIterator] = currentChar;
        _bufferIterator++;

    }
}
void Linky::updateAsync() {
    if(_serport->available()) {
        char currentChar;

        currentChar = _serport->read() & 0x7F;
        processRXChar(currentChar);
    }
}
```

Then I created a couple of function that ease the parsing of the data by a lot (getCommandValue_int / getCommandValue_long / getCommandValue_str) to use these function you have to pass the actual command name like ADCO the length in this case 4 and the expected length of the output in this case 12 plus some other values like the size of received line.

```cpp
bool Linky::isValidNumber(String str){
   for(byte i=0;i<str.length();i++)  {
       if(!isDigit(str.charAt(i))) return false;
   }
   return true;
}

int Linky::getCommandValue_int(String CMD, int CMDlenght, int CMDResultLenght, String line, int lineLenght, int defaultIfError) {
  if(!line.startsWith(CMD)) { return defaultIfError; }
  if(CMDlenght+1+CMDResultLenght > lineLenght) { return defaultIfError; } // Invalid size line length too short

  String raw_value = line.substring(CMDlenght+1, CMDlenght+1+CMDResultLenght);
  if(!isValidNumber(raw_value)) { return defaultIfError; }

  return raw_value.toInt();
}

long Linky::getCommandValue_long(String CMD, int CMDlenght, int CMDResultLenght, String line, int lineLenght, long defaultIfError) {
  if(!line.startsWith(CMD)) { return defaultIfError; }
  if(CMDlenght+1+CMDResultLenght > lineLenght) { return defaultIfError; } // Invalid size line length too short

  String raw_value = line.substring(CMDlenght+1, CMDlenght+1+CMDResultLenght);
  if(!isValidNumber(raw_value)) { return defaultIfError; }

  return (long)raw_value.toInt();
}

bool Linky::getCommandValue_str(String CMD, int CMDlenght, int CMDResultLenght, String line, int lineLenght, char* value) {
  if(!line.startsWith(CMD)) { return false; }
  if(CMDlenght+1+CMDResultLenght > lineLenght) { return false; } // Invalid size line length too short

  line.substring(CMDlenght+1, CMDlenght+1+CMDResultLenght).toCharArray(value,CMDResultLenght+1);
  return true;
} 

void Linky::updateStruct(int len) {
     getCommandValue_str ("ADCO"    , 4,12,_buffer,len+1, _data.ADCO     );
     getCommandValue_str ("OPTARIF" , 7, 4,_buffer,len+1, _data.OPTARIF  );
    _data.ISOUSC    =   getCommandValue_int ("ISOUSC"  , 6, 2,_buffer,len+1, _data.ISOUSC);
    _data.HCHC      =   getCommandValue_long("HCHC"    , 4, 9,_buffer,len+1, _data.HCHC);
    _data.HCHP      =   getCommandValue_long("HCHP"    , 4, 9,_buffer,len+1, _data.HCHP);
    _data.EJPHN     =   getCommandValue_long("EJPHN"   , 5, 9,_buffer,len+1, _data.EJPHN);
    _data.EJPHPM    =   getCommandValue_long("EJPHPM"  , 6, 9,_buffer,len+1, _data.EJPHPM);
    _data.BBRHCJB   =   getCommandValue_long("BBRHCJB" , 7, 9,_buffer,len+1, _data.BBRHCJB);
    _data.BBRHPJB   =   getCommandValue_long("BBRHPJB" , 7, 9,_buffer,len+1, _data.BBRHPJB);
    _data.BBRHCJW   =   getCommandValue_long("BBRHCJW" , 7, 9,_buffer,len+1, _data.BBRHCJW);
    _data.BBRHPJW   =   getCommandValue_long("BBRHPJW" , 7, 9,_buffer,len+1, _data.BBRHPJW);
    _data.BBRHCJR   =   getCommandValue_long("BBRHCJR" , 7, 9,_buffer,len+1, _data.BBRHCJR);
    _data.BBRHPJR   =   getCommandValue_long("BBRHPJR" , 7, 9,_buffer,len+1, _data.BBRHPJR);
    _data.PEJP      =   getCommandValue_int ("PEJP"    , 4, 2,_buffer,len+1, _data.HCHP);
     getCommandValue_str ("PTEC"    , 4, 4,_buffer,len+1, _data.PTEC  );
     getCommandValue_str ("DEMAIN"  , 6, 4,_buffer,len+1, _data.DEMAIN  );
    _data.IINST     =   getCommandValue_int ("IINST"   , 5, 3,_buffer,len+1, _data.IINST); 
    _data.IINST1    =   getCommandValue_int ("IINST1"  , 6, 3,_buffer,len+1, _data.IINST1); 
    _data.IINST2    =   getCommandValue_int ("IINST2"  , 6, 3,_buffer,len+1, _data.IINST2); 
    _data.IINST3    =   getCommandValue_int ("IINST3"  , 6, 3,_buffer,len+1, _data.IINST3); 
    _data.ADPS      =   getCommandValue_int ("ADPS"    , 4, 3,_buffer,len+1, _data.ADPS); 
    _data.ADIR1     =   getCommandValue_int ("ADIR1"   , 5, 3,_buffer,len+1, _data.ADIR1); 
    _data.ADIR2     =   getCommandValue_int ("ADIR2"   , 5, 3,_buffer,len+1, _data.ADIR2); 
    _data.ADIR3     =   getCommandValue_int ("ADIR3"   , 5, 3,_buffer,len+1, _data.ADIR3);
    _data.IMAX      =   getCommandValue_int ("IMAX"    , 4, 3,_buffer,len+1, _data.IMAX); 
    _data.IMAX1     =   getCommandValue_int ("IMAX1"   , 5, 3,_buffer,len+1, _data.IMAX1); 
    _data.IMAX2     =   getCommandValue_int ("IMAX2"   , 5, 3,_buffer,len+1, _data.IMAX2); 
    _data.IMAX3     =   getCommandValue_int ("IMAX3"   , 5, 3,_buffer,len+1, _data.IMAX3); 
    _data.PMAX      =   getCommandValue_long("PMAX"    , 4, 5,_buffer,len+1, _data.PMAX); 
    _data.PAPP      =   getCommandValue_long("PAPP"    , 4, 5,_buffer,len+1, _data.PAPP); 
     getCommandValue_str ("MOTDETAT", 8, 6,_buffer,len+1, _data.MOTDETAT );
     getCommandValue_str ("PPOT"    , 4, 2,_buffer,len+1, _data.PPOT);
}
```

Implementing everything into the ESP8266:

{{<og "https://github.com/TheStaticTurtle/LinkyLink">}}

The code is working on some meters but on some other I cannot get data to be read by the esp8266 it seems to be an optocoupler issue.