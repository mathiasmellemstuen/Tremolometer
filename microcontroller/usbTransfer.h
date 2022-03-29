//
// Created by Mathias on 16.03.2022.
//

#ifndef TREMOLOMETER_USBTRANSFER_H
#define TREMOLOMETER_USBTRANSFER_H

#include "data.h"

#define WAIT_FOR_START_SIGNAL_INTERVAL_TIME_MS 100

void usbInit();
void sendData(struct Data* data, int n);
int waitForStartSignal();

/* Procedure:
 * 1. Get measuring time (ms) form GUI
 * 2. Send package size to GUI
 */

#endif //TREMOLOMETER_USBTRANSFER_H
