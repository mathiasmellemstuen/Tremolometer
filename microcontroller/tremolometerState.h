/// @file tremolometerState.h
/// @brief Define the state of the Tremolometer
#ifndef TREMOLOMETER_TREMOLOMETERSTATE_H
#define TREMOLOMETER_TREMOLOMETERSTATE_H

/**
 * Enum for defining the state the current data buffer in in.
 */
enum TremolometerState {
        IDLE=1,             //!< The microcontroller is waiting to start
        BUFFER_FILLING=2,   //!< The microcontroller is filling the data buffer
        BUFFER_FULL=3       //!< The microcontroller has a full data buffer
};
#endif //TREMOLOMETER_TREMOLOMETERSTATE_H
