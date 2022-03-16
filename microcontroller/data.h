//
// Created by Mathias on 16.03.2022.
//

#ifndef TREMOLOMETER_DATA_H
#define TREMOLOMETER_DATA_H

#include "pico/stdlib.h"

// Total 10 bytes in Data struct
#define DATA_STRUCT_SIZE 10

struct Data {
    uint32_t time;
    int16_t x, y, z;
};

#endif //TREMOLOMETER_DATA_H
