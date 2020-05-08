#include<memory>

#include<rclcpp/rclcpp.hpp>

#include "cpp_pubsub/tl_processor.hpp"

auto main(int argc, char* argv[]) -> int{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<Processor>());
    rclcpp::shutdown();
    return 0;
}
