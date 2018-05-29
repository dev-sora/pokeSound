Poke Sound
====

## Overview

This program is designed to send low-dimensional images from a device(which have microphone and speaker) to another with sound alone.

## Description

### What is done?
- `poke.py` - This program transrates images to sounds, mainly using OpenCV. The resolution of input images is limited in 60x60.
- `analysis.py` - This program records input sounds for certain seconds, analyses them and back-transrates sounds into images.

## Requirement

### Hardware
Two devices(any kind will be fine) are needed.  One is for sending, the other is for receiving.

### Software
The following modules are required.

- OpenCV
- Numpy
- Scipy
- Pygame

To install these modules, check documents of each modules.

## Usage

### Send

1. Run `analysis.py` first.
2. The receiving device entering stand-by state, run with your own choice.  
`$ python poke.py <pokémonName>`

#### Available Pokémon
The following arguments can be used as Pokémon name.

- hushigidane
- lizardon
- zenigame
- koiking
- pikachu
- nyasu
- toranseru
- trainer

### Receive

1. Run the code.  
`$ python analysis.py`


## Author

[Sorachi Kato](https://github.com/dev-sora)