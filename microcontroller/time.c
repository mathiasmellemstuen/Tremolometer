#include "time.h"
#include "pico/time.h"

void timeInit() {
    startTime = to_ms_since_boot(get_absolute_time());
}

uint32_t timeSinceStart() {
    return to_ms_since_boot(get_absolute_time()) - startTime;
}