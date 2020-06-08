#this  implementation mainly work on grey scale image
import argparse
import shutil
from pathlib import Path
import pandas as pd
# import natsort
# from oneshot.qatm_pytorch_v3 import CreateModel, ImageDataset,ImageDataset_2, plot_result_mayank, nms, run_one_sample_mayank
from oneshot.qatm_pytorch_v3 import *
from torchvision import models
from oneshot.data_preprocess import find_template,find_template_2
from oneshot.utils import *
import rclpy
from rclpy.node import Node
import os
# from tutorial_interfaces.msg import Num        # CHANGE
from traffic_light_msgs.msg import  TrafficLightStruct
import cv_bridge
import cv2
from geometry_msgs.msg import TransformStamped
from tf2_msgs.msg import TFMessage
import tf2_msgs
import pandas as pd
from data_preprocess import *
from qatm_pytorch_v3 import *
import time
import copy
class QATM(Node):

# def __init__(self):
  def __init__(self, args_):
      self.opt = args_
      # with open(os.path.join(sys.path[0], "my_file.txt"), "r") as f:
      #   print(f.read())
      # loading model
      self.model_1 = models.vgg19(pretrained=False)
      print('mysysis',sys.path)
      sys.path[0]="src/oneshot/oneshot"
      # model.state_dict(''/home/mayank_s/Desktop/template/model/vgg19-dcbb9e9d.pth'')
      self.model_1.load_state_dict(torch.load(os.path.join(sys.path[0], "weights/vgg19-dcbb9e9d.pth")))
      # self.model_1.load_state_dict(torch.load('/myspc/install/oneshot/oneshot/weights/vgg19-dcbb9e9d.pth'))
      self.model = CreateModel(model=self.model_1.features, alpha=self.opt.alpha, use_cuda=self.opt.cuda)
      # self.model = CreateModel(model=models.vgg19(pretrained=True).features, alpha=self.opt.alpha, use_cuda=self.opt.cuda)
      # self.template_root = "/home/mayank_s/playing_ros/c++/ros2_play_old/src/oneshot/oneshot/data/farm_1/saved_temp_img"
      self.template_root = os.path.join(sys.path[0], "data/farm_1/saved_temp_img")
      # input_folder = '/home/mayank_s/Desktop/template/saved_temp_cropped'
      
      self.csv_name =os.path.join(sys.path[0], "data/farm_1/final_snowball.csv")
      self.ref_id = 'tl1001'
      self.show=False
      self.df = pd.read_csv(self.csv_name)
      # ///////////////////////////////////////
   
      super().__init__('qatm_subs_1')#always new node name remember"
      # self.subscription = self.create_subscription( TrafficLightStruct, '/snowball/perception/traffic_light/recogniser_output', self.listener_callback, 10)
      self.subs_prep = self.create_subscription( TrafficLightStruct, '/snowball/perception/traffic_light/preprocessor', self.listener_callback, 10)
      # self.subscription = self.create_subscription(TFMessage, '/tf', self.listener_callback, 10)
      self.subs_tf = self.create_subscription(TFMessage, '/tf', self.callback, 10)

      self.bblabel=[]
      self.loop=0
      print("ready to process one shot----------------------------------------------------------")

  def callback(self,data):
      # print("Hello")
      self.x_pose=data.transforms[0].transform.translation.x
      self.y_pose=data.transforms[0].transform.translation.y
      self.position=str(self.x_pose)+'_'+str(self.y_pose)

  def listener_callback(self, msg):
      # ///////////////////////////////////////////////
      # loading image
      t1=time.time()
      image_msg=msg.raw_image
      bridge = cv_bridge.CvBridge()
      cv_img = bridge.imgmsg_to_cv2(image_msg, 'passthrough')
      image_np = cv2.cvtColor(cv_img, cv2.COLOR_BAYER_BG2BGR, 3)
      # //////////////////////////////////////////////////////////////////////
      cropped_roi=msg.cropped_roi
      print('new data',cropped_roi)
      # crop_img = img[y:y+h, x:x+w]
      crop_img = image_np[cropped_roi.y_offset:cropped_roi.y_offset+cropped_roi.height, cropped_roi.x_offset:cropped_roi.x_offset+cropped_roi.width]
      #showing image
      if self.show:
        cv2.imshow("cropped", crop_img)
        cv2.waitKey(1)
      ######################################################333
      temp_name,bbox_info,min_dist_val=find_template_2(self.ref_id,[float(self.x_pose),float(self.y_pose)],self.df)
      print("current template image is ", temp_name)
      # if temp_name==1:
      #   continue
          # print("waiting for image with id ",ref_id)
          # if show:
          #     imgk=cv2.imread(os.path.join(root,filename))
          #     cv2.putText(imgk, "ID NOT FOUND", (10, 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)
          #     cv2.imshow("img5", imgk)
          #     # cv2.imshow('img', img)
          #     ch = cv2.waitKey(0)
          #     if ch & 0XFF == ord('q'):
          #         cv2.destroyAllWindows()
          #     cv2.destroyAllWindows()
        

      ####################################################################
      # saving template
      temp_path =self.template_root+"/"+temp_name
      img = cv2.imread(temp_path)
      temp_scale_2 =40
      # frame = img[int(bbox_info[1]):int(bbox_info[3]), int(bbox_info[0]):int(bbox_info[2])]
      # frame = img[int(bbox_info[1]-50):int(bbox_info[3]+100), int(bbox_info[0]-50):int(bbox_info[2]+50)]
      frame = img[int(bbox_info[1] - temp_scale_2):int(bbox_info[3] + temp_scale_2),
                        int(bbox_info[0] - temp_scale_2):int(bbox_info[2] + temp_scale_2)]
      ##########################3
      show_temp=True
      if show_temp:

            cv2.imshow('img_frame', frame)
            ch = cv2.waitKey(1)
        #   if ch & 0XFF == ord('q'):
        #       cv2.destroyAllWindows()
        #   # cv2.waitKey(1)
        #   cv2.destroyAllWindows()
      cv2.imwrite(os.path.join(sys.path[0], "data/temp/mytemp.jpg"), frame)
      ##############################################333
      #saving croped images
      image_path=os.path.join(sys.path[0], "data/sample/sample.jpg")
      # image_path="/home/mayank_s/playing_ros/c++/ros2_play_old/src/oneshot/oneshot/data/sample/"+self.position+".jpg"
      cv2.imwrite(image_path, crop_img)

