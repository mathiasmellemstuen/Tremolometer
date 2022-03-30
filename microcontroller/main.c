#include <sys/cdefs.h>
#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/i2c.h"

#include "led.h"
#include "accelerometer.h"
#include "data.h"
#include "usbTransfer.h"
#include "time.h"
#include <malloc.h>

i2c_inst_t *i2c;

#define BUFFER_SIZE 100
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

    struct Data* dataBuffer = malloc(sizeof(struct Data) * BUFFER_SIZE);

    // Wait before taking measurements
    // sleep_ms(5000);
    int16_t maxRunningTime = waitForStartSignal();

    ledRGBSet(1,0,1);

    gpio_put(18, 1);

    timeInit();

    uint16_t allocationIndex = 0;

    while(1) {
        uint32_t currentTime = timeSinceStart();

        // Restarts the algorithm if the time has exceeded maxRunningTime
        if(maxRunningTime < currentTime) {

            maxRunningTime = waitForStartSignal();
            timeInit();
            continue;
        }

        ledRGBSet(1, 0, 1);

        dataBuffer[allocationIndex].time = currentTime;
        dataBuffer[allocationIndex].x = readData(i2c, OUT_X_L);
        dataBuffer[allocationIndex].y = readData(i2c, OUT_Y_L);
        dataBuffer[allocationIndex].z = readData(i2c, OUT_Z_L);
        allocationIndex++;

        ledRGBSet(1, 1, 0);

        if(allocationIndex >= BUFFER_SIZE) {
            sendData(dataBuffer, BUFFER_SIZE);
            allocationIndex = 0;
        }

        sleep_ms(50);
    }

    return 0;
}