// #include "tl_processor.h"
#include "cpp_pubsub/tl_processor.hpp"

// #include "utils/utils.hpp"
Processor::Processor()
  : Node("mayank_subscriber_2")
  {
    // subscription_ = this->create_subscription<std_msgs::msg::String>( "topic", 10, std::bind(&MinimalSubscriber::topic_callback, this, _1));
//     // subscription_ = this->create_subscription<std_msgs::msg::String>( "topic", 10, std::bind(&MinimalSubscriber::topic_callback, this, _1));
//     subscription_ = this->create_subscription<traffic_light_msgs::msg::TrafficLightStruct>( "/tl_bbox_info_new", 10, std::bind(&Processor::void Processor::BBoxCallback(const traffic_light_msgs::msg::TrafficLightStruct::SharedPtr msg)
// , this, _1));

     auto callback = std::bind(&Processor::BBoxCallback, this, _1);

    mysubscription_ = this->create_subscription<traffic_light_msgs::msg::TrafficLightStruct>(
            "/tl_bbox_info_new", 10, callback);
    std::cout<<"process___________________________________________________"<<std::endl;
    // auto callback = std::bind(&MinimalSubscriber::topic_callback, this, _1);
    // subscription_ = this->create_subscription<traffic_light_msgs::msg::TrafficLightStruct>("/tl_bbox_info_new", 10, callback);
  }

void Processor::BBoxCallback(const traffic_light_msgs::msg::TrafficLightStruct::SharedPtr msg)
{
    // Prints the message to the log and flushes it.
    // RCLCPP_INFO(this->get_logger(), "melvin Bounding box : [%f], [%f], [%f], [%f], [%f]", msg->data[0], msg->data[1], msg->data[2], msg->data[3], msg->data[4]);
    RCLCPP_INFO(this->get_logger(), "-------------------------------"); //, msg->data.size());
    int j = 0;
Image_Light lights_ref_obj;
Image_Light detected_bboxes_obj;

// #########################333
typedef std::shared_ptr<Image_Light> LightPtr;
LightPtr mytemp(new Image_Light);
// Image_Light mytemp;
// #############################

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
  // ????????????????????////////////////////
  mytemp->rectified_roi.x= m.x_offset;
  mytemp->rectified_roi.y = m.y_offset;
  mytemp->rectified_roi.height= m.height;
  mytemp->rectified_roi.width= m.width;
  mytemp->detect_score= m.score;

  mytemp->is_detected = true;
  detected_bboxes.push_back(*mytemp);
  ////////////////////////////////////////////
  

// ##############################################
  //  temp.x = m.x_offset;
  //  temp.y = m.y_offset;
  //  temp.height = m.height;
  //  temp.width = m.width ;
  //  score = m.score;


  //  std::cout<<"before projection  boxes 27 :- .... :- " << std::endl;
  //  detected_bboxes_obj.debug_roi.push_back(temp); // = temp;
  //  std::cout<<"before projection  boxes 29 :- .... :- " << std::endl;
  //  detected_bboxes_obj.debug_roi_detect_scores.push_back(score); // = score;
  //  std::cout<<"before projection  boxes 31 :- .... :- " << std::endl;
  //  detected_bboxes.push_back(detected_bboxes_obj);
  //  std::cout<<"before projection  boxes 23 :- .... :- " << std::endl;
      //    lights_ref[0].debug_roi[j] = temp;
      //    std::cout<<"before projection  boxes 35 :- .... :- " << std::endl;
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

  //////////////////////////////////////////////////
  // for (auto i: detected_bboxes)
  // {
  //   std::cout<<i.debug_roi[0];
  //   // i.debug_roi;
  // }
  for (size_t col = 0; col < detected_bboxes.size(); ++col) {
    // std::cout<<col;
    std::cout<<detected_bboxes[col].rectified_roi<<std::endl;

      // cv::Point2f center_refine =
      //     GetCenter(refined_bboxes[col].rectified_roi);
      // auto width_refine = refined_bboxes[col].rectified_roi.width;
  }
  ////////////////////////////////////////////////////
  Select(lights_ref, detected_bboxes, &selected_bboxes);



  for (size_t i = 0; i < lights_ref.size(); ++i) {
    if (!selected_bboxes[i].is_detected ||
        !selected_bboxes[i].is_selected) {
    }
    cv::Rect region = selected_bboxes[i].rectified_roi;
    lights_ref[i].rectified_roi = region;
    lights_ref[i].detect_class_id =
        selected_bboxes[i].detect_class_id;
    lights_ref[i].detect_score =
        selected_bboxes[i].detect_score;
    lights_ref[i].is_detected = selected_bboxes[i].is_detected;
    lights_ref[i].is_selected = selected_bboxes[i].is_selected;
    std::cout<<selected_bboxes[i].detect_score<<std::endl;
    std::cout<<selected_bboxes[i].rectified_roi<<std::endl;
    std::cout<<"our projection roi :- .... :- "<<lights_ref_obj.projection_roi<<std::endl;
  }
///////////////////////////////////////////////////////////////
// visualising image now
  cv::Mat mat_, src;
  src = cv::Mat(msg ->raw_image.height, msg->raw_image.width, CV_8UC3);
  cv_bridge::CvImagePtr cv_ptr = cv_bridge::toCvCopy( msg->raw_image, sensor_msgs::image_encodings::BGR8);
  src = cv_ptr->image;

    
  mat_ = src.clone();
    ////////////////////////////////////
  cv::Rect tmp_may;
  tmp_may.x = msg->cropped_roi.x_offset;
  tmp_may.y = msg->cropped_roi.y_offset;
  tmp_may.height =  msg->cropped_roi.height;
  tmp_may.width =msg->cropped_roi.width;
  // lights_ref_obj.projection_roi = tmp;s
  // cv::Rect myrect=msg->cropped_roi;
    // cv:Rect my_rect ;
    cv::Mat croppedImage = mat_(tmp_may);
    ////////////////////////////////////////
    bool should_show = true;
    if (should_show)
    {
        cv::rectangle(croppedImage, selected_bboxes[0].rectified_roi, cv::Scalar(0, 255, 0), 2, 8, 0);
        cv::rectangle(croppedImage, lights_ref_obj.projection_roi, cv::Scalar(0, 0, 255), 2, 8, 0);
        // cv::resize(mat_, mat_, cv::Size(960, 540));z
        cv::imshow("image", croppedImage);
        cv::waitKey(1);
    }
    // AINFO << region;
  }
    // AINFO << region;
  



