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