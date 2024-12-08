# Six-Axis Movement System Control Web App

## Overview
This web application provides an interface to control a six-axis movement system integrated with camera functionalities (Basler acA1920-150uc), acquisition settings, and end effector controls. The app allows users to manipulate and monitor their equipment through a web interface.

## Features
- **Six-Axis Movement Control**: Control over all six axis.
- **Camera Integration**: Live camera view to monitor operations.
- **Acquisition Settings**: Customizable settings to adjust the camera acquisition parameters.
- **End Effector Control**: Interface to access the Laser and Electrode probes.

## Requirements
- Compatible with Linux systems.
- Requires Python 3.8 or newer.
- Dependencies are listed in the `requirements.txt` file.
- Requires the six axis micromanipulator as designed here

## Folders
- **Micromanipulator App**: Here the user interface is designed.
- **Stepper Motor Code**: This code should be uploaded to the microcontrollers (`Raspberry Pi Picos`) of the stepper motors. It defines all necessary movement control, use eg `PlatformIO Core` for uploading the code
- **Electrode**: This code should be uploaded to the microcontroller (`Arduino Nano`) of the Electrode to allow for control of the switch, use eg `PlatformIO Core` for uploading the code.
- **Laser**: This code should be uploaded to the microcontroller (`Arduino Nano`) of the Laser to allow for control of the switch, use eg `PlatformIO Core` for uploading the code.

## Installation
To set up the web app on your local system, follow these steps:
1. Clone the repository to your local machine.
2. Navigate to the cloned directory.
3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
4. Inside of `Micromanipulator App/website/view.py` change the following:
   - `path`: change to the path that should be used to save images and videos
   - `SN_dict`: change to the serial numbers of the respective used microcontrollers

## Use
To open the web application, follow these steps:
1. Navigate to the directory containing `main.py` (in `Micromanipulator App/`)
2. run
    ```bash
   python main.py
4. Access the web app through your browser at the specified local address

### Camera
1. Turn on the camera (`Real-Time Display Basler`) -  Make sure the camera is connected via USB
2. Change exposure, gain blacklevel and gamma value accordingly (`Camera Settings`)
3. Change the total time of a video to be taken and the fps value (`Video Acquisition Settings`)
4. Take an image or video

### Axes
- Connect an axis and wait for the green symbol to appear next to the axis name (`Connection`)
- Input the number of steps in `manual` mode in `Robot Control` to move that amount; in `automatic` mode input the positional change
    (Note: in `automatic` mode a magnet is used to control the positioning)
    (Note: The tick box next to some axes in `Robot Control` changes the movement mode from `manual` to `automatic` when ticked)
- Movement the axis with the corresponding arrows (`Robot Control`)
  
### Electrode 
`Electroshocker Settings`
- Change the total on time of the electrode (eg 60s)
- Change the time the electrode is on (eg 1s)
- Change the time the electrode is off (eg 10s)

### Laser
`Laser Settings`
- Change the total on time of the laser (eg 60s)
- Change the time the laser is on (eg 1s)
- Change the time the laser is off (eg 10s)

## Liscence

