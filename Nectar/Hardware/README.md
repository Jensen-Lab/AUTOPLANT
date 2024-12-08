# Six-Axis Micro Manipulator Assembly Guide

## Overview
This document provides detailed instructions for assembling the Six-Axis Micro Manipulator.

## Hardware Requirements
A list of all required hardware is provided in the file `Parts.xlsx` including links to suppliers for purchase of commercial available parts. 
- Parts marked as 'bought' will have to be purchased.
- Parts marked as '3D Print' will have to be 3D printed. The corresponding `.stl` files can be found in the folder `3DPrints` sorted into the individual axis.
- Parts that are marked as `Workshop` are metal components. Files with dimensions are included in `Metal_Connectors`. These parts will have to be made or ordered.

### Additional Requirements
- Screws (M2, M3, M4 and M6 of adequate lengths)
- Screwdrivers (corresponding to the screws)

## Electronics Required
The wiring digrams (Schematics) for the electronic setup is included in the folder `PCB`.
- Schematic for the motor drivers. If all six axis are in use, this electronis set-up has to be repeated for each individual axis (For ordering a premade PCB: Gerber, BOM and Pick and Place Files are available for a manual control of the motor (see `software`for the difference in manual and automatic control)
- Schematic for the electronic setup of the `electrode` probe.
- Schematic for the electronis setup of the `laser`probe.

### Additional Requirements
- Wire extensions / Connetions
- Breadboards
- (Soldering Iron)

## Assembly Instructions
The `3DPrints/Robot.step` file illustrates how the different parts fit together. Remember to wire the motors according to the elctronic schematics after assembly.

If automatic mode is wished (as of now implemented only for x,y, and r), follow these steps:
- glue the magnet holder to the back of the motor (the free rotating piece)
- add the magnet
- add the sensor board on the shield
- attach the motorscrew spacer and then the sensor shield to the back of the motor (screws of the motor have to be exchanged for longer ones)
- add the wiring

### Step 1: Z-Axis
- The axis is the base. Add the brackets at the desired height and attach the platform.
- The motor is connected via the metal connector and kept in place with the clamp, plate and block.

### Step 2: Rotational-Axis 1
- A base plate for extra height is the base.
- Attach the Stage to this platform in such a way that the connection to the motor will cross over the flat corner.
- Attach the base to the Z-axis.
- Add the motor via the metal connector. It is held in place at the appropiate distance on the Z axis with the printed motor holder

### Step 3: X-Axis and Y-Axis
- For extra height place the height plate in between the rotational 1 axis and the x axis.
- Attach the motors to the motor holders (x and y).
- Attach the moving part of the x stage (bottom) to the y holder
- Attach the x stage to the X-Stage print (on the non movable part)
- Now the printed stages x and y should be just on top of each other.
- Connect the motor holder and the x stage print with the connection piece and connect the motor shaft with the x axis via the metal connection.
- Connect the y stage onto the movable part of the x stage
- Connect the y axis with the motor shaft via the metal connector.
- Connect the stage system to rotation 1.

### Step 4: Rotational Axis 2
- Attach the motor holder to the y stage
- Add the motor to the holder (be careful when exchanhing the screws of the motor for attachment, so the gears do not fall out of the box.

### Step 5: R-Axis
- Add the motor to the holder
- Add the stage to the holder and connect the stage and motor via the metal connector.
- Add the metal rod to the rod holder and attach the piece to the stage
- Attach the stage to the rotatonal axis 2

## Connection with the PC
For setting up the software see the `README.md` file in the `Software` folder
