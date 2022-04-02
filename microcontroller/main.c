#include "pico/stdlib.h"
#include "hardware/i2c.h"
#include "pico/multicore.h"
#include "led.h"
#include "accelerometer.h"
#include "data.h"
#include "usbTransfer.h"
#include "time.h"
#include "tremolometerState.h"
#include <malloc.h>

#define BUFFER_SIZE 100
#define SWAP_AMOUNTS 2
#define SAMPLING_TIME_MS 50

struct Data* allocateBuffer() {
    return malloc(sizeof(struct Data) * BUFFER_SIZE);
}

void sampling(i2c_inst_t* i2c, struct Data* dataBuffer, struct Data* anotherDataBuffer, uint32_t* totalMeasureTimeMs, enum TremolometerState* state) {
    ledRGBSet(true, false, false);

    // Waiting until the tremolometer state is not IDLE
    while(*state == IDLE) {}

    uint16_t allocationIndex = 0;

    timeInit();

    ledRGBSet(false, false, true);

    for (uint32_t time = timeSinceStart(); time <= *totalMeasureTimeMs; time = timeSinceStart()) {

        dataBuffer[allocationIndex].time = time;
        //dataBuffers[0][allocationIndex].x = readData(i2c, OUT_X_L);
        //dataBuffers[0][allocationIndex].y = readData(i2c, OUT_Y_L);
        //dataBuffers[0][allocationIndex].z = readData(i2c, OUT_Z_L);
        dataBuffer[allocationIndex].x = 1;
        dataBuffer[allocationIndex].y = 2;
        dataBuffer[allocationIndex].z = 3;
        allocationIndex++;

        if(allocationIndex >= BUFFER_SIZE) {

            // Swapping the buffers
            struct Data* temp = dataBuffer;
            dataBuffer = anotherDataBuffer;
            anotherDataBuffer = temp;

            //Signaling that the buffer is full so the program sends it to USB
            *state = BUFFER_FULL;
            allocationIndex = 0;
        }

        sleep_ms(SAMPLING_TIME_MS);
    }

    sampling(i2c, dataBuffer, anotherDataBuffer, totalMeasureTimeMs, state);

}
void main2() {


    // Doing initial setup for i2c
    i2c_inst_t *i2c;
    i2c = i2c1;
    i2c_init(i2c, 400 * 1000);
    initAccel(i2c);

    // ALlocating the data buffer
    struct Data* dataBuffer = allocateBuffer();

    //Receiving the pointer from the other buffer from the main core
    struct Data* anotherDataBuffer = multicore_fifo_pop_blocking();

    uint32_t* totalMeasureTimeMs = multicore_fifo_pop_blocking();

    enum TremolometerState* state = multicore_fifo_pop_blocking();

    // Starting the sampling function that runs recursively
    sampling(i2c, dataBuffer, anotherDataBuffer, totalMeasureTimeMs, state);
}

int main(void) {


    // Start second core (core 1). Using this core for sampling from sensor
    multicore_launch_core1(main2);


    // Init USB
    usbInit();

    // Init serial
    stdio_init_all();

    //Initting led
    ledRGBInit();
    ledRGBSet(false, false, false);

    // Allocating memory for the buffer
    struct Data* dataBuffer = allocateBuffer();
    //Sending pointer to the allocated buffer over to the other cpu
    multicore_fifo_push_blocking(dataBuffer);

    uint32_t* totalMeasureTimeMs = malloc(sizeof(uint32_t));
    // Sending pointer to the total measure time over to the other core
    multicore_fifo_push_blocking(totalMeasureTimeMs);


    enum TremolometerState* state = malloc(sizeof(enum TremolometerState));
    *state = IDLE;
    // Sending pointer to the state over the the other core
    multicore_fifo_push_blocking(state);

    waitForHandshake();

    while(1) {

        //ledRGBSet(state == IDLE, state == BUFFER_FILLING, state == BUFFER_FULL);

        if(*state == IDLE) {

            // Waiting for a start signal when the tremolometer is in idle state
            *totalMeasureTimeMs = waitForStartSignal();


            // Changing the state to BUFFER_FILLING when we got the starting time
            *state = BUFFER_FILLING;
            ledRGBSet(false, true, true);
        }

        // Sending the buffer if it's full
        if(*state == BUFFER_FULL) {
            ledRGBSet(false, true, false);
            sendData(dataBuffer, BUFFER_SIZE);
            *state = BUFFER_FILLING;
        }
    }
}