################################################
      template_dir =self.opt.template_images_dir
      # image_path =root+"/"+filename
    #   dataset = ImageDataset_3(Path(template_dir), crop_img, thresh_csv='src/oneshot/oneshot/thresh_template.csv')
      dataset = ImageDataset_2(Path(template_dir), image_path, thresh_csv=os.path.join(sys.path[0], "data/thresh_template.csv"))
    #   t1=time.time()
      # scores, w_array, h_array, thresh_list = run_multi_sample(model, dataset)
      # self.model = CreateModel(model=models.vgg19(pretrained=True).features, alpha=self.opt.alpha, use_cuda=self.opt.cuda)
      # mymodel=self.model
      model = copy.deepcopy(self.model)
      # model =self.model
      scores, w_array, h_array, thresh_list = run_one_sample_mayank(model, dataset)
      # scores, w_array, h_array, thresh_list = run_one_sample_mayank(self.model, dataset)
      # scores, w_array, h_array, thresh_list=run_one_sample(model, dataset['template'], dataset['image'], dataset['image_name'])
      # print("nms...")
      time_take=(time.time()-t1)*1000
      print('amount of time taken',time_take)
      # _ = plot_result_multi(model,dataset.image_raw, boxes, indices, show=True, save_name='result.png')
      thresh_list = .99
      t2=time.time()

      boxes,_,max_score = nms(scores, w_array, h_array, thresh_list)
      limit_boxes = 5
      boxes = boxes[:limit_boxes]
      print("time taken in nms", (time.time() - t2) * 1000)
      show=True
      if show:
        print('image_shape is ',dataset.image_raw.shape)
        # _ = plot_result_multi(dataset.image_raw, boxes, indices, show=True, save_name='result.png')
        _ = plot_result_mayank(dataset.image_raw, boxes, show=True, save_name='result.png')
# ///////////////////////////////////////////////////////////////////
def main(args=None):
    # ssssssssssssssssssssssssssssssss
    parser = argparse.ArgumentParser(description='QATM Pytorch Implementation')
    parser.add_argument('--cuda',default=True, action='store_true')
    parser.add_argument('-s', '--sample_image', default='data/sample/gwm_1284.jpg')
    # parser.add_argument('-t', '--template_images_dir', default='/home/mayank_sati/Desktop/qatm_data/template/')
    parser.add_argument('-t', '--template_images_dir', default=os.path.join(sys.path[0], "data/temp/"))
    parser.add_argument('--alpha', type=float, default=25)
    parser.add_argument('--thresh_csv', type=str, default=os.path.join(sys.path[0], "data/thresh_template.csv"))
    opt = parser.parse_args()

    # sssssssssssssssssssssssssssssss
    # print(opt)
    rclpy.init(args=args)
    # with torch.no_grad():
    node = QATM(opt)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()