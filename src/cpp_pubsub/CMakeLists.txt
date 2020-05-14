cmake_minimum_required(VERSION 3.5)
project(cpp_pubsub)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

include_directories(include)

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)


find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(traffic_light_msgs REQUIRED)
find_package(OpenCV REQUIRED)
find_package(cv_bridge REQUIRED)


add_executable(talker src/publisher_member_function.cpp)
ament_target_dependencies(talker rclcpp std_msgs)

add_executable(listener src/subscriber_member_function.cpp)
ament_target_dependencies(listener rclcpp std_msgs)

add_executable(mayrun src/mayank.cpp)
ament_target_dependencies(mayrun  traffic_light_msgs rclcpp std_msgs)

add_executable(snow_prs src/snow_process.cpp)
ament_target_dependencies(snow_prs  traffic_light_msgs rclcpp std_msgs OpenCV)

add_executable(processor src/tl_processor.cpp src/main.cpp include/hm/hungarian_bigraph_matcher.cc)
ament_target_dependencies(processor traffic_light_msgs rclcpp std_msgs OpenCV cv_bridge)


add_executable(reviser src/reviser.cpp src/main_reviser.cpp )
ament_target_dependencies(reviser traffic_light_msgs rclcpp std_msgs OpenCV cv_bridge)

  # install the launch directory
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}/
)

install(TARGETS
  talker
  listener
  mayrun
  snow_prs
  processor
  reviser
  DESTINATION lib/${PROJECT_NAME})

  #install(DIRECTORY include/
  #DESTINATION include)

ament_package()

