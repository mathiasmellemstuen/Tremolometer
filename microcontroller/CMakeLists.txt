cmake_minimum_required(VERSION 3.13)

include(pico-sdk/pico_sdk_init.cmake)
project(tremolometer)

pico_sdk_init()

add_executable(tremolometer main.c)

target_link_libraries(tremolometer pico_stdlib)

pico_add_extra_outputs(tremolometer)