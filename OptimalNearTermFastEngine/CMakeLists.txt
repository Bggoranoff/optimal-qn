cmake_minimum_required(VERSION 3.10)
cmake_policy(SET CMP0074 NEW)

project(OptimalNearTerm C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED True)

file(GLOB_RECURSE SRC_FILES src/*.c)

message("Source files collected: ${SRC_FILES}")

add_executable(OptimalNearTerm ${SRC_FILES})

target_include_directories(OptimalNearTerm PRIVATE src)

