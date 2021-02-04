#include <VarSpeedServo.h>

VarSpeedServo myServo;  // create a servo object 

int angle = 0;   // variable to hold the angle for the servo motor
int last_angle = 0;

void setup() {
  myServo.attach(9); // attaches the servo on pin 9 to the servo object 
  Serial.begin(9600); // open a serial connection to your computer
  Serial.print("Ready");
}

void loop() {
  if (!Serial.available()) {
    return;
  }
  
  angle = int(Serial.read() - int('!')) * 2;
  
  // only if angle comes twice, it moves
  if (angle != last_angle) {
    last_angle = angle;
    return;
  }
  
  // print out the angle for the servo motor 
  Serial.print(", angle: ");
  Serial.println(angle); 

  // set the servo position  
  myServo.write(angle, 17, true);
}


