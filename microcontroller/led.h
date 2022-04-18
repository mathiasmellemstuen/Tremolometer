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
void ledInit();

/**
 * @brief Sett the LED on or off
 * Setts the rapsberry PI Pico LED on or off
 *
 * @param on LED is on
 */
void setLed(bool on);

/**
 * @brief Initiate RGB LED
 * Initiate RGB LED on Tiny 2040
 */
void ledRGBInit();

/**
 * @brief Toggle RGB LED
 * Sett the Red, Green or Blue LED on or off
 *
 * @param rOn Red LED on
 * @param gOn Green LED on
 * @param bOn Blue LED on
 */
void ledRGBSet(bool rOn, bool gOn, bool bOn);
#endif //TREMOLOMETER_LED_H
