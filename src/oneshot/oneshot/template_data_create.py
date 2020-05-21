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
class MinimalSubscriber(Node):

    def __init__(self):
      super().__init__('temp_subs')#always new node name remember"
      self.subscription = self.create_subscription( TrafficLightStruct, '/snowball/perception/traffic_light/processor', self.listener_callback, 10)
      # self.subscription = self.create_subscription( TrafficLightStruct, '/snowball/perception/traffic_light/preprocessor', self.listener_callback, 10)
      # self.subscription = self.create_subscription(TFMessage, '/tf', self.listener_callback, 10)
      self.subscription_2 = self.create_subscription(TFMessage, '/tf', self.callback, 10)
      self.base_pth="/home/mayank_s/Desktop/template/saved_temp"
      self.base_pth_2="/home/mayank_s/Desktop/template/saved_temp_img"
      self.bblabel=[]
      self.loop=0
      print("ready to datasets storage----------------------------------------------------------")

    def callback(self,data):
        
        # print("Hello")
        self.x=data.transforms[0].transform.translation.x
        self.y=data.transforms[0].transform.translation.y
        
        # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        # print(data.header.timestamp_sec)
        # print(data.pose.position)
        # return (data.pose.position.x)
        self.position=str(self.x)+'_'+str(self.y)
        
    def listener_callback(self, msg):
        self.loop+=1
        print(self.loop)
        print("my position is ",self.position)
        #########################################3333
        # this is for projection roi
        image_msg=msg.raw_image
        bridge = cv_bridge.CvBridge()
        cv_img = bridge.imgmsg_to_cv2(image_msg, 'passthrough')
        # print("image shape is ", cv_img.shape)
        image_np = cv_img
        width=int(msg.projection_roi.width/2)
        height=int(msg.projection_roi.height/2)
        image_np = cv2.cvtColor(image_np, cv2.COLOR_BAYER_BG2BGR, 3) 
        cv_img=image_np
        cropped_roi=msg.selected_box
        # cropped_roi=msg.cropped_roi
        print('new data',cropped_roi)
        # crop_img = img[y:y+h, x:x+w]
        crop_img = image_np[cropped_roi.y_offset:cropped_roi.y_offset+cropped_roi.height, cropped_roi.x_offset:cropped_roi.x_offset+cropped_roi.width]
      ################################################
      #showing image
        cv2.imshow("cropped", crop_img)
        cv2.waitKey(1)
        base_path=self.base_pth
        base_path2=self.base_pth_2
        if not os.path.exists(base_path):
              print("base_path folder not present. Creating New folder...")
              os.makedirs(base_path)
        if not os.path.exists(base_path2):
            print("base_path folder not present. Creating New folder...")
            os.makedirs(base_path2)
              # loop = 1
          # base_path = "./xishui_new"
        save_path=(base_path +"/"  +self.position+'.jpg')
        cv2.imwrite(save_path, crop_img, [cv2.IMWRITE_JPEG_QUALITY, 100])
        save_path2=(base_path2 +"/"  +self.position+'.jpg')
        cv2.imwrite(save_path2, cv_img, [cv2.IMWRITE_JPEG_QUALITY, 100])
       ######################################################3
        create_csv=True
        if create_csv:
          img_name = self.position + ".jpg"
            # obj_class=file_data[0]
          obj_class = "traffic_light"
          xmin = int(cropped_roi.x_offset)
          ymin = int(cropped_roi.y_offset)
          xmax = int(cropped_roi.x_offset+cropped_roi.width)
          ymax = int(cropped_roi.y_offset+cropped_roi.height)
          obj_id = "tl1001"
          width=height=0
          data_label = [img_name,0, width, height, obj_class, xmin, ymin, xmax, ymax, obj_id,self.x,self.y]
          self.bblabel.append(data_label)
#################################################
          if self.loop>=140:
            columns = ['img_name','time_stamp' ,'width', 'height', 'obj_class', 'xmin', 'ymin', 'xmax', 'ymax', 'obj_id','x_pose','y_pose']

            df = pd.DataFrame(self.bblabel, columns=columns)
            print("into csv file")
            # df.to_csv('template-traffic_light.csv', index=False)
            # csv_name = file_dir.split("/")[-1]
            # csv_name = file_dir + ".csv"
            csv_name = "/home/mayank_s/Desktop/template/final_snowball.csv"
            df.to_csv(csv_name, index=False)

        # self.get_logger().info('I heard: "%d"' % msg.detections) # CHANGE


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    minimal_subscriber.destroy_node()
    rclpy.shutdown()
    print("finally finished")


if __name__ == '__main__':
    main()