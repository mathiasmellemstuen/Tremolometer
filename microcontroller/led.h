//
// Created by Mathias on 16.03.2022.
//

#ifndef TREMOLOMETER_LED_H
#define TREMOLOMETER_LED_H

#include <stdbool.h>
#include "pico/stdlib.h"

static const int LED_R = 18;
static const int LED_G = 19;
static const int LED_B = 20;

void ledInit();
void setLed(bool on);

void ledRGBInit();

void ledRGBSet(bool rOn, bool gOn, bool bOn);
#endif //TREMOLOMETER_LED_H
