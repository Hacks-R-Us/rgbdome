#include <EtherCard_STM.h>
#include <IPAddress.h>
#include <WS2812B.h>
#include <EEPROM.h>

#define LEDS 484
// UDP port for control commands
#define port_c 1338
// UDP port for LED data
#define port_d 10460

// EEPROM order - mac[6], ip[4], sn[4], gw[4], host[40]
#define hostlen 40
#define start_addr 0

char hostname[hostlen];

// LED Strip
WS2812B strip = WS2812B(LEDS);

// Buffer for UDP data
byte Ethernet::buffer[(LEDS * 3) + 43];

void udpData(uint16_t dest_port, uint8_t src_ip[4], uint16_t src_port, const char *data, uint16_t len){
  for(uint16_t i=0; i<LEDS; i++){
    uint16_t j = i * 3;
    uint8_t r = data[j];
    uint8_t g = data[j+1];
    uint8_t b = data[j+2];
    strip.setPixelColor(i, r, g, b);
  }
  strip.show();
}

void control(uint16_t dest_port, uint8_t src_ip[4], uint16_t src_port, const char *data, uint16_t len) {
  if (data[0] == 0x01) {
    // Reset
    nvic_sys_reset();
  } else if (data[0] == 0x02) {
    // Change IP
    byte buf[4] = {data[1], data[2], data[3], data[4]};
    int address = start_addr + 6;

    eeprom_write(buf, address, 4);
    nvic_sys_reset();
  } else if (data[0] == 0x11){
    // Flash all LEDs 10 times
    for(int t=0; t<10; t++){
      for(uint16_t i=0; i<LEDS; i++){
        uint16_t j = i * 3;
        strip.setPixelColor(i, 0xff, 0xff, 0xff);
      }
      strip.show();
      delay(1000);
      for(uint16_t i=0; i<LEDS; i++){
        uint16_t j = i * 3;
        strip.setPixelColor(i, 0, 0, 0);
      }
      strip.show();
      delay(1000);
    }
  } else if (data[0] == 0x12){
    // Chase along strip 3 times
    for(int t=0; t<3; t++){
      for(uint16_t i=0; i<LEDS; i++){
        uint16_t j = i * 3;
        strip.setPixelColor(i, 0xff, 0xff, 0xff);
        strip.show();
        delay(10);
      }
      strip.show();
      delay(1000);
      for(uint16_t i=0; i<LEDS; i++){
        uint16_t j = i * 3;
        strip.setPixelColor(i, 0, 0, 0);
      }
      strip.show();
      delay(1000);
    }
  }
}

void eeprom_read(byte* ret_array, int &address, int len) {
  // Read from address, for len bytes, modifying buffer array
  for (int i = 0; i < len; i++) {
    ret_array[i] = EEPROM.read(address);
    ++address;
  }
}

void eeprom_write(byte* ret_array, int &address, int len) {
  for (int i = 0; i < len; i++) {
    EEPROM.write(address, ret_array[i]);
    ++address;
  }
}

void setup(){
  int address = start_addr;
  byte mac[6] = {0, };
  eeprom_read(mac, address, sizeof(mac));

  byte buf[4] = {0, };
  eeprom_read(buf, address, sizeof(buf));
  byte loc_ip[] = {buf[0], buf[1], buf[2], buf[3]};

  eeprom_read(buf, address, sizeof(buf));
  byte sn[] = {buf[0], buf[1], buf[2], buf[3]};

  eeprom_read(buf, address, sizeof(buf));
  byte gw[] = {buf[0], buf[1], buf[2], buf[3]};

  for (int i = 0; i < hostlen; i++) {
    byte c = EEPROM.read(address);
    ++address;
    hostname[i] = c;
    if (c == 0) {
      break;
    }
  }
  
  // Start strip
  strip.begin();
  strip.setBrightness(255);

  if (ether.begin(sizeof Ethernet::buffer, mac) == 0){}
  else{}
  ether.staticSetup(loc_ip, gw);
  ether.udpServerListenOnPort(&udpData, port_d);
  ether.udpServerListenOnPort(&control, port_c);
}

void loop(){
  ether.packetLoop(ether.packetReceive());
}
