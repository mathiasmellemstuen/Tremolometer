#include "usbTransfer.h"
#include "base64Encode.h"
#include <stdio.h>
#include <malloc.h>
#include <stdlib.h>

/**
 * @brief Init USB things.
 * Initialize all things to do with the USB communication.
 */
void usbInit() {
    stdio_init_all();
    stdio_flush();
}

/**
 * @brief Send a data buffer over STDOUT.
 * Send a data buffer over STDOUT. This formats the data in the buffer to base64, then sends that data.
 *
 * @param data Pointer to a data buffer.
 * @param n Number of measurements in the data buffer.
 */
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

/**
 * @brief Wait for a start signal to be sent with measurement time.
 * Wait until the start time is sent over STDIN. The data that is read is measurement time in sec.
 *
 * @return Measurement time in sec.
 */
int16_t waitForStartSignal() {
    int inn;
    // Wait for a message from GUI
    for (inn = -1; inn == PICO_ERROR_TIMEOUT; inn = getchar_timeout_us(0)) {}
    // Convert last input (from stdio) to an int
    inn -= 48;

    // Convert message form GUI to an int
    for (int next = getchar_timeout_us(0); next != PICO_ERROR_TIMEOUT; next = getchar_timeout_us(0)) {
        // Add next number to the inn var
        inn *= 10;
        inn += (next - 48);
    }

    // Return measuring time (in ms)
    return inn;
}

/**
 * @brief Wait for handshake with GUI.
 * Waits until byte 1 is received on STDIN. Then continues.
 */
void waitForHandshake() {
    char in = 0x00;

    while (in != '1') {
        stdio_init_all();
        in = getchar_timeout_us(200 * 1000);
    }

    printf("2");
    fflush(stdout);
    fflush(stdin);
}