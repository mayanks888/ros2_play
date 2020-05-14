#include "cpp_pubsub/Reviser.hpp"

Reviser::Reviser() : Node("reviser")
  {
    // subscription_ = this->create_subscription<std_msgs::msg::String>( "topic", 10, std::bind(&MinimalSubscriber::topic_callback, this, _1));
//     // subscription_ = this->create_subscription<std_msgs::msg::String>( "topic", 10, std::bind(&MinimalSubscriber::topic_callback, this, _1));
//     subscription_ = this->create_subscription<traffic_light_msgs::msg::TrafficLightStruct>( "/tl_bbox_info_new", 10, std::bind(&Processor::void Processor::BBoxCallback(const traffic_light_msgs::msg::TrafficLightStruct::SharedPtr msg)
// , this, _1));

    //  auto callback = std::bind(&Reviser::BBoxCallback, this, _1);

    // rev_subscription_ = this->create_subscription<traffic_light_msgs::msg::TrafficLightStruct>(
    //         "/tl_bbox_info_new", 10, callback);

    // std::cout<<"process___________________________________________________"<<std::endl;

    rev_subscription_ = this->create_subscription<traffic_light_msgs::msg::TrafficLightStruct>("/snowball/perception/traffic_light/recogniser_output", 10, std::bind(&Reviser::topic_callback, this, _1));
    std::cout<<"reviser process___________________________________________________"<<std::endl;
    // auto callback = std::bind(&MinimalSubscriber::topic_callback, this, _1);
    // subscription_ = this->create_subscription<traffic_light_msgs::msg::TrafficLightStruct>("/tl_bbox_info_new", 10, callback);
  }


  void Reviser::topic_callback(const traffic_light_msgs::msg::TrafficLightStruct::SharedPtr msg)
      {
        // std::cout<<1<<std::endl;

        ////////////////////////////////////////////////////////////////////////////////////
        typedef std::shared_ptr<Image_Light> LightPtr;
        // LightPtr mytemp(new Image_Light);
        LightPtr mylight (new Image_Light);
        std::vector<LightPtr> lights_ref ; //= new LightPtr;
        mylight->color=UNKNOWN_COLOR;
          // lights_ref.confidence=0.2;
        
        lights_ref.push_back(mylight);
        // ????????????????v
        option.ts=msg->selected_box.header.stamp.sec;
       // double timestamp= msg->selected_box.header.stamp;
      // //////////////////////
    
      /////////////////////////
      // lights_ref.color.Tlcolor=red;
        for (size_t i = 0; i < lights_ref.size(); ++i) {
        // std::string id = lights_ref[i]->info.id().id();
          std::cout << lights_ref[i]->color << std::endl;
          switch (lights_ref[i]->color) {
            default:
            case BLACK:
            case UNKNOWN_COLOR:
              // if (color_map_.find(id) != color_map_.end() && option.ts > 0 && option.ts - time_map_[id] < config_.color_reviser_config().blink_time()) {
              if (color_map_.find(id) != color_map_.end() && option.ts > 0 && option.ts - time_map_[id] <1.5)
              { 
                std::cout << "Revise " << kColorStr[lights_ref[i]->color] << " to color " << kColorStr[color_map_[id]];
                lights_ref[i]->color = color_map_[id];
              } else {
                std::cout << "Unrevised color " << kColorStr[lights_ref[i]->color];
                }
              break;
            case YELLOW:
              // if YELLOW appears after RED, revise it to RED
                if (color_map_.find(id) != color_map_.end() && option.ts > 0 &&
                    color_map_.at(id) == RED) {
                  lights_ref[i]->color = color_map_.at(id);
                  std::cout << "Revise Yellow to color Red";
                  color_map_[id] = RED;
                  time_map_[id] = option.ts;
                  break;
                }
            case RED:
            case GREEN:
              if (time_map_.size() > 10) {
                color_map_.clear();
                time_map_.clear();
              }
              color_map_[id] = lights_ref[i]->color;
              time_map_[id] = option.ts;
              std::cout << "Revise Keep Color Unchanged: " << kColorStr[lights_ref[i]->color]<<std::endl;
              break;
    }
      }
      }