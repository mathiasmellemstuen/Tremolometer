/// @file usbTransfer.h
/// @brief Handle USB transfer
#ifndef TREMOLOMETER_USBTRANSFER_H
#define TREMOLOMETER_USBTRANSFER_H

#include "data.h"

/**
 * @brief Init USB things.
 * Initialize all things to do with the USB communication.
 */
static inline void usbInit() {
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
void sendData(struct Data* data, int n);

/**
 * @brief Wait for a start signal to be sent with measurement time.
 * Wait until the start time is sent over STDIN. The data that is read is measurement time in sec.
 *
 * @return Measurement time in sec.
 */
int16_t waitForStartSignal();

/**
 * @brief Wait for handshake with GUI.
 * Waits until byte 1 is received on STDIN. Then continues.
 */
void waitForHandshake();

#endif //TREMOLOMETER_USBTRANSFER_H
