#include <Wire.h>
#include <stdio.h>
#include <Adafruit_MCP23017.h>

#define MCP3425_address 0x68
#define configRegister 0b10011000 //16bit 15sps PGA x1

char serial_text[20];
int last_pressure_angle = 0;
Adafruit_MCP23017 expander;

void setup() {
  Wire.begin();
  Serial.begin(19200);
  Serial.setTimeout(100);
  Wire.beginTransmission(MCP3425_address);
  Wire.write(configRegister);
  Wire.endTransmission();
  pinMode(2, INPUT);
  pinMode(3, INPUT);
  pinMode(4, INPUT);
  pinMode(5, INPUT);
  pinMode(6, INPUT);
  pinMode(7, INPUT);

  expander.begin();
  for (int i = 0; i < 13; i++) {
    expander.pinMode(i, INPUT);
    expander.pullUp(i, HIGH);
  }
}

void loop() {
  int brake_value;
  String input;
  
  /** 送信段 **/
  brake_value = readADC();
  snprintf(serial_text, 20, "brake:%d", brake_value);
  Serial.println(serial_text);
  snprintf(serial_text, 20, "mascon:%d%d%d%d%d%d%d%d", digitalRead(2), digitalRead(3), digitalRead(4), digitalRead(5), digitalRead(6), digitalRead(7), digitalRead(8), digitalRead(9));
  Serial.println(serial_text);

  snprintf(serial_text, 20, "gpio:%u", expander.readGPIOAB());
  Serial.println(serial_text);
}

int readADC() {
  Wire.requestFrom(MCP3425_address, 2);
  return ( (Wire.read() << 8 ) + Wire.read() );
}
