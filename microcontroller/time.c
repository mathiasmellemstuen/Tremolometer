//
// Created by Mathias on 21/03/2022.
//

#include "time.h"
#include "pico/time.h"

/**
 * Set startTime to current time since boot.
 */
void timeInit() {
    startTime = to_ms_since_boot(get_absolute_time());
}

/**
 * Calculates the time since timeInit() was called.
 * @return Time since timeInit() in ms.
 */
uint32_t timeSinceStart() {
    return to_ms_since_boot(get_absolute_time()) - startTime;
}