指定できるポケモンは以下の通り。()内は、指定するときの個体名です。
フシギダネ
リザードン
ゼニガメ
コイキング
ピカチュウ
ニャース
トランセル
トレーナー

Poke Sound
====

## Overview

This program is designed to send low-dimensional images from a device(which have microphone and speaker) to another with sound alone.

## Description

### What is done?
- poke.py - This is to transrate images to sounds, mainly using OpenCV. The resolution of images is limited in 60x60.  
- analysis.py - This is to record sounds for certain seconds, analyse them and back-transrate sounds into images.

## Requirement

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

### Receive

1. Run the code.  
`$ python analysis.py`


## Author

[Sorachi Kato](https://github.com/dev-sora)