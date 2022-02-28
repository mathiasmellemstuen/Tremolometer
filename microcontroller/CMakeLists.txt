cmake_minimum_required(VERSION 3.13)

include(pico-sdk/pico_sdk_init.cmake)

project(tremolometer)

pico_sdk_init()

add_executable(tremolometer main.c tusb_config.h)

target_include_directories(tremolometer PUBLIC ${CMAKE_CURRENT_LIST_DIR})

target_link_libraries(tremolometer pico_stdlib tinyusb_host tinyusb_board)

pico_add_extra_outputs(tremolometer)