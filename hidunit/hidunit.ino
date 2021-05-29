#include <Wire.h>
#include <stdio.h>
#include <Adafruit_MCP23017.h>
#include <Servo.h>
#define MCP3425_address 0x68
#define configRegister 0b10011000 //16bit 15sps PGA x1

char serial_text[20];
int last_pressure_angle = 0;
Adafruit_MCP23017 expander;
int ats_status = 0;
Servo bc_servo;
Servo bp_servo;

// 最後に指令を受け取ったミリ秒
unsigned long last_received_time = millis();

void setup() {
  Wire.begin();
  Serial.begin(19200);
  Serial.setTimeout(50);
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
  expander.pinMode(0, OUTPUT);
  expander.pinMode(1, OUTPUT);
  expander.pinMode(2, OUTPUT);
  expander.pinMode(3, OUTPUT);

  for (int i = 4; i < 13; i++) {
    expander.pinMode(i, INPUT);
    expander.pullUp(i, HIGH);
  }

  // サーボ無効
  digitalWrite(14, LOW);
  
  bc_servo.attach(12);
  bp_servo.attach(11);
}

void loop() {
  if (abs(millis() - last_received_time) > 1000) {
    // サーボ無効
    digitalWrite(14, LOW);
  }
  
  int brake_value = 0;
  String input;

  expander.digitalWrite(0, ats_status & 0b1);
  expander.digitalWrite(1, ats_status & 0b10);
  expander.digitalWrite(2, ats_status & 0b100);
  expander.digitalWrite(3, ats_status & 0x1000);
  
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
    last_received_time = millis();
  } else {
    return;
  }

  String input_value_str = input.substring(1);
  int input_value = input_value_str.toInt();

  // ATS表示器に出力する
  if (input.charAt(0) == 'a') {
    ats_status = input_value & 0b1111;
  }
  if (input.charAt(0)== 'b') {
    // サーボ有効
    digitalWrite(14, HIGH);
    bc_servo.writeMicroseconds(input_value);
  }
  if (input.charAt(0) == 'p') {
    // サーボ有効
    digitalWrite(14, HIGH);
    bp_servo.writeMicroseconds(input_value);
  }
}

int readADC() {
  Wire.requestFrom(MCP3425_address, 2);
  return ( (Wire.read() << 8 ) + Wire.read() );
}
