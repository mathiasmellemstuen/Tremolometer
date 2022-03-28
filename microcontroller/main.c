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

    ledRGBInit();
    ledRGBSet(0, 1, 1);

    struct Data accelData;

    // Wait before taking measurements
    waitForStartSignal();

    gpio_put(18, 1);

    while(1) {
        ledRGBSet(1, 0, 1);
        accelData.time = time_us_32();
        accelData.time = readData(i2c, OUT_X_L);
        accelData.time = readData(i2c, OUT_Y_L);
        accelData.time = readData(i2c, OUT_Z_L);

        ledRGBSet(1, 1, 0);
        sendData(&accelData, 1);

        sleep_ms(500);
    }

    return 0;
}
#pragma clang diagnostic pop