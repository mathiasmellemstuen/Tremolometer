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

static inline int calcOutputLen(int inputLen) {
    return 4 * ((inputLen + 2) / 3);
}

#endif //TREMOLOMETER_DATA_H
