#include <sys/cdefs.h>
#include <malloc.h>
#include <stdio.h>
#include "pico/stdlib.h"
#include "pico/binary_info.h"
#include "hardware/i2c.h"
#include <math.h>
#include "data.h"
#include "usbTransfer.h"
#include "led.h"

#include "acelerometer.h"

#define BTB_PATTERN "%i -> %c%c%c%c%c%c%c%c"
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

// I2C address
static const uint SCL_PIN = 6;
static const uint SDA_PIN = 7;

const int ADD = 0x18;
const uint8_t CTRL_REG_1 = 0x20;
const uint8_t CTRL_REG_4 = 0x23;
const uint8_t TEMP_CFG_REG = 0xC0;

i2c_inst_t *i2c;

int reg_write(i2c_inst_t *i2cP, const uint addr, const uint8_t reg, uint8_t *buff, const uint8_t nbytes);
int reg_read(i2c_inst_t *i2cP, const uint addr, uint8_t reg, uint8_t *buff, const uint8_t nbytes);

int reg_write(i2c_inst_t *i2cP, const uint addr, const uint8_t reg, uint8_t *buff, const uint8_t nbytes) {
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
    i2c_write_blocking(i2cP, 0x33, msg, (nbytes + 1), false);

    return numBytesRead;
}

int reg_read(i2c_inst_t *i2cP, const uint addr, uint8_t reg, uint8_t *buff, const uint8_t nbytes) {
    int numBytesRead = 0;

    // reg |= 80;

    // Check to make sure caller is asking for 1 or more bytes
    if (nbytes < 1)
        return 0;

    // Read data from register(s) over I2C
    i2c_write_blocking(i2cP, 0x33, &reg, 1, true);

    numBytesRead = i2c_read_blocking(i2cP, 0x32, buff, nbytes, false);
    return numBytesRead;
}

void lis3dh_init() {
    uint8_t buf[2];
    int status;

    // Turn normal mode and 1.344kHz data rate on
    buf[0] = CTRL_REG1;
    buf[1] = 0x97;
    status = i2c_write_blocking(i2c, ADDRESS, buf, 2, false);
    if (status == PICO_ERROR_TIMEOUT) {
        printf("WRITE ERROR: timeout\n");
        while (1) {}
    }
    else if (status == PICO_ERROR_GENERIC) {
        printf("WRITE ERROR: generic | address nok acknowledged!\n");
        while (1) {}
    }

    // Turn self test
    buf[0] = CTRL_REG4;
    buf[1] = 0x02;
    status = i2c_write_blocking(i2c, ADDRESS, buf, 2, false);
    if (status == PICO_ERROR_TIMEOUT) {
        printf("WRITE ERROR: timeout\n");
        while (1) {}
    }
    else if (status == PICO_ERROR_GENERIC) {
        printf("WRITE ERROR: generic | address nok acknowledged!\n");
        while (1) {}
    }
}

void lis3dh_calc_value(uint16_t raw_value, float *final_value, bool isAccel) {
    // Convert with respect to the value being temperature or acceleration reading
    float scaling;
    float senstivity = 0.004f; // g per unit

    if (isAccel == true) {
        scaling = 64 / senstivity;
    } else {
        printf("%i\n", raw_value);
        scaling = 64;
    }

    // raw_value is signed
    *final_value = (float) ((int16_t) raw_value) / scaling;
}

void lis3dh_read_reg(uint8_t reg, uint8_t *val) {
    int status;

    status = i2c_write_blocking(i2c, ADDRESS, &reg, 1, true);
    if (status == PICO_ERROR_TIMEOUT) {
        printf("WRITE ERROR: timeout\n");
        while (1) {}
    }
    else if (status == PICO_ERROR_GENERIC) {
        printf("WRITE ERROR: generic | address not acknowledged!\n");
        while (1) {}
    }

    status = i2c_read_blocking(i2c, ADDRESS, val, 1, false);
    if (status == PICO_ERROR_TIMEOUT) {
        printf("READ ERROR: timeout\n");
        while (1) {}
    }
    else if (status == PICO_ERROR_GENERIC) {
        printf("READ ERROR: generic | address not acknowledged!\n");
        while (1) {}
    }

    // printf("Reg(%i): " BTB_PATTERN "\n", reg, BTB(*val));
}

void lis3dh_read_data(uint8_t reg, float *final_value, bool IsAccel) {
    // Read two bytes of data and store in a 16 bit data structure
    uint8_t lsb;
    uint8_t msb;
    uint16_t raw_accel;
    i2c_write_blocking(i2c, ADDRESS, &reg, 1, true);
    i2c_read_blocking(i2c, ADDRESS, &lsb, 1, false);

    reg |= 0x01;
    i2c_write_blocking(i2c, ADDRESS, &reg, 1, true);
    i2c_read_blocking(i2c, ADDRESS, &msb, 1, false);

    raw_accel = (msb << 8) | lsb;

    printf("%i\n", raw_accel);

    lis3dh_calc_value(raw_accel, final_value, IsAccel);
}

