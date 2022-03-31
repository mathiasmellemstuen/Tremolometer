cmake_minimum_required(VERSION 3.13)

include(pico-sdk/pico_sdk_init.cmake)
project(tremolometer)

pico_sdk_init()

add_executable(tremolometer time.h time.c base64Encode.h base64Encode.c data.h usbTransfer.h usbTransfer.c led.c led.h accelerometer.c accelerometer.h main.c)

target_include_directories(tremolometer PUBLIC ${CMAKE_CURRENT_LIST_DIR})

target_link_libraries(tremolometer pico_stdlib hardware_i2c pico_multicore)

pico_enable_stdio_usb(tremolometer 1)
pico_enable_stdio_uart(tremolometer 0)

pico_add_extra_outputs(tremolometer)