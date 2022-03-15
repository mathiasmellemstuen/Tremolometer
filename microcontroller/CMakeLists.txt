ake_minimum_required(VERSION 3.13)

include(pico-sdk/pico_sdk_init.cmake)
project(tremolometer)

pico_sdk_init()

add_executable(tremolometer main.c)

target_include_directories(tremolometer PUBLIC ${CMAKE_CURRENT_LIST_DIR})

target_link_libraries(tremolometer pico_stdlib)

pico_enable_stdio_usb(tremolometer 1)
pico_enable_stdio_uart(tremolometer 0)

pico_add_extra_outputs(tremolometer)