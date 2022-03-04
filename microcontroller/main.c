#pragma clang diagnostic push
#pragma ide diagnostic ignored "EndlessLoop"
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

static inline void printData(Data d) {
    printf("%c,%c,%c,%c\n", d.time, d.x, d.y, d.z);
}

void createRunningLight() {
    gpio_init(PICO_DEFAULT_LED_PIN);
    gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);
    gpio_put(PICO_DEFAULT_LED_PIN, 1);
}

int main(void) {
    stdio_init_all();
    createRunningLight();

    sleep_ms(6000);

    // printf("Allocate buffer\n");
    struct Data* buffer = malloc(sizeof(Data) * BUFFER_SIZE);

    // printf("Fill buffer\n");
    for(int i = 0; i < BUFFER_SIZE; i++) {
        buffer[i] = (Data) {4294967295, i+100, i+200, i+300};
    }
    sleep_ms(3000);

    // printf("Print buffer\n");
    for(int i = 0; i < BUFFER_SIZE; i++) {
        sleep_ms(100);
        printData(buffer[i]);
    }

    // printf("%s", (const char *) buffer);

    sleep_ms(1000);

    static char t = 68;
    static char d = 0;

    bool led = 0;

    for (;;t++, d++) {
        printf("Input\n");
        char ui = getchar();
        printf("char: %c\n", ui);

        if (led) led = 0;
        else led = 1;

        if (ui == 49)
            gpio_put(PICO_DEFAULT_LED_PIN, led);

        // sleep_ms(500);
    }
    return 0;
}

#pragma clang diagnostic pop