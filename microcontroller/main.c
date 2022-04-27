#include <stdio.h>

#include "pico/stdlib.h"
#include "pico/multicore.h"
#include "hardware/i2c.h"

#include "accelerometer.h"
#include "data.h"
#include "usbTransfer.h"
#include "time.h"

#define BUFFER_SIZE 64   //!< Define the buffer size to use.
#define WAIT_TIME 25     //!< Define how long between measurements (in ms).

i2c_inst_t* i2c;    //!< The i2c instance.

// Define data buffer 1 and 2
struct Data data0[BUFFER_SIZE]; //!< Array of Data structs to act as a buffer to store measurements.
struct Data data1[BUFFER_SIZE]; //!< Array of Data structs to act as a buffer to store measurements.

// Define pointer to data buffers
struct Data* sensorData;    //!< Pointer to the data buffer data is being stored to.
struct Data* sendingData;   //!< Pinter to the data buffer data is being sent from.

uint8_t bufferInUse;    //!< Indicate what buffer is being used to write measurements to.
uint8_t bufferIndex;    //!< Where in the buffer data is being stored to.

void main2() {

    multicore_fifo_drain();

    while (1) {
        // Wait for signal to start sending the data.
        multicore_fifo_pop_blocking();

        // Calc new buffer
        bufferInUse = (bufferInUse + 1) % 2;

        // Set the new buffer
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
    }
}

int main(void) {
    // Init stuff
    usbInit();
    stdio_init_all();

    i2c = i2c1;
    i2c_init(i2c, 400 * 1000);
    initAccel(i2c, NO_SELF_TEST);

    sensorData = data0;
    bufferInUse = 0;

    multicore_fifo_drain();
    multicore_launch_core1(main2);

    //waitForHandshake();

    while (1) {
        // Wait for start signal and get the measurement time.
        sleep_ms(1000);
        uint16_t runningTime = waitForStartSignal() * 1000;
        // runningTime = 20000;
        // Start timing
        timeInit();
        uint32_t endTime = runningTime + timeSinceStart();
        uint32_t lastTime = 0;

        // Do all measurements
        for (uint32_t time = timeSinceStart(); time <= endTime + 1000; time = timeSinceStart()) {
            // Wait for WAIT_TIME ms before taking next measurement
            if ((time - lastTime) < WAIT_TIME)
                continue;

            lastTime = timeSinceStart();
            // Add the data to the current buffer
            sensorData[bufferIndex].time = time;
            sensorData[bufferIndex].x = readData(i2c, OUT_X_L);
            sensorData[bufferIndex].y = readData(i2c, OUT_Y_L);
            sensorData[bufferIndex].z = readData(i2c, OUT_Z_L);

            // If the buffer is full, initiate sending the data
            if (++bufferIndex == BUFFER_SIZE) {
                // Send signal to core1 that it should start sending data
                multicore_fifo_push_blocking(1);
                // Wait for core1 to indicate that measurement can start
                multicore_fifo_pop_blocking();
                // Reset buffer index
                bufferIndex = 0;
            }
        }
        // Send the remaining data
        sendData(sensorData, BUFFER_SIZE);
    }

    return 0;
}