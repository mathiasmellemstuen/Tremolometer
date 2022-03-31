#include <sys/cdefs.h>
#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/i2c.h"
#include "pico/multicore.h"

#include "led.h"
#include "accelerometer.h"
#include "data.h"
#include "usbTransfer.h"
#include "time.h"
#include <malloc.h>

i2c_inst_t *i2c;
struct Data accelData;

#pragma clang diagnostic push
#pragma ide diagnostic ignored "EndlessLoop"

void main2() {

}

#define BUFFER_SIZE 100
int main(void) {
    // Start second core (core 1)
    multicore_launch_core1(main2);

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
    int16_t ii = waitForStartSignal();

    ledRGBSet(1,0,1);

    gpio_put(18, 1);

    timeInit();
    endTime = (startTime - startTime) + ii;

    for (uint32_t time = timeSinceStart(); time <= endTime; time = timeSinceStart()) {
        ledRGBSet(1, 0, 1);
        accelData.time = to_ms_since_boot(get_absolute_time()) - startTime;
        // accelData.x = readData(i2c, OUT_X_L);
        accelData.x = ii;
        accelData.y = readData(i2c, OUT_Y_L);
        accelData.z = readData(i2c, OUT_Z_L);

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

    ledRGBSet(0, 1, 0);

    return 0;
}