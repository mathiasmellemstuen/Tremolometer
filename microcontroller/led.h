/// @file led.h
/// @brief Functions to control the LED.
#ifndef TREMOLOMETER_LED_H
#define TREMOLOMETER_LED_H

#include <stdbool.h>
#include "pico/stdlib.h"

static const int LED_R = 18;    //!< Pin for Red LED.
static const int LED_G = 19;    //!< Pin for Green LED.
static const int LED_B = 20;    //!< Pin for Blue LED.

/**
 * @brief Initiate LED pins.
 * Initiates LED pins for rasberry PI Pico
 */
static inline void ledInit() {
    gpio_init(PICO_DEFAULT_LED_PIN);
    gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);
}

/**
 * @brief Sett the LED on or off
 * Setts the rapsberry PI Pico LED on or off
 *
 * @param on LED is on
 */
static inline void setLed(bool on) {
    gpio_put(PICO_DEFAULT_LED_PIN, on);
}

/**
 * @brief Initiate RGB LED
 * Initiate RGB LED on Tiny 2040
 */
static inline void ledRGBInit() {
    gpio_init(LED_R);
    gpio_set_dir(LED_R, GPIO_OUT);
    gpio_init(LED_G);
    gpio_set_dir(LED_G, GPIO_OUT);
    gpio_init(LED_B);
    gpio_set_dir(LED_B, GPIO_OUT);
}

/**
 * @brief Toggle RGB LED
 * Sett the Red, Green or Blue LED on or off
 *
 * @param rOn Red LED on
 * @param gOn Green LED on
 * @param bOn Blue LED on
 */
static inline void ledRGBSet(bool rOn, bool gOn, bool bOn) {
    gpio_put(LED_R, !rOn);
    gpio_put(LED_G, !gOn);
    gpio_put(LED_B, !bOn);
}

#endif //TREMOLOMETER_LED_H
