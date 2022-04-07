#include "time.h"
#include "pico/time.h"

/**
 * @brief Set startTime to time since boot
 * Set startTime to current time since boot.
 */
void timeInit() {
    startTime = to_ms_since_boot(get_absolute_time());
}

/**
 * @brief Calc time since timeInit().
 * Calculates the time since timeInit() was called.
 *
 * @return Time since timeInit() in ms.
 */
uint32_t timeSinceStart() {
    return to_ms_since_boot(get_absolute_time()) - startTime;
}