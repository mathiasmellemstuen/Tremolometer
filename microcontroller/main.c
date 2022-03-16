#include <stdio.h>
#include <malloc.h>
#include "pico/stdlib.h"
#include "pico/malloc.h"
#include <string.h>
#include <math.h>

#define BUFFER_SIZE 1

// Total 10 bytes
struct Data {
    uint32_t time;
    int16_t x, y, z;
};
static char encoding_table[] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                                'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                                'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                                'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
                                'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                                'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                                'w', 'x', 'y', 'z', '0', '1', '2', '3',
                                '4', '5', '6', '7', '8', '9', '+', '/'};
static int mod_table[] = {0, 2, 1};

char* encode(const unsigned char* data, size_t input_length, size_t *output_length) {

    *output_length = 4 * ((input_length + 2) / 3);

    char *encoded_data = malloc(*output_length);

    for (int i = 0, j = 0; i < input_length;) {

        uint32_t octet_a = i < input_length ? (unsigned char)data[i++] : 0;
        uint32_t octet_b = i < input_length ? (unsigned char)data[i++] : 0;
        uint32_t octet_c = i < input_length ? (unsigned char)data[i++] : 0;

        uint32_t triple = (octet_a << 0x10) + (octet_b << 0x08) + octet_c;

        encoded_data[j++] = encoding_table[(triple >> 3 * 6) & 0x3F];
        encoded_data[j++] = encoding_table[(triple >> 2 * 6) & 0x3F];
        encoded_data[j++] = encoding_table[(triple >> 1 * 6) & 0x3F];
        encoded_data[j++] = encoding_table[(triple >> 0 * 6) & 0x3F];
    }

    for (int i = 0; i < mod_table[input_length % 3]; i++)
        encoded_data[*output_length - 1 - i] = '=';

    return encoded_data;
}

static void sendData(struct Data* data, int n) {

    // Splitting the data object into array of bytes
    unsigned char bytes[10];
    bytes[0] = data->time >> 24;
    bytes[1] = data->time >> 16;
    bytes[2] = data->time >> 8;
    bytes[3] = data->time;
    bytes[4] = data->x >> 8;
    bytes[5] = data->x;
    bytes[6] = data->y >> 8;
    bytes[7] = data->y;
    bytes[8] = data->z >> 8;
    bytes[9] = data->z;

    // Base 64 encoding
    size_t resultLength = 0;
    char* result = encode(bytes, 10, &resultLength);

    //Writing data to stdout
    fwrite(result, sizeof(char), resultLength, stdout);
    fflush(stdout);
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
    //setbuf(stdout, NULL);
    ledOn();

    struct Data* buffer = malloc(sizeof(struct Data) * BUFFER_SIZE);
    buffer[0] = (struct Data){0, 1, 2, 3};

    waitForStartSignal();

    while(1) {
        ledOff();
        sleep_ms(500);
        buffer[0].time = buffer[0].time + 1;
        buffer[0].x = 100 * sin((double)buffer[0].time);
        buffer[0].y = 100 * cos((double)buffer[0].time);
        sendData(buffer, BUFFER_SIZE);
        ledOn();
        sleep_ms(500);
    }

    return 0;
}