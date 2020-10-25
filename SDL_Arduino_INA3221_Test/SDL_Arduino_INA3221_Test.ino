// Dump measurement from INA3221
//
// Send command '1', '2', '3' to start acquisition on channel 1, 2, 3 and send 'S' to stop.
/*
    float bus_v = bus_raw * 0.001;
    float shunt_mv = shunt_raw * 0.005;
    float load_mv = bus_v * 1000 - shunt_mv;
    float current_ma = shunt_mv * 10;  // V/R = V/0.1 = V*10
  */  
// To flash new program: press reset button and run the following command (with the correct .hex file)
// ./avr/bin/avrdude -p m32u4 -P /dev/ttyACM0 -c avr109 -C ./avr/etc/avrdude.conf -U flash:w:/tmp/arduino_build_239786/SDL_Arduino_INA3221_Test.ino.hex
//

// Christophe Augier <christophe@kitae.tech>


#include <Wire.h>
#include "SDL_Arduino_INA3221.h"

SDL_Arduino_INA3221 ina3221;

void setup(void) 
{
    
  Serial.begin(115200);
//  Serial.print("Start measuring current on ID=0x");
  int MID;
  MID = ina3221.getManufID();
//  Serial.println(MID, HEX);
}

static bool started = false;
static int channel = 0;
static int period = 0;

void loop(void) 
{
  static unsigned long last_time = 0;
  static uint8_t counter = 0;

  if (Serial.available() > 0) {
    char cmd = Serial.read();
    switch(cmd) {
      case '1':
        started = true;
        channel = 1;
        period = 10000;  // 10ms
        counter = 0;
        ina3221.begin(1);
        last_time = micros();
        break;
      case '2':
        started = true;
        channel = 2;
        period = 5000;  // 5 ms
        counter = 0;
        ina3221.begin(2);
        last_time = micros();
        break;
      case '3':
        started = true;
        channel = 3;
        period = 5000;  // 5 ms
        counter = 0;
        ina3221.begin(3);
        last_time = micros();
        break;       
      case 'S':
        started = false;
      break;
    }
  }
  if (!started) {
    return;
  }
  

  unsigned long now = micros();
  long delta = now - last_time;
  if (now > last_time) {
    delta = now - last_time;
  } else {
    delta = (0xffffffff - last_time) + now;
  }
  if (delta >= period) {
    int16_t bus_raw = ina3221.getBusVoltage_raw(channel);
    int16_t shunt_raw = ina3221.getShuntVoltage_raw(channel);
    uint8_t buf[6];
    buf[0] = 0xaa; // 0b10101010
    buf[1] = counter;
    buf[2] = bus_raw & 0xff;
    buf[3] = bus_raw >> 8;
    buf[4] = shunt_raw & 0xff;
    buf[5] = shunt_raw >> 8;
    Serial.write(buf, 6);
    last_time = now;
    counter++;
  }
}
