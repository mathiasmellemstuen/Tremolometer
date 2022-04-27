/// @file time.h
/// @brief Functions involving time.
#ifndef TREMOLOMETER_TIME_H
#define TREMOLOMETER_TIME_H

#include "pico.h"
#include "pico/time.h"

static uint32_t startTime; //!< Store the time timeInit() was called.

/**
 * @brief Set startTime to time since boot
 * Set startTime to current time since boot.
 */
static inline void timeInit() {
    startTime = to_ms_since_boot(get_absolute_time());
}

/**
 * @brief Calc time since timeInit().
 * Calculates the time since timeInit() was called.
 *
 * @return Time since timeInit() in ms.
 */
static inline uint32_t timeSinceStart() {
    return to_ms_since_boot(get_absolute_time()) - startTime;
}

#endif //TREMOLOMETER_TIME_H
