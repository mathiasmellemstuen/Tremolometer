//
// Created by Mathias on 16.03.2022.
//

#include "usbTransfer.h"
#include "base64Encode.h"
#include <stdio.h>
#include <malloc.h>

void usbInit() {
    stdio_init_all();
    stdio_flush();
}

void sendData(struct Data* data, int n) {

    // Splitting the data object into array of bytes
    unsigned char bytes[DATA_STRUCT_SIZE * n];

    for(int i = 0; i < n; i++) {

        bytes[0 + (DATA_STRUCT_SIZE * i)] = data[i].time >> 24;
        bytes[1 + (DATA_STRUCT_SIZE * i)] = data[i].time >> 16;
        bytes[2 + (DATA_STRUCT_SIZE * i)] = data[i].time  >> 8;
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

int waitForStartSignal() {
    int inn;
    // Wait for a message from GUI
    for (inn = -1; inn == PICO_ERROR_TIMEOUT; inn = getchar_timeout_us(0)) {}

    for (int next = 0; next != PICO_ERROR_TIMEOUT; next = getchar_timeout_us(0)) {
        inn *= 10;
        inn += next;
    }

    return inn;
}