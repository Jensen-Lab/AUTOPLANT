#include <Arduino.h>
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_I2CDevice.h>
#include <stdio.h>
#include "pico/stdlib.h"
#include "pico/multicore.h"
#include "hardware/irq.h"
#include "hardware/adc.h"
#include "hardware/sync.h"
#include "hardware/irq.h" // Include the header file that defines SIO_IRQ_PROC0_FIFO
#include <TMCStepper.h>
#include <main_TMC2130.h>
#include <AS5048B_TMC_stepper.h>


#define I2C_ADDRESS 0b1000000
TwoWire wire = TwoWire(i2c0, 8, 9);


Adafruit_I2CDevice i2c_dev = Adafruit_I2CDevice(I2C_ADDRESS, &wire);


TMC2130Stepper driver(CS_PIN, SW_MOSI, SW_MISO, SW_SCK);
AS5048B_TMC_stepper motor = AS5048B_TMC_stepper(i2c_dev, driver);


/// multicore
struct SensorData {
    double value;
};

volatile SensorData sensorData;
volatile bool dataReady = false;


int Nsteps = 0;
int dir = 0;
int dir_old = 0;
int microstep = 0;
int rms_current = 0;
int hold = 0;
int stepDelay = 0;
int autoModeFlag = 0;
double target_position = 0;


void setup(){
  //sleep_ms(1000); // Sleep for 1 second
    Serial.begin(115200); // Start the serial communication
    motor.init();
  //sleep_ms(1000);
}

void loop(){
  //sleep_ms(100); // Sleep for 1 second
  // check for serial input from computer
  sleep_ms(1);

  if (autoModeFlag)
  {
      
    motor.moveTowardsTarget();

    if(Serial.available()>0){
      char readVal = Serial.read();
      if (readVal == 'p'){
        Serial.println(motor.GetCurrentPosition());
      }
      if (readVal == 't'){
        motor.setMaxTolorance(Serial.parseInt());
      }
      if (readVal == 'b'){
        target_position = Serial.parseInt();
        motor.setTargetPosition(target_position);
        Serial.println(target_position);
      }
      if (readVal == 'x'){
        target_position = motor.getTargetPosition() + Serial.parseInt();
        motor.setTargetPosition(target_position);
        Serial.println(target_position);
      }
      if (readVal == 'a'){
        autoModeFlag = Serial.parseInt();
        if (autoModeFlag == 0)
        {
          Serial.println("Mode set to manual");
        }
      }
      if (readVal == 's'){
        autoModeFlag = 0;
        Serial.println("Emergency stop");
        Serial.println("Mode set to manual");
      }
    }
  } else {

    if(Serial.available()>0){
      char readVal = Serial.read();
      if (readVal == 'h'){
          //homed = false;
          // home();
      }
      if (readVal == 'x'){
        Nsteps = Serial.parseInt();
        //steps(dir,Nsteps,max_steps,160,hold,dir_old);
        Serial.println("Move in progress");
        while(Nsteps > 0){
          Nsteps = motor.moveStepsManual(Nsteps, 0,100);

          if(Serial.available()>0){
            char readVal = Serial.read();
            if (readVal == 's'){
              Serial.println("Emergency stop");
              break;
            }
          }
        }  
      }
      if (readVal == 'd'){
        dir_old = dir;
        dir = Serial.parseInt();
        motor.setDirManual(dir);
      }
      if (readVal == 'm'){
        microstep = Serial.parseInt();
        motor.setMicroStepSizeManual(microstep);
      }
      if (readVal == 'r'){
        rms_current = Serial.parseInt();
        motor.setRMSCurrentManual(rms_current);
      }
      if (readVal == 'e'){
        hold = Serial.parseInt();
        motor.setHoldManual(hold);
      }
      if (readVal == 't'){
        stepDelay = Serial.parseInt();
        motor.setStepDelayManual(stepDelay);
      }
      if (readVal == 'p'){
        Serial.println(motor.GetCurrentPosition());
      }
      if (readVal == 'a'){
        autoModeFlag = Serial.parseInt();
        if (autoModeFlag > 0)
        {
          motor.setTargetPosition(motor.GetCurrentPosition());
          Serial.println("Mode set to autonomus");
          Serial.println(motor.getTargetPosition());
        }
      }
    }
  }
}


void setup1() {
   // while (!motor.init_flag)
   // {
        
   // }
    sleep_ms(1000); // Sleep for 1 second
}


void loop1() {

  sleep_ms(1);
  motor.positionAvgFilter(0.05);
    //motor.getTotalPosition();
    //motor.getCurrentAngle



}

