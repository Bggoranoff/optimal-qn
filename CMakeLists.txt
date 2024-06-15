cmake_minimum_required(VERSION 3.10)

project(OptimalNearTerm)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED True)

file(GLOB_RECURSE SRC_FILES "src/*.c")

add_executable(OptimalNearTerm ${SRC_FILES})

target_include_directories(OptimalNearTerm PRIVATE src)

