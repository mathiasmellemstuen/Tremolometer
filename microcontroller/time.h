/// @file time.h
#ifndef TREMOLOMETER_TIME_H
#define TREMOLOMETER_TIME_H

#include "pico.h"
#include "pico/time.h"

static uint32_t startTime; //!< Store the time timeInit() was called.

void timeInit();
uint32_t timeSinceStart();

#endif //TREMOLOMETER_TIME_H
