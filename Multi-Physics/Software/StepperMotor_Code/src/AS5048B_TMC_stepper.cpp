#include <AS5048B_TMC_stepper.h>
#include <SPI.h>
#include <TMCStepper.h>
#include <Adafruit_I2CDevice.h>
#include <main_TMC2130.h>
#include <cmath>



    AS5048B_TMC_stepper::AS5048B_TMC_stepper(Adafruit_I2CDevice& dev, TMC2130Stepper& stepper)
        : i2c_dev(dev), driver(stepper) {

        encoderValuesAdress = 0XFA+4;
        encoderResolution = 16384;
        tolorance = 0.25;
        IIRVal = 0.80;

        current_position = 0;
       

        AvgPos = 0;
        

        target_position = 0;
        position_error = 0;

        rotations = 0;
        angle_value = 0;
        angle_value_old = 0;
        
        pos_hysterese_flag = true;
        neg_hysterese_flag = true;


        stepCounter = 0;
        dir = 0;
        dir_old = 0;
        steps = 10000;
        stepDelay = 200;
        microstep = 16;
        rms_current = 950;
        hold = 1;
        homed = false;
        max_steps = 1000;  
        max_stepsManual = 100000;

        

        bool init_flag = false;

        }


    void AS5048B_TMC_stepper::init(){
        pinMode(EN_PIN, OUTPUT);
        pinMode(STEP_PIN, OUTPUT);
        pinMode(DIR_PIN, OUTPUT);
        pinMode(CS_PIN, OUTPUT);
        pinMode(STALL_PIN, INPUT_PULLUP);

        SPI.begin(); // Begin SPI communication
        driver.begin();
        driver.rms_current(rms_current); // Set motor RMS current
        
        driver.microsteps(microstep);   // Set microsteps
        driver.en_pwm_mode(true);

        // driver.diag1_stall(true);   // for x and y stallguard
        // driver.diag1_stall(false);  // disable stallguard
        driver.TPWMTHRS(10);           // disable stallguard
        driver.pwm_ampl(255);          // disable stallguard

        driver.TCOOLTHRS(0xFFFFF); // Maximum coolstep threshold
        driver.semin(5);
        driver.semax(2);
        driver.sedn(0b01);
        // driver.sgt(6);              // for x and y stallguard 

        digitalWrite(STEP_PIN,HIGH);
        delayMicroseconds(100);
        digitalWrite(STEP_PIN,LOW);
        delayMicroseconds(100);
        digitalWrite(EN_PIN, LOW);     //hold motor position

        i2c_dev.begin();
        i2c_dev.setSpeed(400000); // Set the I2C clock to 400kHz
        sleep_ms(100); // Sleep for 100ms

        for (size_t i = 0; i < 10; i++)
        {
            sleep_ms(100);
            getCurrentAngle();
        }
        
        sleep_ms(100);
        double angle_value_old = getCurrentAngle();

        if (angle_value_old > encoder_res/2)
        {
            rotations = -1;
        } else
        {
            rotations = 0;
        }
        

        
        //for (size_t i = 0; i < 100; i++)
        // first_pos = positionAvgFilter(0.2);
        
        
        AvgPos = angle_value_old;
        target_position = getTotalPosition();
        init_flag = true;
        
    }


    int AS5048B_TMC_stepper::getMicroStepSize(){
        return microstep;
    }
    void AS5048B_TMC_stepper::setMicroStepSizeManual(int microstep){
        this->microstep = microstep;
        driver.microsteps(microstep);
    }

    int AS5048B_TMC_stepper::getRMSCurrent(){
        return rms_current;
    }
    void AS5048B_TMC_stepper::setRMSCurrentManual(int current){
        this->rms_current = current;
        driver.rms_current(current);
    }

    int AS5048B_TMC_stepper::getHold(){
        return hold;
    }
    void AS5048B_TMC_stepper::setHoldManual(bool hold){
        this->hold = hold;
    }

    int AS5048B_TMC_stepper::getStepDelay(){
        return stepDelay;
    }
    void AS5048B_TMC_stepper::setStepDelayManual(int delay){
        this->stepDelay = delay;
    }



    void AS5048B_TMC_stepper::setMaxTolorance(double tolorance){
        this->tolorance = tolorance;
    }

    double AS5048B_TMC_stepper::getTargetPosition(){
        return target_position;
    }

    int AS5048B_TMC_stepper::getDir(){
        return dir;
    }
    void AS5048B_TMC_stepper::setDirManual(int dir){
        this->dir = dir;
        driver.shaft(dir);
    }

    void AS5048B_TMC_stepper::setTargetPosition(double target){
        target_position = target;
    }

    double AS5048B_TMC_stepper::positionAvgFilter(double IRR) {
    // Implementation of the position average filter

        AvgPos = AvgPos* (1-IRR)+ getTotalPosition() * IRR;
    
        //while(!rp2040.fifo.available())
        
        //rp2040.fifo.pop();
        //angle_mutex.lock();
        current_position = AvgPos;
        //angle_mutex.unlock();
        //rp2040.fifo.push(1);
        

    return AvgPos; // Placeholder return
    }


    double AS5048B_TMC_stepper::GetCurrentPosition(){
        double temp_current_position = 0;

        //int command = 1;
        //rp2040.fifo.push(command);

        //while(!rp2040.fifo.available())
        rp2040.fifo.idleOtherCore();
        temp_current_position = current_position;
        rp2040.fifo.resumeOtherCore();
        //rp2040.fifo.pop();
        

        return temp_current_position;
    }

    double AS5048B_TMC_stepper::getCurrentAngle() {
    double current_angle = 0;
    uint8_t data[2];
    i2c_dev.write_then_read(&encoderValuesAdress, 1, data, 2,false); 
    current_angle = (uint16_t)data[0]<<6 ;
    current_angle += (uint16_t)data[1] & 0b111111;
    return current_angle;
    
    }

    double AS5048B_TMC_stepper::getTotalPosition() {
        

      angle_value = getCurrentAngle();

    //   if (angle_value_old > highHys && angle_value < lowHys && pos_hysterese_flag == true) // If the angle goes over 0 point from high to low and the positive hysteresis flag is set
    //  {
    //     rotations++; // Increment the rotations
    //     pos_hysterese_flag = false; // Reset the hysteresis flag
    //     neg_hysterese_flag = true; // Set the hysteresis flag for the other direction
    //   } else if (angle_value_old < lowHys && angle_value > highHys && neg_hysterese_flag == true) // If the angle goes over 0 point from low to high and the negative hysteresis flag is set
    //   {
    //     rotations--; // Decrement the rotations
    //     pos_hysterese_flag = true; // Set the hysteresis flag for the other direction
    //     neg_hysterese_flag = false; // Reset the hysteresis flag
    //   } else if (angle_value_old > highHys && angle_value < highHys) // If the angle crosses the high hysteresis range
    //   {
    //     neg_hysterese_flag = true; // Set the hysteresis flag to allow negative rotation incrementation
    //   } else if (angle_value_old < lowHys && angle_value > lowHys) // If the angle crosses the low hysteresis range
    //   {
    //     pos_hysterese_flag = true; // Set the hysteresis flag to allow positive rotation incrementation
    //   }

      if (angle_value_old > highHys && angle_value < lowHys) {
        // If the angle goes over 0 point from high to low
        rotations++; // Increment the rotations 
      } else if (angle_value_old < lowHys && angle_value > highHys) {
        // If the angle goes over 0 point from low to high
        rotations--; // Decrement the rotations
      }
      
      angle_value_old = angle_value;

      if (rotations < 0) // If the rotations are negative
      {
        
        return  angle_value - encoder_res + (rotations+1)*encoder_res;
      } else
      {
         // Calculate the current position
         return  angle_value + rotations*encoder_res; // Calculate the current position
      }
        
    //return current_position; // Placeholder return
    }


    double AS5048B_TMC_stepper::moveTowardsTarget(){
        //double test = 0;
        int step_diff = 0;
        int steps_to_move = 0;


        double temp_current_position = 0;

        //int command = 1;
        //rp2040.fifo.push(command);

        //while(!rp2040.fifo.available())

        temp_current_position = GetCurrentPosition();
        //rp2040.fifo.pop();
        

        position_error = (target_position - temp_current_position);
        //Serial.println(temp_current_position);

        if ( abs(position_error) > tolorance){
            //test = position_error;
            if (position_error > 0)
            {
                dir_old = dir;
                dir = 0;
                driver.shaft(dir);  
            }
            else if (position_error < 0)
            {   
                
                dir_old = dir;
                dir = 1;
                driver.shaft(dir);
            }
            microstep = 16;
            step_diff = abs(position_error)/(encoder_res/(400*microstep));
            
            if(step_diff<200){         // for all axis
        
                stepDelay = 5000;       // for all axis
                //Serial.println("slow");
                //driver.rms_current(950);
                steps_to_move = step_diff;
                microstep = 32;

                if (steps_to_move > 10){
                steps_to_move = 10;
                }
            

            } else if(step_diff<1000){         // for all axis
        
                stepDelay = 1000;       // for all axis
                //Serial.println("slow");
                //driver.rms_current(950);
                steps_to_move = (step_diff-190)*0.7;

            }
            else
            {
                stepDelay = 200;
                //Serial.println("fast");
                //driver.rms_current(850);
            
                steps_to_move = (step_diff-950)*0.7;
                
            }

            if (steps_to_move > max_steps){
                steps_to_move = max_steps;
            }
            
            
            if (steps_to_move <= 0){                         
                if (dir_old != dir){
                    digitalWrite(EN_PIN, LOW);
                    for (int i = 0; i < step_diff; i++){
                        digitalWrite(STEP_PIN,HIGH);
                        delayMicroseconds(stepDelay);
                        digitalWrite(STEP_PIN,LOW);
                        delayMicroseconds(stepDelay);
                    }
                    dir_old = dir;
                    digitalWrite(EN_PIN, HIGH);
                }
            }
            
            for(int i = 0; i<steps_to_move; i++){
                
                        digitalWrite(STEP_PIN,HIGH);
                        delayMicroseconds(stepDelay);
                        digitalWrite(STEP_PIN,LOW);
                        delayMicroseconds(stepDelay);
                        
                 
                // if (i%100 == 0){
                //     positionAvgFilter(IIRVal,4);

                // }   
            }

            digitalWrite(EN_PIN, LOW);
        }
    //return target_position - positionAvgFilter(IIRVal,4); 
    return 0; 
    }

