#include <Adafruit_MCP4725.h>
#include <stdio.h>
#include <Servo.h>

#define MCP4725_address 0x60

Adafruit_MCP4725 dac;
int speed_value = 0;
Servo er_servo;

// 最後に指令を受け取ったミリ秒
unsigned long last_received_time = millis();

void setup() {
  Serial.begin(19200);
  dac.begin(MCP4725_address);

  dac.setVoltage(0, false);

  // サーボ無効
  digitalWrite(21, LOW);
  er_servo.attach(16);
}

void loop() {
  if (abs(millis() - last_received_time) > 5000) {
    // サーボ無効
    digitalWrite(21, LOW);
  }
  
  String input;
  String input_value_str;
  int input_value;
  
  /** 受信段 **/
  input = Serial.readStringUntil('\n');
  Serial.println(input);
  if (input.indexOf("EOF")) {
    input.replace("EOF", "");
    last_received_time = millis();
  } else {
    return;
  }
  input_value_str = input.substring(1);
  input_value = input_value_str.toInt();

  // 速度計にアナログ出力する
  if (input.charAt(0) == 's') {
    speed_value = input_value;
  }
  
  // ER圧力計
  if (input.charAt(0) == 'e') {
    // サーボ有効
    digitalWrite(21, HIGH);
    er_servo.writeMicroseconds(input_value);
  }

  dac.setVoltage(speed_value, false);
  
  delay(50);
}
