/// @file data.h
/// @brief Definition of the data struct.
#ifndef TREMOLOMETER_DATA_H
#define TREMOLOMETER_DATA_H

#include "pico/stdlib.h"

#define DATA_STRUCT_SIZE 10 //!< Size of the data struct in bytes.

/**
 * @brief Store the time and data of a single measurement.
 * Stores the time of a x,y,z accelerometer measurement.
 */
struct Data {
    uint32_t time;
    int16_t x, y, z;
};

/**
 * @brief Calculate the length of the data when it converting to base64.
 * Calculate the amount of bites are going to be send when converting data buffer to base64.
 *
 * @see base64Encode.c
 *
 * @param inputLen The length of the data buffer.
 * @return Number of bites it takes to send data.
 */
static inline int calcOutputLen(int inputLen) {
    return 4 * ((inputLen + 2) / 3);
}

#endif //TREMOLOMETER_DATA_H
