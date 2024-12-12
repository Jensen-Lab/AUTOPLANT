#include <Arduino.h>
#include <TimeLib.h>

// Output pins to switch
int switchPin = 4;

void setup() {
    Serial.begin(115200);
    Serial.println("<Arduino is ready>");
    pinMode(switchPin, OUTPUT);
    digitalWrite(switchPin, LOW);
}

String readString;
long time_on = 30;
long time_off = 10;
long total_time_on = 80;
int running = 0;

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
      total_time_on = Serial.parseInt();
    }
  }


  if (running == 1){
    // time_t startTime_total = minute()*60 + second();
    // while (total_time_on > minute()*60+second()){
    time_t startTime_total = millis();
    // while (astrapi_total_time_on > minute()*60+second()){
    // Serial.println(total_time_on);
    // Serial.println(total_time_on*1000);
    // Serial.println(startTime_total);
    // Serial.println(startTime_total+total_time_on*1000);
    while ((startTime_total+total_time_on*1000) > millis()){  
      digitalWrite(switchPin, HIGH);
      delay(time_on*1000);
      digitalWrite(switchPin, LOW);
      delay(time_off*1000);
    }
    running = 0;
    // }
  }
}
