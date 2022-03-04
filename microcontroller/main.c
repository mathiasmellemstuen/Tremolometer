#include <stdio.h>
#include <malloc.h>
#include "pico/stdlib.h"
#include "pico/malloc.h"

#define BUFFER_SIZE 20

typedef struct Data Data;
// Total 10 bytes
struct Data {
    uint32_t time;
    int16_t x, y, z;
};

static inline void sendData(Data* data) {

    unsigned char bytes[10];

    bytes[0] = (data->time << 2 >> 24) & 0xFF;
    bytes[1] = (data->time << 2 >> 16) & 0xFF;
    bytes[2] = (data->time << 2 >> 8)  & 0xFF;
    bytes[3] = data->time & 0xFF;
    bytes[4] = (data->x >> 8) & 0xFF;
    bytes[5] = data->x & 0xFF;
    bytes[6] = (data->y >> 8) & 0xFF;
    bytes[7] = data->y & 0xFF;
    bytes[8] = (data->z >> 8) & 0xFF;
    bytes[9] = data->z & 0xFF;

    printf("%x%x%x%x%x%x%x%x%x%x", bytes[0], bytes[1], bytes[2], bytes[3], bytes[4], bytes[5], bytes[6], bytes[7], bytes[8], bytes[9]);
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
    ledOn();

    struct Data* buffer = malloc(sizeof(Data) * BUFFER_SIZE);
    for(int i = 0; i < BUFFER_SIZE; i++) {
        buffer[i] = (Data) {1, 2, 3, 4};
    }

    waitForStartSignal();

    ledOff();
    for(int i = 0; i < BUFFER_SIZE; i++) {
        sleep_ms(100);
        sendData(buffer + i);
    }

    sleep_ms(1000);

    return 0;
}