#include "usbTransfer.h"
#include "base64Encode.h"
#include <stdio.h>
#include <malloc.h>
#include <stdlib.h>
#include "led.h"

void usbInit() {
    stdio_init_all();
    stdio_flush();
}

void sendData(struct Data* data, int n) {
    // Splitting the data object into array of bytes
    unsigned char bytes[DATA_STRUCT_SIZE * n];

    // Move all data from buffer to the char array
    for (int i = 0; i < n; i++) {
        bytes[0 + (DATA_STRUCT_SIZE * i)] = data[i].time >> 24;
        bytes[1 + (DATA_STRUCT_SIZE * i)] = data[i].time >> 16;
        bytes[2 + (DATA_STRUCT_SIZE * i)] = data[i].time >> 8;
        bytes[3 + (DATA_STRUCT_SIZE * i)] = data[i].time;
        bytes[4 + (DATA_STRUCT_SIZE * i)] = data[i].x >> 8;
        bytes[5 + (DATA_STRUCT_SIZE * i)] = data[i].x;
        bytes[6 + (DATA_STRUCT_SIZE * i)] = data[i].y >> 8;
        bytes[7 + (DATA_STRUCT_SIZE * i)] = data[i].y;
        bytes[8 + (DATA_STRUCT_SIZE * i)] = data[i].z >> 8;
        bytes[9 + (DATA_STRUCT_SIZE * i)] = data[i].z;
    }

    // Base 64 encoding
    size_t resultLength = 0;
    char* result = encode(bytes, DATA_STRUCT_SIZE * n, &resultLength);

    //Writing encoded data to stdout
    fwrite(result, sizeof(char), resultLength, stdout);
    fflush(stdout);

    // De-allocating resources created by the encode function
    free(result);
}

int16_t waitForStartSignal() {

    while(true) {
        stdio_init_all();
        char character = getchar();

        if(character == 'S') { // Start signal
            break;

        } else if(character == 'E') { // Exit signal
            ledRGBSet(true, true, true);
            waitForHandshake();
            waitForStartSignal();
            return 0;
        }
    }

    return 0;
}

void waitForHandshake() {

    while(true) {
        stdio_init_all();
        char character = getchar();

        if(character == 'T') {
            break;
        }
    }

    printf("T");
    fflush(stdout);
}