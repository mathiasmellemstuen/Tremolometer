#include <stdio.h>
#include "pico/stdlib.h"

void createRunningLight() {
    gpio_init(PICO_DEFAULT_LED_PIN);
    gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);
    gpio_put(PICO_DEFAULT_LED_PIN, 1);
}
int main(void) {

    stdio_init_all();

    createRunningLight();

    while (1) {
        printf("Dette er fra pico...");
        sleep_ms(1000);
    }
    return 0;
}
