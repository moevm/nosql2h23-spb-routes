PROJECT(myproject)
CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

SET(mylibSRCS difficult_func.cpp wrapper_func.cpp)

ADD_LIBRARY(Summator SHARED ${mylibSRCS})

TARGET_LINK_LIBRARIES(mylib)
