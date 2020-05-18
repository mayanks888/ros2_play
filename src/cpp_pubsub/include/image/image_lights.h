#include <iostream>
#include <bits/stdc++.h>
// #include "Eigen/Core"
#include "opencv2/opencv.hpp"


enum TlColor {
  BLACK = 0,
  GREEN = 1,
  RED = 2,
  YELLOW = 3,
  UNKNOWN_COLOR=4
};

// enum TlColor {
//   GREEN = 0,
//   YELLOW = 1,
//   RED = 2,
//   BLACK = 3,
//   UNKNOWN_COLOR=4
// };


struct Image_Light {
  Image_Light() = default;
  cv::Mat frame;
  cv::Rect projection_roi;
  std::vector<cv::Rect> debug_roi;
  std::vector<float> debug_roi_detect_scores;
  cv::Rect rectified_roi;
  bool is_detected = false; 
  bool is_selected = false;       
  TlColor color;          //  Image_Light color Status.
  int detect_class_id=1;
  // output score by detection
  float detect_score = 0.0f;
  double confidence = 0.0;

};
// typedef std::shared_ptr<Image_Light> LightPtr;
// typedef std::vector<LightPtr> LightPtrs;