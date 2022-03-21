#include <malloc.h>
#include "pico/stdlib.h"
#include <math.h>
#include "data.h"
#include "usbTransfer.h"
#include "led.h"
#include "time.h"

#define BUFFER_SIZE 100

int main(void) {

    usbInit();
    ledInit();

    setLed(true);
    waitForStartSignal();
    timeInit();
    setLed(false);

    struct Data* buffer = malloc(sizeof(struct Data) * BUFFER_SIZE);

    int i = 0;
    int j = 0;

    while(true) {

        buffer[i].time = timeSinceStart();
        buffer[i].x = 100 * sin((double)j/10.0f);
        buffer[i].y = 100 * cos((double)j/10.0f);
        buffer[i].z = 100 * cos(M_PI / 4 + (double)j/10.0f);

        sleep_ms(10);

        if(i == BUFFER_SIZE - 1) {
            sendData(buffer, BUFFER_SIZE);
            i = 0;
            continue;
        }
        i += 1;
        j += 1;
    }

    return 0;
}