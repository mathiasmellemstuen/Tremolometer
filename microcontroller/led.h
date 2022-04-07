/// @file led.h
#ifndef TREMOLOMETER_LED_H
#define TREMOLOMETER_LED_H

#include <stdbool.h>
#include "pico/stdlib.h"

static const int LED_R = 18;    //!< Pin for Red LED.
static const int LED_G = 19;    //!< Pin for Green LED.
static const int LED_B = 20;    //!< Pin for Blue LED.

void ledInit();
void setLed(bool on);

void ledRGBInit();

void ledRGBSet(bool rOn, bool gOn, bool bOn);
#endif //TREMOLOMETER_LED_H
