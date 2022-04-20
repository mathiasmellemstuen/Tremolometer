/**
 * @file accelerometer.h
 * @brief Accelerometer code.
 *
 * Pin layout on Tiny 2040:
 *  - SCL pin = A1 = Yellow
 *  - SDA pin = A0 = Blue
 */
#ifndef TREMOLOMETER_ACCELEROMETER_H
#define TREMOLOMETER_ACCELEROMETER_H

#include "pico/stdlib.h"
#include "hardware/i2c.h"

// Macro for printing int_8 to binary format
#define BTB_PATTERN "%i -> %c%c%c%c%c%c%c%c";      //!< Pattern for printing a int_8 to it bit representation.

/**
 * What to supply BTB_PATTERN with for int_8 to be printed as bits.
 * @param byte The int_8 to print as bites.
 */
#define BTB(byte) \
  byte,                      \
  (byte & 0x80 ? '1' : '0'), \
  (byte & 0x40 ? '1' : '0'), \
  (byte & 0x20 ? '1' : '0'), \
  (byte & 0x10 ? '1' : '0'), \
  (byte & 0x08 ? '1' : '0'), \
  (byte & 0x04 ? '1' : '0'), \
  (byte & 0x02 ? '1' : '0'), \
  (byte & 0x01 ? '1' : '0')

/*
 * Notes:
 * Yellow -> SCL -> 6
 * Blue   -> SDA -> 7
 */
static const uint SCL_PIN = 27; //!< i2c clock pin.
static const uint SDA_PIN = 26; //!< i2c data pin.

/*
 * Registers
 */
static const uint8_t WHO_AM_I = 0x0E;   //!< Address to WHO_AM_I register.
static const uint8_t ADDRESS = 0x18;    //!< The address of the accelerometer.
static const uint8_t STATUS_REG = 0x27; //!< Address to the STATUS_REG.

// Control registers
static const uint8_t CTRL_REG0 = 0x1E;      //!< SDO_PU_DISC, 0, 0, 1, 0, 0, 0, 0
static const uint8_t CTRL_REG1 = 0x20;      //!< ODR3, ODR2, ODR1, ODR0, LPen, Zen, Yen, Xen
static const uint8_t CTRL_REG2 = 0x21;      //!< HPM1, HPM0, HPCF2, HPCF1, FDS, HPCLICK, HP_IA2, HP_IA1
static const uint8_t CTRL_REG3 = 0x22;      //!< I1_CLICK, I1_IA1, I1_IA2, I1_ZYXDA, I1_321DA, I1_WTM, I1_OVERRUN
static const uint8_t CTRL_REG4 = 0x23;      //!< BDU, BLE, FS1, FS0, HR, ST1, ST0, SIM
static const uint8_t CTRL_REG5 = 0x24;      //!< BOOT, FIFO_EN, --, --, LIR_INT1, D4D_INT1, LIR_INT2, D4D_INT2
static const uint8_t CTRL_REG6 = 0x25;      //!< I2_CLICK, I2_IA1, I2_IA2, I2_BOOT, I2_ACT, -- INT_POLARITY, --
static const uint8_t TMP_CFG_REG = 0x1F;    //!< ADC_EN, TEMP_EN, 0, 0, 0, 0, 0, 0

// X,Y,Z register
static const uint8_t OUT_X_L = 0x28;    //!< First 8 bits of x reading.
static const uint8_t OUT_X_H = 0x29;    //!< Last 8 bits of x reading.
static const uint8_t OUT_Y_L = 0x2A;    //!< First 8 bits of y reading.
static const uint8_t OUT_Y_H = 0x2B;    //!< Last 8 bits of y reading.
static const uint8_t OUT_Z_L = 0x2C;    //!< First 8 bits of z reading.
static const uint8_t OUT_Z_H = 0x2D;    //!< Last 8 bits for z reading.

// Other
static const float SENSITICITY_2G = 1.0f / 256; //!< (g/LSB).
static const float EARTH_GRAVITY = 9.80665;     //!< Earth's gravity in [m/s^2].

/**
 * Defining different measurement modes for the accelerometer.
 */
enum Mode {
    NO_SELF_TEST=0, //!< No self test.
    SELF_TEST_1=1,  //!< Self test mode 1.
    SELF_TEST_2=2   //!< Self test mode 2.
};

/**
 * @brief Initiate the accelerometer
 * Initiate accelerometer. Setts SDA and SCL pin to be I2C pins.
 * Setts the accelerometer register to be:
 * - High data rate
 * - Type of self test
 *
 * @see Accelerometer doc
 * @param i2c Pointer to i2c instance
 * @param mode What mode the measurement shall use
 */
void initAccel(i2c_inst_t *i2c, enum Mode mode);

/**
 * @brief Write value to  register.
 * Write to a value to a register on the accelerometer.
 *
 * @param i2c Pointer to a i2c instance.
 * @param reg What register to write to.
 * @param buff Pointer to a buffer that stores what to write.
 * @param nbytes The number of bytes to write to the register.
 * @return Number of bytes writen, or PICO_ERROR_GENERIC if address not acknowledged, no device present.
 */
int writeReg(i2c_inst_t *i2c, const uint8_t reg, uint8_t *buff, const uint8_t nbytes);

/**
 * @brief Read data from a register.
 * Read the values form a register.
 *
 * @param i2c Pointer to i2c instance.
 * @param reg What register shall be read form.
 * @param buff Pointer to buffer the data shall be written to.
 * @param nbytes Number of bytes writen.
 * @return Number of bytes read, or PICO_ERROR_GENERIC if address not acknowledged, no device present.
 */
int readReg(i2c_inst_t *i2c, const uint8_t reg, uint8_t *buff, const uint8_t nbytes);

/**
 * @brief Reads measurement data form the accelerometer.
 * Reads the first, then second X, Y or Z data register form the accelerometer. Then the to 8-bit numbers are combined into a 16-bit number.
 *
 * @param i2c Pointer to i2c instance.
 * @param reg What data register to read from. Give OUT_X_l, OUT_Y_L or OUT_Z_L.
 * @return Value form register formatted correctly as a 16-bit number
 */
int16_t readData(i2c_inst_t *i2c, uint8_t reg);

/**
 * @brief Check if a address is reserved.
 * Calculate if the address is reserved.
 *
 * @param addr Address to test.
 * @return True if the address is reserved.
 */
bool reservedAddr(uint8_t addr);

/**
 * @brief Print i2c connection status off all ports.
 * Read some data from each i2c address to determine if there are any i2c device contented to that address. If there is @ will be printed in that spot.
 * This is a good function to use if the address for a connected i2c device is not known.
 *
 * @param i2c Pointer to i2c instance.
 */
void busScan(i2c_inst_t *i2c);

/**
 * @brief Print status for all CTRL registers.
 * Print the status of the all control registers for the accelerometer.
 *
 * @param i2c Pointer to i2c instance.
 */
void printRegisterStatus(i2c_inst_t *i2c);

#endif //TREMOLOMETER_ACCELEROMETER_H
