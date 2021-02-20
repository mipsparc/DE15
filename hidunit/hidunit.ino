#include <Servo.h>
#include <Wire.h>
#include <stdio.h>
#include <Adafruit_MCP23017.h>

#define MCP3425_address 0x68
#define configRegister 0b10011000 //16bit 15sps PGA x1
#define speedOutPin 10 // D10ポート

Servo myServo;
char serial_text[20];
int last_pressure_angle = 0;
Adafruit_MCP23017 mcp;

void setup() {
  Wire.begin();
  Serial.begin(9600);
  Wire.beginTransmission(MCP3425_address);
  Wire.write(configRegister);
  Wire.endTransmission();
  pinMode(2, INPUT);
  pinMode(3, INPUT);
  pinMode(4, INPUT);
  pinMode(5, INPUT);
  pinMode(6, INPUT);
  pinMode(7, INPUT);
  myServo.attach(A0);

  mcp.begin((uint8_t)0x0);
  for (int i = 0; i < 13; i++) {
    mcp.pullUp(i, HIGH);
  }
  for (int i = 13; i < 16; i++) {
    mcp.pinMode(i, OUTPUT);
    mcp.digitalWrite(i, HIGH);
  }
}

void loop() {
  // speed:123\n の形式で送受信する
  /** 送信段 **/
  int brake_value = readADC();
  snprintf(serial_text, 20, "brake:%d", brake_value);
  Serial.println(serial_text);
  snprintf(serial_text, 20, "mascon:%d%d%d%d%d%d%d%d", digitalRead(2), digitalRead(3), digitalRead(4), digitalRead(5), digitalRead(6), digitalRead(7), digitalRead(8), digitalRead(9));
  Serial.println(serial_text);

  snprintf(serial_text, 20, "gpio:%u", mcp.readGPIOAB());
  Serial.println(serial_text);

  /** 受信段 **/
  String input = Serial.readStringUntil('\n');
  int pos = input.indexOf(":");
  if (pos < 0) {
    return;
  }

  String input_type = input.substring(0, pos);
  String input_value_str = input.substring(pos + 1);
  int input_value = input_value_str.toInt();

  // 速度計にアナログ出力する
  if (input_type == "speed") {
    analogWrite(speedOutPin, input_value);
  }
  // 圧力計サーボに指令する
  if (input_type == "pressure") {
    int pressure_angle = input_value;
    if (last_pressure_angle != pressure_angle) {
      myServo.writeMicroseconds(pressure_angle);
      last_pressure_angle = pressure_angle;
    }
  }
}

int readADC() {
  Wire.requestFrom(MCP3425_address, 2);
  return ( (Wire.read() << 8 ) + Wire.read() );
}
