#include <Arduino.h>
#include <TimeLib.h>

// Output pins to MOSFETs
int switchPin = 4;

int time_on = 1;
int time_off = 10;
int astrapi_total_time_on = 10;
int running = 0;


void setup() {
  Serial.begin(115200);
  pinMode(switchPin, OUTPUT);
  digitalWrite(switchPin, LOW);
}

void loop() {
  if (Serial.available())  {
    char c = Serial.read();  //gets one byte from serial buffer
    if (c == 's') {
      // start run
      running = 1;
      digitalWrite(switchPin, HIGH);
    }
    else if (c == 'q') {
      // stop run
      running = 0;
      digitalWrite(switchPin, LOW);
    }
    else if (c == 't') {
      // on time
      time_on = Serial.parseInt();
    }
    else if (c == 'o') {
      // off time between runs
      time_off = Serial.parseInt();
    }
    else if (c == 'a') {
      // total on time
      astrapi_total_time_on = Serial.parseInt();
    }
  }

  if (running == 1){
    time_t startTime_total = millis();
    while ((startTime_total+astrapi_total_time_on*1000) > millis()){
      digitalWrite(switchPin, HIGH);
      delay(time_on*1000);
      digitalWrite(switchPin, LOW);
      delay(time_off*1000);
    }
    running = 0;
  }

}