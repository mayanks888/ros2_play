// Copyright 2016 Open Source Robotics Foundation, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "traffic_light_msgs/msg/traffic_light_struct.hpp"
// #include "opencv2/opencv.hpp"
#include "image/image_lights.h"

using std::placeholders::_1;

    // explicit Processor(const rclcpp::NodeOptions &options)

class MinimalSubscriber : public rclcpp::Node
{
public:
  MinimalSubscriber()
  : Node("mayank_subscriber_2")
  {
    // subscription_ = this->create_subscription<std_msgs::msg::String>( "topic", 10, std::bind(&MinimalSubscriber::topic_callback, this, _1));
    // subscription_ = this->create_subscription<std_msgs::msg::String>( "topic", 10, std::bind(&MinimalSubscriber::topic_callback, this, _1));
    subscription_ = this->create_subscription<traffic_light_msgs::msg::TrafficLightStruct>( "/tl_bbox_info_new", 10, std::bind(&MinimalSubscriber::topic_callback, this, _1));
    std::cout<<"process___________________________________________________"<<std::endl;
    // auto callback = std::bind(&MinimalSubscriber::topic_callback, this, _1);
    // subscription_ = this->create_subscription<traffic_light_msgs::msg::TrafficLightStruct>("/tl_bbox_info_new", 10, callback);
  }

private:

  void topic_callback(const traffic_light_msgs::msg::TrafficLightStruct::SharedPtr msg) const
    {
      std::cout<<1<<std::endl;
      // std::cout<<msg->detections<<std::endl;
      // RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg->data.c_str());
      // RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg->selected_box;
      // RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg->detections();
      ////////////////////////////////////////////////////////////////////////////////////
      int j = 0;
      Image_Light lights_ref_obj;
      Image_Light detected_bboxes_obj;
      
      std::vector<Image_Light> lights_ref;
      std::vector<Image_Light> selected_bboxes;
      std::vector<Image_Light> detected_bboxes;
      cv::Rect temp;
      float score;
      std::cout<<"before projection  boxes 17:- .... :- " << std::endl;
      if(!msg->detections.empty())
      {
        for(auto m : msg->detections)
        {
          temp.x = m.x_offset;
          temp.y = m.y_offset;
          temp.height = m.height;
          temp.width = m.width ;
          score = m.score;
          std::cout<<"before projection  boxes 27 :- .... :- " << std::endl;
          detected_bboxes_obj.debug_roi.push_back(temp); // = temp;
          std::cout<<"before projection  boxes 29 :- .... :- " << std::endl;
          detected_bboxes_obj.debug_roi_detect_scores.push_back(score); // = score;
          std::cout<<"before projection  boxes 31 :- .... :- " << std::endl;
          detected_bboxes.push_back(detected_bboxes_obj);
          std::cout<<"before projection  boxes 23 :- .... :- " << std::endl;
              //   lights_ref[0].debug_roi[j] = temp;
              //   std::cout<<"before projection  boxes 35 :- .... :- " << std::endl;
              //   //  std::cout<<"before projection  boxes 34:- .... :- " << std::endl;
              // lights_ref[0].debug_roi_detect_scores[j]  = score;
              // std::cout<<"before projection  boxes 38 :- .... :- " << std::endl;
              // j++;
        }
      }
      cv::Rect tmp, ctmp;
      tmp.x = msg->projection_roi.x_offset;
      tmp.y = msg->projection_roi.y_offset;
      tmp.height =  msg->projection_roi.height;
      tmp.width =msg->projection_roi.width;
      // tmp=msg->projection_roi;
      lights_ref_obj.projection_roi = tmp;
      lights_ref_obj.rectified_roi = tmp;
      std::cout<<"before projection  boxes 46 :- .... :- " << std::endl;
      lights_ref_obj.debug_roi.push_back(cv::Rect(0, 0, 0, 0));
      lights_ref_obj.debug_roi_detect_scores.push_back(0.0f);
      lights_ref.push_back(lights_ref_obj);
      ctmp.x = msg->cropped_roi.x_offset;
      ctmp.y = msg->cropped_roi.y_offset;
      ctmp.height = msg->cropped_roi.height;
      ctmp.width = msg->cropped_roi.width;
      lights_ref[0].debug_roi[0] = ctmp;
      std::cout<<"before projection  boxes :- .... :- "<<lights_ref[0].debug_roi[0] << std::endl;
      
    
    ///////////////////////////////////////////
      // lights_ref_obj.projection_roi = (msg->projection_roi);
      // lights_ref_obj.rectified_roi = msg->projection_roi;
      // lights_ref_obj.debug_roi.push_back(cv::Rect(0, 0, 0, 0));
      // lights_ref_obj.debug_roi_detect_scores.push_back(0.0f);
      // lights_ref.push_back(lights_ref_obj);
    //////////////////////////////////////////////////////////////////////////////////////
      }
    rclcpp::Subscription<traffic_light_msgs::msg::TrafficLightStruct>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MinimalSubscriber>());
  rclcpp::shutdown();
  return 0;
}