/*
  for (auto &light : lights_ref) {
    // By default, the first debug ros is crop roi. (Reserve a position here).
    light.rectified_roi = light.projection_roi;
    light.debug_roi.push_back(cv::Rect(0, 0, 0, 0));
    light.debug_roi_detect_scores.push_back(0.0f);
  }

  cv::Rect cbox = pre_->GetCropRoi();
  if (BoxIsValid(cbox, cv::Size(2064, 1544))) {
    lights_ref[0].debug_roi[0] = cbox;

    for (size_t j = 0; j < detected_bboxes.size(); ++j) {
      cv::Rect &region = detected_bboxes[j].rectified_roi;
      float score = detected_bboxes[j].detect_score;
      region.x += cbox.x;
      region.y += cbox.y;
      lights_ref[0].debug_roi.push_back(region);
      lights_ref[0].debug_roi_detect_scores.push_back(score);
    }

    Select(lights_ref, detected_bboxes, &selected_bboxes);
  } else {
    for (size_t h = 0; h < lights_ref.size(); ++h) {
      Image_Light light = lights_ref[h];
      light.is_detected = false;
      selected_bboxes.push_back(light);
    }
  }
    std::flush(std::cout);
}
*/
bool Processor::BoxIsValid(const cv::Rect &box, const cv::Size &size) {
  if (box.width <= 0 || box.height <= 0 || box.x >= size.width ||
      box.y >= size.height || box.x + box.width - 1 < 0 ||
      box.y + box.height - 1 < 0) {
    return false;
  }
  return true;
}

cv::Point2f Processor::GetCenter(const cv::Rect &box) {
  return cv::Point2f(box.x + box.width / 2, box.y + box.height / 2);
}

float Processor::Get2dGaussianScore(const cv::Point2f &p1, const cv::Point2f &p2,
                         float sigma1, float sigma2) {
  return static_cast<float>(
      std::exp(-0.5 * (((p1.x - p2.x) * (p1.x - p2.x)) / (sigma1 * sigma1) +
                       ((p1.y - p2.y) * (p1.y - p2.y)) / (sigma2 * sigma2))));
}

float Processor::Get1dGaussianScore(float x1, float x2, float sigma) {
  return static_cast<float>(
      std::exp(-0.5 * (x1 - x2) * (x1 - x2) / (sigma * sigma)));
}

