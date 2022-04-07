//
// Created by Mathias on 31/03/2022.
//

#ifndef TREMOLOMETER_TREMOLOMETERSTATE_H
#define TREMOLOMETER_TREMOLOMETERSTATE_H

/**
 * Enum for defining the state the current data buffer in in.
 */
enum TremolometerState {
        IDLE=1,
        BUFFER_FILLING=2,
        BUFFER_FULL=3
};
#endif //TREMOLOMETER_TREMOLOMETERSTATE_H
