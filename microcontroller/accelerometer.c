//
// Created by Tobias Hallingstad on 22/03/2022.
//

#include <stdio.h>
#include "accelerometer.h"
#include "hardware/i2c.h"
#include "pico/binary_info.h"

/**
 * @brief Initiate the accelerometer
 * Initiate accelerometer. Setts SDA and SCL pin to be I2C pins.
 * Setts the accelerometer register to be:
 * - High data rate
 * - Type of self test
 * @see Accelerometer doc
 * @param i2c Pointer to i2c instance
 * @param mode What mode the measurement shall use
 */
void initAccel(i2c_inst_t *i2c, enum Mode mode) {
    // Init GPIO pins to be i2c pint
    gpio_set_function(SDA_PIN, GPIO_FUNC_I2C);
    gpio_set_function(SCL_PIN, GPIO_FUNC_I2C);
    gpio_pull_up(SDA_PIN);
    gpio_pull_up(SCL_PIN);
    bi_decl(bi_2pins_with_func(SDA_PIN, SCL_PIN, GPIO_FUNC_I2C));

    // Modify registers in startup
    uint8_t buf[2];
    // Turn normal mode and 1.344kHz data rate on
    buf[0] = CTRL_REG1;
    buf[1] = 0x97;
    i2c_write_blocking(i2c, ADDRESS, buf, 2, false);

    // Turn self test
    buf[0] = CTRL_REG4;
    switch (mode) {
        case NO_SELF_TEST:
            buf[1] = 0x4;       // No self test
            break;
        case SELF_TEST_1:
            buf[1] = 0x0A;      // self test 1
            break;
        case SELF_TEST_2:
            buf[1] = 0x0C;      // self test 2
            break;
    }
    i2c_write_blocking(i2c, ADDRESS, buf, 2, false);
}

/***
 * Write to a value to a register on the accelerometer.
 * @param i2c Pointer to a i2c instance.
 * @param reg What register to write to.
 * @param buff Pointer to a buffer that stores what to write.
 * @param nbytes The number of bytes to write to the register.
 * @return Number of bytes writen, or PICO_ERROR_GENERIC if address not acknowledged, no device present.
 */
int writeReg(i2c_inst_t *i2c, const uint8_t reg, uint8_t *buff, const uint8_t nbytes) {
    int numBytesRead = 0;
    uint8_t msg[nbytes + 1];

    // Check to make sure caller is asking for 1 or more bytes
    if (nbytes < 1)
        return 0;

    // Append register address to front of data packet
    msg[0] = reg;
    for (int i = 0; i < nbytes; i++)
        msg[i + 1] = buff[i];

    // Write data to register(s) over i2C
    numBytesRead = i2c_write_blocking(i2c, ADDRESS, msg, (nbytes + 1), false);

    return numBytesRead;
}

/***
 * Read the values form a register.
 * @param i2c Pointer to i2c instance.
 * @param reg What register shall be read form.
 * @param buff Pointer to buffer the data shall be written to.
 * @param nbytes Number of bytes writen.
 * @return Number of bytes read, or PICO_ERROR_GENERIC if address not acknowledged, no device present.
 */
int readReg(i2c_inst_t *i2c, const uint8_t reg, uint8_t *buff, const uint8_t nbytes) {
    int numBytesRead = 0;

    // Check to make sure caller is asking for 1 or more bytes
    if (nbytes < 1)
        return 0;

    // Read data from register(s) over I2C
    i2c_write_blocking(i2c, ADDRESS, &reg, 1, true);

    numBytesRead = i2c_read_blocking(i2c, ADDRESS, buff, nbytes, false);
    return numBytesRead;
}

/***
 * @brief Reads measurement data form the accelerometer.
 * Reads the first, then second X, Y or Z data register form the accelerometer. Then the to 8-bit numbers are combined into a 16-bit number.
 *
 * @param i2c Pointer to i2c instance.
 * @param reg What data register to read from. Give OUT_X_l, OUT_Y_L or OUT_Z_L.
 * @return Value form register formatted correctly as a 16-bit number
 */
int16_t readData(i2c_inst_t *i2c, uint8_t reg) {
    // Read two bytes of data and store in a 16-bit data structure
    uint8_t lsb, msb;

    i2c_write_blocking(i2c, ADDRESS, &reg, 1, true);
    i2c_read_blocking(i2c, ADDRESS, &lsb, 1, false);

    // Move to next reg and read that
    reg |= 0x01;
    i2c_write_blocking(i2c, ADDRESS, &reg, 1, true);
    i2c_read_blocking(i2c, ADDRESS, &msb, 1, false);

    // Return the 16 bit measurement
    return (int16_t)((msb << 8) | lsb);
}

/***
 * Calculate if the address is reserved.
 * @param addr Address to test.
 * @return True if the address is reserved.
 */
bool reservedAddr(uint8_t addr) {
    return (addr & 0x78) == 0 || (addr & 0x78) == 0x78;
}

/***
 * @brief Print i2c connection status off all ports.
 * Read some data from each i2c address to determine if there are any i2c device contented to that address. If there is @ will be printed in that spot.
 * This is a good function to use if the address for a connected i2c device is not known.
 *
 * @param i2c Pointer to i2c instance.
 */
void busScan(i2c_inst_t *i2c) {
    printf("\nI2C Bus Scan\n");
    printf("  0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F\n");
    for (int addr = 0; addr < (1 << 7); ++addr) {
        if(addr%16==0) {
            printf("%02x ", addr);
        }

        int ret;
        uint8_t rxdata;

        if (reservedAddr(addr))
            ret = PICO_ERROR_GENERIC;
        else
            ret = i2c_read_blocking(i2c, addr, &rxdata, 1, false);

        printf(ret < 0 ? "." : "@");
        printf(addr % 16 == 15 ? "\n" : "  ");
    }
    printf("Done.\n");
}

/***
 * Print the status of the all control registers for the accelerometer.
 * @param i2c Pointer to i2c instance.
 */
void printRegisterStatus(i2c_inst_t *i2c) {
    uint8_t regVal;
    printf("Register status:\n");
    readReg(i2c, CTRL_REG0, &regVal, 1);
    printf("Reg 0: "BTB_PATTERN "\n", BTB(regVal));

    readReg(i2c, CTRL_REG0, &regVal, 1);
    printf("Reg 1: "BTB_PATTERN "\n", BTB(regVal));

    readReg(i2c, CTRL_REG0, &regVal, 1);
    printf("Reg 2: "BTB_PATTERN "\n", BTB(regVal));

    readReg(i2c, CTRL_REG0, &regVal, 1);
    printf("Reg 3: "BTB_PATTERN "\n", BTB(regVal));

    readReg(i2c, CTRL_REG0, &regVal, 1);
    printf("Reg 4: "BTB_PATTERN "\n", BTB(regVal));

    readReg(i2c, CTRL_REG0, &regVal, 1);
    printf("Reg 5: "BTB_PATTERN "\n", BTB(regVal));

    readReg(i2c, CTRL_REG0, &regVal, 1);
    printf("Reg 6: "BTB_PATTERN "\n", BTB(regVal));
    printf("----\n");
}