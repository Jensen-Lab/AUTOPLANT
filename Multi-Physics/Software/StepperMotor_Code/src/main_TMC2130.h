/** motor driver TMC2130
  * Raspberry Pi Pico - stepper motor driver support

  * The defaults assumes a TMC2130 stepper driver has been wired up to the Pico as follows:

  *   GND   -> any Pico GND
  *   3V    -> 3V3_EN
  *   DIR   -> GP14
  *   STEP  -> GP15
  *   MISO  -> GP0
  *   CS    -> GP1
  *   SCK   -> GP2
  *   MOSI  -> GP3

  * remember to include a resistor (about 3.3kOhm) between the readout DIR Pin and any GND
  * remember to have the GND on minus (black cable) and Power supply on + (white cable)
*/

// define PINs
// Raspberry Pi Pico:
#define EN_PIN    18   //enable
#define DIR_PIN   14   //direction
#define STEP_PIN  15   //step
#define SW_MISO   0    //Master In Slave Out (MISO)
#define CS_PIN    1    //chip select
#define SW_SCK    2    //Slave Clock (SCK)
#define SW_MOSI   3    //Master Out Slave In (MOSI)

#define R_SENSE     0.11f   // depends on the motor driver

#define STALL_PIN 22 // diag pin
