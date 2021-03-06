#include <stdio.h>
#include "accelerometer.h"
#include "hardware/i2c.h"
#include "pico/binary_info.h"

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
    buf[1] = 0x47;
    //buf[1] = 0x97;
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

void busScan(i2c_inst_t *i2c) {
    printf("\nI2C Bus Scan\n");
    printf("  0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F\n");
    for (int addr = 0; addr < (1 << 7); ++addr) {
        if (addr%16==0)
            printf("%02x ", addr);

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