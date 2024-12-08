#ifndef AS5048B_TMC_stepper_h
#define AS5048B_TMC_stepper_h

#include <Arduino.h>
#include <SPI.h>
#include <TMCStepper.h>
// load initial parameters and Pins

#include <cmath>

// encoder things start
#include <Wire.h>
#include <Adafruit_I2CDevice.h>


#define encoder_res 16383

#define hysterese 2000
#define highHys encoder_res - hysterese
#define lowHys hysterese






class AS5048B_TMC_stepper {
        private:
        Adafruit_I2CDevice& i2c_dev;
        TMC2130Stepper& driver;

        

        double getCurrentAngle();

        

        int I2C_SdaPin ;
        int I2C_SclPin ;
        int encoderI2CAddress ;

        
        uint8_t encoderValuesAdress ;
        int encoderResolution ;
        int tolorance ;

        double current_position ;
        double old_position ;
        double IIRVal;
        double AvgPos ;
        
        //mutex angle_mutex;

        double target_position ;
        int rotations ;
        double angle_value ;
        double angle_value_old ;
        double position_error ;
        bool pos_hysterese_flag ;
        bool neg_hysterese_flag ;


        int stepCounter ;
        int dir ;
        int dir_old ;
        int Nsteps ;
        int steps ;
        int stepDelay ;
        int microstep ;
        int rms_current ;
        int hold ;
        bool homed ;
        int max_steps ;  
        int max_stepsManual ;


    public:
        // Constructor
        AS5048B_TMC_stepper(Adafruit_I2CDevice& dev, TMC2130Stepper& stepper);

        double GetCurrentPosition();
        

        double getTotalPosition();
        double positionAvgFilter(double IRR);

        void init();

        void setTargetPosition(double target);
        double getTargetPosition();

        double moveTowardsTarget();
        
        
        void setMaxTolorance(double tolorance);
        bool init_flag;

        int getMicroStepSize();
        void setMicroStepSizeManual(int microstep);

        int getRMSCurrent();
        void setRMSCurrentManual(int current);

        int getHold();
        void setHoldManual(bool hold);

        int getStepDelay();
        void setStepDelayManual(int delay);

        int getDir();
        void setDirManual(int dir);

        int moveStepsManual(int Nsteps,int max_stepsManual,int stopMaxSteps);

        void setMaxStepsManual(int max_stepsManual);
        


        
        

};

#endif