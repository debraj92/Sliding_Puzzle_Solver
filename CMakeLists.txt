cmake_minimum_required(VERSION 3.19)
project(658_A1)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_BUILD_TYPE Release)
set(CMAKE_CXX_FLAGS_RELEASE "-O3")
add_executable(658_A1 main.cpp SlidingTileBoard.cpp SlidingTileBoard.h SlidingTilePuzzleIDA_Star.cpp SlidingTilePuzzleIDA_Star.h)
