#include <stdio.h>
#include <malloc.h>
#include "pico/stdlib.h"
#include "pico/malloc.h"

#define BUFFER_SIZE 5

// Total 10 bytes
struct Data {
    uint32_t time;
    int16_t x, y, z;
};

static inline void sendData(struct Data* data, int n) {

    fwrite(data,sizeof(struct Data), n, stdout);
    //fflush(stdout);
}

void ledOn() {
    gpio_init(PICO_DEFAULT_LED_PIN);
    gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);
    gpio_put(PICO_DEFAULT_LED_PIN, 1);
}

void ledOff() {
    gpio_put(PICO_DEFAULT_LED_PIN, 0);
}

void waitForStartSignal() {
    while(getchar_timeout_us(10) != '1') {
        stdio_init_all();
        sleep_ms(100);
    }
}

int main(void) {
    stdio_init_all();
    stdio_flush();
    setbuf(stdout, NULL);
    ledOn();

    struct Data* buffer = malloc(sizeof(struct Data) * BUFFER_SIZE);
    buffer[0] = (struct Data){10, 10, 10, 10};
    buffer[1] = (struct Data){5, 6, 7, 8};
    buffer[2] = (struct Data){9, 10, 11, 12};
    buffer[3] = (struct Data){13, 14, 15, 16};
    buffer[4] = (struct Data){17, 18, 19, 20};
    //waitForStartSignal();

    while(1) {
        ledOff();
        sleep_ms(500);
        sendData(buffer, BUFFER_SIZE);
        ledOn();
        sleep_ms(500);
    }

    return 0;
}