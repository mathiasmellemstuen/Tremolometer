//
// Created by Mathias on 16.03.2022.
//

#include "led.h"
#include "pico/stdlib.h"

/**
 * @brief Initiate LED pins.
 * Initiates LED pins for rasberry PI Pico
 */
void ledInit() {
    gpio_init(PICO_DEFAULT_LED_PIN);
    gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);
}

/**
 * @brief Sett the LED on or off
 * Setts the rapsberry PI Pico LED on or off
 * @param on LED is on
 */
void setLed(bool on) {
    gpio_put(PICO_DEFAULT_LED_PIN, on);
}

/**
 * @brief Initiate RGB LED
 * Initiate RGB LED on Tiny 2040
 */
void ledRGBInit() {
    gpio_init(LED_R);
    gpio_set_dir(LED_R, GPIO_OUT);
    gpio_init(LED_G);
    gpio_set_dir(LED_G, GPIO_OUT);
    gpio_init(LED_B);
    gpio_set_dir(LED_B, GPIO_OUT);
}

/**
 * Sett the Red, Green or Blue LED on or off
 * @param rOn Red LED on
 * @param gOn Green LED on
 * @param bOn Blue LED on
 */
void ledRGBSet(bool rOn, bool gOn, bool bOn) {
    gpio_put(LED_R, !rOn);
    gpio_put(LED_G, !gOn);
    gpio_put(LED_B, !bOn);
}
