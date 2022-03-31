//
// Created by Mathias on 16.03.2022.
//

#include "led.h"
#include "pico/stdlib.h"

void ledInit() {
    gpio_init(PICO_DEFAULT_LED_PIN);
    gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);
}
void setLed(bool on) {
    gpio_put(PICO_DEFAULT_LED_PIN, on);
}

void ledRGBInit() {
    gpio_init(LED_R);
    gpio_set_dir(LED_R, GPIO_OUT);
    gpio_init(LED_G);
    gpio_set_dir(LED_G, GPIO_OUT);
    gpio_init(LED_B);
    gpio_set_dir(LED_B, GPIO_OUT);
}

void ledRGBSet(bool rOff, bool gOff, bool bOff) {
    gpio_put(LED_R, rOff);
    gpio_put(LED_G, gOff);
    gpio_put(LED_B, bOff);
}