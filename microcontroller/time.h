//
// Created by Mathias on 21/03/2022.
//

#ifndef TREMOLOMETER_TIME_H
#define TREMOLOMETER_TIME_H

#include "pico.h"
#include "pico/time.h"

static uint32_t startTime;

void timeInit();

static inline uint32_t timeSinceStart() {
    return to_ms_since_boot(get_absolute_time()) - startTime;
}

#endif //TREMOLOMETER_TIME_H
