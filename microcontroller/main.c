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