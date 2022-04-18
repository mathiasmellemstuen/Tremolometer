/// @file base64Encode.h
/// @brief Encode data buffer to base64.
#ifndef TREMOLOMETER_BASE64ENCODE_H
#define TREMOLOMETER_BASE64ENCODE_H

#include "pico/stdlib.h"

/**
 * TODO
 */
static const char encodingArray[] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/'};

/**
 * TODO
 */
static const int modArray[] = {0, 2, 1};

char* encode(const unsigned char* data, size_t inputLength, size_t* outputLength);

#endif //TREMOLOMETER_BASE64ENCODE_H
