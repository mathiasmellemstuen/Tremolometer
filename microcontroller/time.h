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
void timeInit();

/**
 * @brief Calc time since timeInit().
 * Calculates the time since timeInit() was called.
 *
 * @return Time since timeInit() in ms.
 */
uint32_t timeSinceStart();

#endif //TREMOLOMETER_TIME_H
