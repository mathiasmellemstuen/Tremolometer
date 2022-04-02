#include "pico/stdlib.h"
#include "hardware/i2c.h"
#include "pico/multicore.h"
#include "led.h"
#include "accelerometer.h"
#include "data.h"
#include "usbTransfer.h"
#include "time.h"
#include <stdio.h>

#define BUFFER_SIZE 100
#define LOCK_DATA 24
#define LOCK_SEND 25
i2c_inst_t* i2c;

struct Data data0[BUFFER_SIZE];
struct Data data1[BUFFER_SIZE];

struct Data* sensorData;
struct Data* sendingData;
uint8_t bufferInUse;
uint8_t i;

bool waitData, fullBuffer;

void main2() {

    printf("Core 2: init\n");
    while (1) {

        multicore_fifo_pop_blocking();

        printf("Core 2: Start\n");

        // Calc new buffer
        bufferInUse = (bufferInUse + 1) % 2;

        if (bufferInUse == 0)
            sensorData = data0;
        else if (bufferInUse == 1)
            sensorData = data1;

        multicore_fifo_push_blocking(0);

        if (bufferInUse == 0)
            sendingData = data1;
        else if (bufferInUse == 1)
            sendingData = data0;

        sendData(sendingData, BUFFER_SIZE);


        printf("Core 2: end\n");
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
    fullBuffer = false;

    sleep_ms(5000);
    printf("Core 1: init\n");

    multicore_launch_core1(main2);

    timeInit();

    while (1) {

        sensorData[i].time = timeSinceStart();
        sensorData[i].x = readData(i2c, OUT_X_L);
        sensorData[i].y = readData(i2c, OUT_Y_L);
        sensorData[i].z = readData(i2c, OUT_Z_L);


        printf("core 1: %i\n", i);
        i++;

        if(i == BUFFER_SIZE) {
            multicore_fifo_push_blocking(0);
            multicore_fifo_pop_blocking();
            i = 0;
        }


        sleep_ms(50);
    }

    return 0;
}