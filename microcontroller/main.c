#include <stdio.h>
#include "pico/stdlib.h"
#include "bsp/board.h"
#include "tusb.h"

int main() {

    board_init();
    tusb_init();

    return 0;
}