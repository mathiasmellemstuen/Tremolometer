//
// Created by Mathias on 21/03/2022.
//

#ifndef TREMOLOMETER_TIME_H
#define TREMOLOMETER_TIME_H

#include "pico.h"

static uint32_t startTime;

void timeInit();
uint32_t timeSinceStart();

#endif //TREMOLOMETER_TIME_H
