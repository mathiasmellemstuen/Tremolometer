#include "pico/stdlib.h"
#include "hardware/i2c.h"
#include "hardware/sync.h"
#include "pico/multicore.h"
#include "led.h"
#include "accelerometer.h"
#include "data.h"
#include "usbTransfer.h"
#include "time.h"
#include "tremolometerState.h"
#include <malloc.h>

#pragma clang diagnostic push
#pragma ide diagnostic ignored "EndlessLoop"

#define BUFFER_SIZE 100
#define LOCK_DATA 24
#define LOCK_SEND 25
i2c_inst_t* i2c;

struct Data data0[BUFFER_SIZE];
struct Data data1[BUFFER_SIZE];

struct Data* dataP;
struct Data* dataS;
uint8_t dataSize, bufferInUse;
uint8_t *i;

bool wait, waitData;

void main2() {
    uint8_t size = 0;

    printf("Core 2: init\n");
    while (1) {

        // Wait for buffer to fill
        if (dataSize <= 90)
            continue;

        printf("Core 2: Start\n");

        wait = true;
        // Calc new buffer
        bufferInUse = (bufferInUse + 1) % 2;
        size = dataSize;
        dataSize = 0;

        if (bufferInUse == 0)
            dataP = data0;
        else if (bufferInUse == 1)
            dataP = data1;
        i = 0;
        wait = false;

        if (bufferInUse == 0)
            dataS = data1;
        else if (bufferInUse == 1)
            dataS = data0;

        sendData(dataS, size);
        size = 0;

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

    dataP = data0;
    bufferInUse = 0;
    wait = false;

    sleep_ms(5000);
    printf("Core 1: init\n");

    multicore_launch_core1(main2);

    timeInit();
    while (1) {
        if (wait) {
            printf("Core 1: wait\n");
            continue;
        }

        dataP[*i].time = timeSinceStart();
        dataP[*i].x = readData(i2c, OUT_X_L);
        dataP[*i].y = readData(i2c, OUT_Y_L);
        dataP[*i].z = readData(i2c, OUT_Z_L);

        dataSize++;
        i++;

        printf("core 1: %i\n", dataSize);

        sleep_ms(50);
    }

    return 0;
}