void lis3dh_print_register_status() {
    uint8_t regVal;
    printf("Register status:\n");
    lis3dh_read_reg(CTRL_REG0, &regVal);
    printf("Reg 0: "BTB_PATTERN "\n", BTB(regVal));

    lis3dh_read_reg(CTRL_REG1, &regVal);
    printf("Reg 1: "BTB_PATTERN "\n", BTB(regVal));

    lis3dh_read_reg(CTRL_REG2, &regVal);
    printf("Reg 2: "BTB_PATTERN "\n", BTB(regVal));

    lis3dh_read_reg(CTRL_REG3, &regVal);
    printf("Reg 3: "BTB_PATTERN "\n", BTB(regVal));

    lis3dh_read_reg(CTRL_REG4, &regVal);
    printf("Reg 4: "BTB_PATTERN "\n", BTB(regVal));

    lis3dh_read_reg(CTRL_REG5, &regVal);
    printf("Reg 5: "BTB_PATTERN "\n", BTB(regVal));

    lis3dh_read_reg(CTRL_REG6, &regVal);
    printf("Reg 6: "BTB_PATTERN "\n", BTB(regVal));
    printf("----\n");
}

bool reserved_addr(uint8_t addr) {
    return (addr & 0x78) == 0 || (addr & 0x78) == 0x78;
}

void bus_scan() {
    printf("\nI2C Bus Scan\n");
    printf("  0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F\n");
    for (int addr = 0; addr < (1 << 7); ++addr) {
        if(addr%16==0) {
            printf("%02x ", addr);
        }

        int ret;
         uint8_t rxdata;

         if (reserved_addr(addr))
             ret = PICO_ERROR_GENERIC;
         else
             ret = i2c_read_blocking(i2c_default, addr, &rxdata, 1, false);

         printf(ret < 0 ? "." : "@");
         printf(addr % 16 == 15 ? "\n" : "  ");
    }
    printf("Done.\n");
}

/*
 * Structs
 */
typedef struct Vec3i Vec3i;
struct Vec3i {
    int16_t x, y, z;
};

typedef struct Vec3f Vec3f;
struct Vec3f {
    float x, y, z;
};

#pragma clang diagnostic push
#pragma ide diagnostic ignored "EndlessLoop"

int main(void) {
    float x_accel, y_accel, z_accel, temp;

    usbInit();

    // Pins
    i2c = i2c1;

    // Buffer to store raw reads
    uint8_t data[6];

    // Init serial
    stdio_init_all();

    // Init I2C port
    i2c_init(i2c, 400 * 1000);

    // Init I2C pins
    gpio_set_function(SDA_PIN, GPIO_FUNC_I2C);
    gpio_set_function(SCL_PIN, GPIO_FUNC_I2C);
    gpio_pull_up(SDA_PIN);
    gpio_pull_up(SCL_PIN);
    bi_decl(bi_2pins_with_func(SDA_PIN, SCL_PIN, GPIO_FUNC_I2C));

    sleep_ms(3000);

    printf("init\n");
    // bus_scan();
    lis3dh_init();
    lis3dh_print_register_status();

    uint8_t value;
    lis3dh_read_reg(WHO_AM_I, &value);

    // Wait before taking measurements
    sleep_ms(2000);

    // waitForStartSignal();

    while(1) {
        /*
        sleep_ms(10000);

        lis3dh_read_data(0x28, &x_accel, true);
        lis3dh_read_data(0x2A, &y_accel, true);
        lis3dh_read_data(0x2C, &z_accel, true);
        lis3dh_read_data(CTRL_REG4, &temp, false);

        // Acceleration is read as a multiple of g (gravitational acceleration on the Earth's surface)
        printf("ACCELERATION VALUES: \n");
        printf("X acceleration: %.3fg\n", x_accel);
        printf("Y acceleration: %.3fg\n", y_accel);
        printf("Z acceleration: %.3fg\n", z_accel);

        sleep_ms(10000);
         */
    }

    return 0;
}
#pragma clang diagnostic pop


/*
printf("Reg status:\n");
data[0] = 0;

reg_read(i2c, i2cAddr, CTRL_REG0, &data[0], 8);
printf("Reg 0: %i | "BTB_PATTERN"\n", data[0], BTB(data[0]));

reg_read(i2c, i2cAddr, CTRL_REG1, &data[0], 8);
printf("Reg 1: %i | "BTB_PATTERN"\n", data[0], BTB(data[0]));

reg_read(i2c, i2cAddr, CTRL_REG2, &data[0], 8);
printf("Reg 2: %i | "BTB_PATTERN"\n", data[0], BTB(data[0]));

reg_read(i2c, i2cAddr, CTRL_REG3, &data[0], 8);
printf("Reg 3: %i | "BTB_PATTERN"\n", data[0], BTB(data[0]));

reg_read(i2c, i2cAddr, CTRL_REG4, &data[0], 8);
printf("Reg 4: %i | "BTB_PATTERN"\n", data[0], BTB(data[0]));

reg_read(i2c, i2cAddr, CTRL_REG5, &data[0], 8);
printf("Reg 5: %i | "BTB_PATTERN"\n", data[0], BTB(data[0]));

reg_read(i2c, i2cAddr, CTRL_REG6, &data[0], 8);
printf("Reg 6: %i | "BTB_PATTERN"\n", data[0], BTB(data[0]));


    // Get i2c addr
    // Sett self-test bit
    {
        uint8_t value;
        reg_read(i2c, i2cAddr, CTRL_REG4, &value, 8);
        printf("%i |"BTB_PATTERN" \n", value, BTB(value));
        value %= 0xF9;
        value |= (1 << 2);
        reg_write(i2c, i2cAddr, CTRL_REG4, &value, 8);
    }
    /*
    data[0] = 0;
    data[0] |= (1 << 2);
    reg_write(i2c, i2cAddr, CTRL_REG4, &data[0], 1);
    */
