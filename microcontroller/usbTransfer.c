//
// Created by Mathias on 16.03.2022.
//

#include "usbTransfer.h"
#include "base64Encode.h"
#include <stdio.h>

void usbInit() {
    stdio_init_all();
    stdio_flush();
}

void sendData(struct Data* data, int n) {

    // Splitting the data object into array of bytes
    unsigned char bytes[DATA_STRUCT_SIZE * n];

    for(int i = 0; i < n; i++) {
        bytes[0 + (DATA_STRUCT_SIZE * i)] = data->time >> 24;
        bytes[1 + (DATA_STRUCT_SIZE * i)] = data->time >> 16;
        bytes[2 + (DATA_STRUCT_SIZE * i)] = data->time >> 8;
        bytes[3 + (DATA_STRUCT_SIZE * i)] = data->time;
        bytes[4 + (DATA_STRUCT_SIZE * i)] = data->x >> 8;
        bytes[5 + (DATA_STRUCT_SIZE * i)] = data->x;
        bytes[6 + (DATA_STRUCT_SIZE * i)] = data->y >> 8;
        bytes[7 + (DATA_STRUCT_SIZE * i)] = data->y;
        bytes[8 + (DATA_STRUCT_SIZE * i)] = data->z >> 8;
        bytes[9 + (DATA_STRUCT_SIZE * i)] = data->z;
    }

    // Base 64 encoding
    size_t resultLength = 0;
    char* result = encode(bytes, DATA_STRUCT_SIZE * n, &resultLength);

    //Writing encoded data to stdout
    fwrite(result, sizeof(char), resultLength, stdout);
    fflush(stdout);
}

void waitForStartSignal() {
    while(getchar_timeout_us(0) != '1') {
        stdio_init_all();
        sleep_ms(WAIT_FOR_START_SIGNAL_INTERVAL_TIME_MS);
    }
}
