#include <stdio.h>

#include "pico/stdlib.h"
#include "pico/multicore.h"
#include "hardware/i2c.h"

#include "led.h"
#include "accelerometer.h"
#include "data.h"
#include "usbTransfer.h"
#include "time.h"

#define BUFFER_SIZE 100

// Define i2c instance
i2c_inst_t* i2c;

// Define data buffer 1 and 2
struct Data data0[BUFFER_SIZE];
struct Data data1[BUFFER_SIZE];

// Define pointer to data buffers
struct Data* sensorData;
struct Data* sendingData;

uint8_t bufferInUse, bufferIndex;

void main2() {
    while (1) {
        // Wait for signal to start sending the data.
        multicore_fifo_pop_blocking();

        ledRGBSet(0,1,1);

        // Calc new buffer
        bufferInUse = (bufferInUse + 1) % 2;

        // Sett the new buffer
        if (bufferInUse == 0)
            sensorData = data0;
        else if (bufferInUse == 1)
            sensorData = data1;

        // Send signal for measurements to resume
        multicore_fifo_push_blocking(0);

        // Change the sending buffer
        if (bufferInUse == 0)
            sendingData = data1;
        else if (bufferInUse == 1)
            sendingData = data0;

        // Send the data from buffer
        sendData(sendingData, BUFFER_SIZE);
        ledRGBSet(0,1,0);
    }
}

int main(void) {
    // Init stuff
    usbInit();
    stdio_init_all();
    ledRGBInit();

    i2c = i2c1;
    i2c_init(i2c, 400 * 1000);
    initAccel(i2c);

    sensorData = data0;
    bufferInUse = 0;

    multicore_launch_core1(main2);

    waitForHandshake();

    while (1) {
        // Wait for start signal and get the measurement time.
        uint16_t runningTime = waitForStartSignal();
        ledRGBSet(0,1,0);

        // Start timing
        timeInit();
        uint32_t endTime = runningTime + timeSinceStart();

        ledRGBSet(0,0,1);
        // Do all measurements
        for (uint32_t time = timeSinceStart(); time <= endTime; time = timeSinceStart()) {
            // Add the data to the current buffer
            sensorData[bufferIndex].time = time;
            sensorData[bufferIndex].x = readData(i2c, OUT_X_L);
            sensorData[bufferIndex].y = readData(i2c, OUT_Y_L);
            sensorData[bufferIndex].z = readData(i2c, OUT_Z_L);

            // If the buffer is full, initiate sending the data
            if (++bufferIndex == BUFFER_SIZE) {
                // Send signal to core1 that it should start sending data
                multicore_fifo_push_blocking(0);
                // Wait for core1 to indicate that measurement can start
                multicore_fifo_pop_blocking();
                // Reset buffer index
                bufferIndex = 0;
            }

            // Wait for next measurement
            sleep_ms(5);
        }
        // Send the remaining data
        sendData(sensorData, BUFFER_SIZE);
    }

    return 0;
}