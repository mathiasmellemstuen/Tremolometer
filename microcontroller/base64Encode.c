//
// Created by Mathias on 16.03.2022.
//

#include "base64Encode.h"
#include <malloc.h>

char* encode(const unsigned char* data, size_t inputLength, size_t* outputLength) {

    *outputLength = 4 * ((inputLength + 2) / 3);

    char *encodedData = malloc(*outputLength);

    for (int i = 0, j = 0; i < inputLength;) {

        uint32_t octet_a = i < inputLength ? (unsigned char)data[i++] : 0;
        uint32_t octet_b = i < inputLength ? (unsigned char)data[i++] : 0;
        uint32_t octet_c = i < inputLength ? (unsigned char)data[i++] : 0;

        uint32_t triple = (octet_a << 0x10) + (octet_b << 0x08) + octet_c;

        encodedData[j++] = encodingArray[(triple >> 3 * 6) & 0x3F];
        encodedData[j++] = encodingArray[(triple >> 2 * 6) & 0x3F];
        encodedData[j++] = encodingArray[(triple >> 1 * 6) & 0x3F];
        encodedData[j++] = encodingArray[(triple >> 0 * 6) & 0x3F];
    }

    for (int i = 0; i < modArray[inputLength % 3]; i++)
        encodedData[*outputLength - 1 - i] = '=';

    return encodedData;
}
