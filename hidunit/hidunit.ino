#include <Servo.h>
#include <Wire.h>
#include <stdio.h>
#include <Adafruit_MCP23017.h>
#include <Adafruit_MCP4725.h>

#define MCP3425_address 0x68
#define configRegister 0b10011000 //16bit 15sps PGA x1
#define MCP4725_address 0x60
#define speedOutPin 10 // D10ポート

Servo myServo;
char serial_text[20];
int last_pressure_angle = 0;
Adafruit_MCP23017 expander;
int input_value;
Adafruit_MCP4725 dac;
int last_speed = 0;
int speed_count = 0;

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
  myServo.attach(A0);

  expander.begin();
  for (int i = 0; i < 13; i++) {
    expander.pinMode(i, INPUT);
    expander.pullUp(i, HIGH);
  }
  
  dac.begin(MCP4725_address);
}

void loop() {
  int brake_value;
  String input;
  int pos;
  String input_type;
  String input_value_str;
  
  /** 送信段 **/
  brake_value = readADC();
  snprintf(serial_text, 20, "brake:%d", brake_value);
  Serial.println(serial_text);
  snprintf(serial_text, 20, "mascon:%d%d%d%d%d%d%d%d", digitalRead(2), digitalRead(3), digitalRead(4), digitalRead(5), digitalRead(6), digitalRead(7), digitalRead(8), digitalRead(9));
  Serial.println(serial_text);

  snprintf(serial_text, 20, "gpio:%u", expander.readGPIOAB());
  Serial.println(serial_text);

  /** 受信段 **/
  input = Serial.readStringUntil('\n');
  if (input.indexOf("EOF")) {
    input.replace("EOF", "");
  } else {
    return;
  }
  input_value_str = input.substring(1);
  input_value = input_value_str.toInt();
  
  // 速度計にアナログ出力する
  if (input.charAt(0) == 's') {
    if (last_speed != input_value) {
      speed_count += 1;
    } else {
      speed_count = 0;
    }

    if (speed_count > 3) {
      speed_count = 0;
      if (last_speed - input_value > 10) {
        input_value = abs(last_speed - 10);
      }
      dac.setVoltage(input_value, false);
      last_speed = input_value;
    }
    
    return;
  }
  
  // 圧力計サーボに指令する
  if (input.charAt(0) == 'p') {
    int pressure_angle = input_value;
    if (last_pressure_angle != pressure_angle) {
      myServo.writeMicroseconds(pressure_angle);
      last_pressure_angle = pressure_angle;
    }

    return;
  }
}

int readADC() {
  Wire.requestFrom(MCP3425_address, 2);
  return ( (Wire.read() << 8 ) + Wire.read() );
}
