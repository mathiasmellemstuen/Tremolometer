//
// Created by Mathias on 16.03.2022.
//

#ifndef TREMOLOMETER_USBTRANSFER_H
#define TREMOLOMETER_USBTRANSFER_H

#include "data.h"

void usbInit();
void sendData(struct Data* data, int n);
int16_t waitForStartSignal();
void waitForHandshake();

/* Procedure:
 * 1. Get measuring time (ms) form GUI
 * 2. Send package size to GUI
 */

#endif //TREMOLOMETER_USBTRANSFER_H