void AS5048B_TMC_stepper::setMaxStepsManual(int max_stepsManual){
    this->max_stepsManual = max_stepsManual;
}

int AS5048B_TMC_stepper::moveStepsManual(int Nsteps,int max_stepsManual,int stopMaxSteps){
    // change the driver current according to number of steps
    this->max_stepsManual = max_stepsManual;
    
    digitalWrite(EN_PIN, LOW);

    if(Nsteps<1000){            // for all axis
    // if(Nsteps<10000){        //for Z

        stepDelay = 1000;       // for all axis
        // stepDelay = 200000;  // for stab and rot2
    }
    else{
        stepDelay = 200;
    }

    // account for backlash in chnaging direction
    // if (Nsteps <= 500){                         // for x,stab
    // if (Nsteps <= 0){                           // for y
    // if (Nsteps <= 1000){                        // for rot
    // if (Nsteps <= 2000){                        // for Z
    // if (Nsteps <= 0){                           // for rot 2
    if (Nsteps <= 0){                           // for no backlash

        if (dir_old != dir){
            digitalWrite(EN_PIN, LOW);
            for (int i = 0; i < Nsteps; i++){
                digitalWrite(STEP_PIN,HIGH);
                delayMicroseconds(stepDelay);
                digitalWrite(STEP_PIN,LOW);
                delayMicroseconds(stepDelay);
            }
            dir_old = dir;

            if (hold == 0){
                digitalWrite(EN_PIN, HIGH);
            }
            else{
                digitalWrite(EN_PIN, LOW);
            }
        }
    }

    int stepsToMove = 0;
    if (Nsteps > stopMaxSteps)
    {
        stepsToMove = stopMaxSteps;
    } else
    {
        stepsToMove = Nsteps;
    }
    

    for(int i = 0; i<stepsToMove; i++){
        if (dir == 1){
            //Serial.println(stepCounter);
            if (max_stepsManual > 0){
                if (stepCounter<max_stepsManual){
                    digitalWrite(STEP_PIN,HIGH);
                    delayMicroseconds(stepDelay);
                    digitalWrite(STEP_PIN,LOW);
                    delayMicroseconds(stepDelay);
                    stepCounter += 1;
                }
                else if(stepCounter>max_stepsManual){
                    Serial.println("You are out of space, too many steps chosen");
                    break;
                }
            }
            else if (max_stepsManual == 0){
                digitalWrite(STEP_PIN,HIGH);
                delayMicroseconds(stepDelay);
                digitalWrite(STEP_PIN,LOW);
                delayMicroseconds(stepDelay);
                stepCounter += 1;
            }
        }else{
            if (max_stepsManual > 0){
                if (stepCounter>0){
                    digitalWrite(STEP_PIN,HIGH);
                    delayMicroseconds(stepDelay);
                    digitalWrite(STEP_PIN,LOW);
                    delayMicroseconds(stepDelay);
                    stepCounter -= 1;
                }
                else{
                    Serial.println("You are out of space, too many steps chosen");
                    break;
                }
            }else{
                digitalWrite(STEP_PIN,HIGH);
                delayMicroseconds(stepDelay);
                digitalWrite(STEP_PIN,LOW);
                delayMicroseconds(stepDelay);
                stepCounter -= 1;
            }
        }
    }
    if (hold == 0){
        digitalWrite(EN_PIN, HIGH);
    }
    else{
        digitalWrite(EN_PIN, LOW);
    }
    if (Nsteps > stopMaxSteps)
    {
        return Nsteps - stopMaxSteps;
    } else
    {
        return 0;
    }
}