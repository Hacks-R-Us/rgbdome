# RGB Dome Arduino code

## nanostrand
Controller for Arduino Nano using enc28j60 ethernet chip

### Requirements
- Ethercard
- Neopixel

### Limits
- ~240 LED's before running out of memory

## stmstrand
Controller for STM32 using enc28j60 ethernet chip and Arduino_STM32

### Requirements
- Arduino_STM32
- Ethercard_STM
- WS2812B, modified to use SPI 2

### Limits
- ~700 LED's before failing to run at all
- 484 LED's per UDP packet

### Connections
PA5 - SCK
PA6 - SO
PA7 - SI
PA8 - CS
PB15 - LEDs

### Notes
The 3v3 reg on "Blue Pill" STM32 boards is somewhat cheap, and some instability has been experienced when using the onboard 3v3 to power the ENC28J60. Using an external 3v3 reg (e.g, LD1117V33) between the onboard 5v and the ENC28J60's 3v3 seems to fix these instabilities.

For futher information, see:
http://wiki.stm32duino.com/index.php?title=Blue_Pill#Known_issues
https://electronics.stackexchange.com/questions/52349/why-is-ethernet-so-power-hungry
