#include <sys/cdefs.h>
#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/i2c.h"

#include "led.h"
#include "accelerometer.h"
#include "data.h"
#include "usbTransfer.h"

i2c_inst_t *i2c;

#pragma clang diagnostic push
#pragma ide diagnostic ignored "EndlessLoop"

int main(void) {
    // Init USB stuff
    usbInit();

    // Init serial
    stdio_init_all();

    // Init I2C port
    i2c = i2c1;
    i2c_init(i2c, 400 * 1000);

    initAccel(i2c);

    // Wait before taking measurements
    sleep_ms(2000);

    // waitForStartSignal();

    while(1) {
        struct Data accelData = {
                time_us_32(),
                readData(i2c, OUT_X_L),
                readData(i2c, OUT_Y_L),
                readData(i2c, OUT_Z_L)
        };

        sendData(&accelData, 1);

        sleep_ms(500);
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
    regWrite(i2c, i2cAddr, CTRL_REG4, &data[0], 1);
    */
