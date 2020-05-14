// #ifndef CPP_PUBSUB__TLPROCESSOR_H
// #define CPP_PUBSUB__TLPROCESSOR_H

#include <bits/stdc++.h>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float32_multi_array.hpp"
#include "opencv2/opencv.hpp"
#include "traffic_light_msgs/msg/traffic_light_struct.hpp"
// #include "hm/hungarian_bigraph_matcher.h"
#include "image/image_lights.h"
#include "cv_bridge/cv_bridge.h"

using std::placeholders::_1;
#pragma once
// using Preprocessor::GetProjRoi;
// rclcpp (ROS Client Library for C++)
class Reviser : public rclcpp::Node
{
public:
Reviser();
    // explicit Processor(const rclcpp::NodeOptions &options)
    //     : Node("bbox", options)
    // {
    //     RCLCPP_INFO(this->get_logger(), "Starting %s.", this->get_name());
   

    //     auto callback = std::bind(&Processor::BBoxCallback, this, _1);

    //     bbox_sub_ = this->create_subscription<traffic_light_msgs::msg::TrafficLightStruct>(
    //         "/tl_bbox_info_new", 10, callback);
    // }

private:

    void topic_callback(const traffic_light_msgs::msg::TrafficLightStruct::SharedPtr msg);

    std::unordered_map<std::string, TlColor> color_map_;
    std::unordered_map<std::string, double> time_map_;


    std::map<TlColor, std::string> kColorStr = {{UNKNOWN_COLOR, "unknown"},
                                              {RED, "red"},
                                              {GREEN, "green"},
                                              {YELLOW, "yellow"},
                                              {BLACK, "black"}};

    std::string id="1";
    struct ReviseOption {
      // explicit ReviseOption(const double timestamp) : ts(timestamp) {}
      double ts;  // timestamp for lights
    };
    ReviseOption option;
    // ???/////////////////////////////////////
    // void ComputeRectsOffset(const cv::Rect &rect1,
    //                                    const cv::Rect &rect2, int *offset);
    // void BBoxCallback(const traffic_light_msgs::msg::TrafficLightStruct::SharedPtr msg);
    // bool BoxIsValid(const cv::Rect &box, const cv::Size &size);
    // float Get1dGaussianScore(float x1, float x2, float sigma);
    // float Get2dGaussianScore(const cv::Point2f &p1, const cv::Point2f &p2,
    //                      float sigma1, float sigma2);
    // cv::Point2f GetCenter(const cv::Rect &box);  
    // void Select( std::vector<Image_Light> &hdmap_bboxes,
    //                          std::vector<Image_Light> &refined_bboxes,
    //                         std::vector<Image_Light> *selected_bboxes);
    // rclcpp::Subscription<traffic_light_msgs::msg::TrafficLightStruct>::SharedPtr bbox_sub_;
    // int count = 0;
    // cv::Rect box;                                                                                                                                                                                                                                                                                                                                                                                 
    // Prevents this Node from being copied
    RCLCPP_DISABLE_COPY(Reviser)

    rclcpp::Subscription<traffic_light_msgs::msg::TrafficLightStruct>::SharedPtr rev_subscription_;

};
