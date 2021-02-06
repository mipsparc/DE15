#include <Servo.h>
#include <Wire.h>
#include <stdio.h>
#define MCP3425_address 0x68
#define configRegister 0b10011000 //16bit 15sps PGA x1
#define speedOutPin 10 // D10ポート

Servo myServo;
int last_target_angle = 0;
int target_angle = 0;
int angle = 0;

void setup() {
    Wire.begin();
    Serial.setTimeout(50);
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
}
 
void loop() {
    char brake_text[20];
    char mascon_text[20];
    String input;
    char pos;
    unsigned int mascon_value;
    
    int brake_value = readADC();
    snprintf(brake_text, 20, "brake:%d", brake_value);
    Serial.println(brake_text);
    snprintf(mascon_text, 20, "mascon:%d%d%d%d%d%d%d%d", digitalRead(2), digitalRead(3), digitalRead(4), digitalRead(5), digitalRead(6), digitalRead(7), digitalRead(8), digitalRead(9));
    Serial.println(mascon_text);

    // speed:123 の形式で送る
    input = Serial.readStringUntil('\n');
    pos = input.indexOf(":");
    if (pos == -1) {
      return;
    }
    String input_type = input.substring(0, pos);
    String input_value_str = input.substring(pos+1);
    int input_value = input_value_str.toInt();

    // 速度計にアナログ出力する
    if (input_type == String("speed")) {
      analogWrite(speedOutPin, input_value);
    }
    if (input_type == String("pressure")) {
      target_angle = input_value;
    }

    moveServo();
}
 
int readADC() {
    Wire.requestFrom(MCP3425_address, 2);
    return ( (Wire.read() << 8 ) + Wire.read() );
}

void moveServo() {
      if (target_angle == last_target_angle) {
        return;
      }
      last_target_angle = target_angle;
      if (angle == target_angle) {
        return;
      }

      angle += (target_angle - angle) / 5;

      myServo.writeMicroseconds(angle);
}
