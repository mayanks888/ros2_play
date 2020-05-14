#include<memory>

#include<rclcpp/rclcpp.hpp>

#include "cpp_pubsub/Reviser.hpp"

auto main(int argc, char* argv[]) -> int{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<Reviser>());
    rclcpp::shutdown();
    return 0;
}
