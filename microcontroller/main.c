#include <malloc.h>
#include "pico/stdlib.h"
#include <math.h>
#include "data.h"
#include "usbTransfer.h"
#include "led.h"

#define BUFFER_SIZE 1

int main(void) {

    usbInit();
    ledInit();
    setLed(true);
    waitForStartSignal();

    struct Data* buffer = malloc(sizeof(struct Data) * BUFFER_SIZE);
    buffer[0] = (struct Data){0, 1, 2, 3};

    while(1) {
        setLed(false);
        sleep_ms(500);

        buffer[0].time = buffer[0].time + 1;
        buffer[0].x = 100 * sin((double)buffer[0].time);
        buffer[0].y = 100 * cos((double)buffer[0].time);

        sendData(buffer, BUFFER_SIZE);

        setLed(true);
        sleep_ms(500);
    }

    return 0;
}