void Processor::Select(std::vector<Image_Light> &hdmap_bboxes,
                           std::vector<Image_Light> &refined_bboxes,
                            std::vector<Image_Light> *selected_bboxes) {
  // find bbox with max area in refined_bboxes
  std::cout<<1<<std::endl;
  auto max_area_refined_bbox =
      std::max_element(refined_bboxes.begin(), refined_bboxes.end(),
                       [](const Image_Light lhs, const Image_Light rhs) {
                         return lhs.rectified_roi.area() <
                                rhs.rectified_roi.area();
                       });
  
  //  cv::Mat_<int> cost_matrix(hdmap_bboxes.size(), refined_bboxes.size());
  std::vector<std::vector<double> > score_matrix(
      hdmap_bboxes.size(), std::vector<double>(refined_bboxes.size(), 0));
  for (size_t row = 0; row < hdmap_bboxes.size(); ++row) {
    cv::Point2f center_hd = GetCenter(hdmap_bboxes[row].rectified_roi);
    auto width_hd = hdmap_bboxes[row].rectified_roi.width;
    for (size_t col = 0; col < refined_bboxes.size(); ++col) {
      cv::Point2f center_refine =
          GetCenter(refined_bboxes[col].rectified_roi);
      auto width_refine = refined_bboxes[col].rectified_roi.width;

      // use gaussian score as metrics of distance and width
      // distance_score:
      //    larger distance => 0.
      //    smaller distance => 1
      double distance_score = static_cast<double>(
          Get2dGaussianScore(center_hd, center_refine, 100, 100));

      // width score:
      //   larger width diff => 0
      //   smaller width diff => 1
      double width_score =
          static_cast<double>(Get1dGaussianScore(width_hd, width_refine, 100));

      // normalized area score
      // larger area => 1
      double area_score = 1.0 *
                          refined_bboxes[col].rectified_roi.area() /
                          (*max_area_refined_bbox).rectified_roi.area();

      // when numerator=1， denominator is very small,
      // converting to int might reduce to same value, here uses 1000
      // + 0.05 to prevent score = 0
      // score * weight h
      score_matrix[row][col] =
          (0.05 + 0.4 * refined_bboxes[col].detect_score +
           0.2 * distance_score + 0.2 * width_score + 0.2 * area_score);
    }
  }



  HungarianOptimizer munkres(score_matrix);
  std::vector<int> hd_index;
  std::vector<int> refined_index;
  munkres.maximize(&hd_index, &refined_index);
  for (size_t i = 0; i < hdmap_bboxes.size(); ++i) {
    hdmap_bboxes[i].is_selected = false;
  }
  for (size_t i = 0; i < hd_index.size(); ++i) {
    if (hd_index[i] < 0 ||
        static_cast<size_t>(hd_index[i]) >= hdmap_bboxes.size() ||
        refined_index[i] < 0 ||
        static_cast<size_t>(refined_index[i]) >= refined_bboxes.size() ||
        hdmap_bboxes[hd_index[i]].is_selected) {
      continue;
    }
    if (score_matrix[hd_index[i]][refined_index[i]] > 0) {
      refined_bboxes[refined_index[i]].is_selected = true;
      hdmap_bboxes[hd_index[i]].is_selected = true;
      selected_bboxes->push_back(refined_bboxes[refined_index[i]]);
    }
  }
  for (size_t i = 0; i < hdmap_bboxes.size(); ++i) {
    if (!hdmap_bboxes[i].is_selected) {
      selected_bboxes->push_back(hdmap_bboxes[i]);
    }
  }
}
/*
void Processor::ComputeRectsOffset(const cv::Rect &rect1,
                                       const cv::Rect &rect2, int *offset) {
  cv::Point center1(rect1.x + rect1.width / 2, rect1.y + rect1.height / 2);
  cv::Point center2(rect2.x + rect2.width / 2, rect2.y + rect2.height / 2);

  cv::Point pt1;
  cv::Point pt2;
  // record the max lateral and longitudinal offset
  if (center2.y <= center1.y) {
    if (center2.x >= center1.x) {
      pt1 = cv::Point(rect1.x + rect1.width, rect1.y);
      pt2 = cv::Point(rect2.x + rect2.width, rect2.y);
    } else {
      pt1 = cv::Point(rect1.x, rect1.y);
      pt2 = cv::Point(rect2.x, rect2.y);
    }
  } else {
    if (center2.x >= center1.x) {
      pt1 = cv::Point(rect1.x + rect1.width, rect1.y + rect1.height);
      pt2 = cv::Point(rect2.x + rect2.width, rect2.y + rect2.height);
    } else {
      pt1 = cv::Point(rect1.x, rect1.y + rect1.height);
      pt2 = cv::Point(rect2.x, rect2.y + rect2.height);
    }
  }

  *offset = std::max(abs(pt1.x - pt2.x), abs(pt1.y - pt2.y));
}
*/

