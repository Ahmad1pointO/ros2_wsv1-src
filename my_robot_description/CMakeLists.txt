cmake_minimum_required(VERSION 3.8)
project(my_robot_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wdeprecated)
endif()

find_package(ament_cmake REQUIRED)

# Install the URDF directory into the share install path
install(
  DIRECTORY urdf launch config
  DESTINATION share/${PROJECT_NAME}


)

ament_package()
