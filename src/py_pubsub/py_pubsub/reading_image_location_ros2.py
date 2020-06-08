import rclpy
from rclpy.node import Node

# from tutorial_interfaces.msg import Num        # CHANGE
from traffic_light_msgs.msg import  TrafficLightStruct
from sensor_msgs.msg import Image
from tf2_msgs.msg import TFMessage
import os
import cv_bridge
import cv2
class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('reading_image_loc')
        self.subscription = self.create_subscription( Image, '/apollo/sensor/camera/traffic/image_short', self.listener_callback, 10)
        # self.subscription = self.create_subscription( Image, '/apollo/perception/traffic_light', self.listener_callback, 10)
        self.subscription_2 = self.create_subscription(TFMessage, '/tf', self.callback, 10)

        self.base_pth="/home/mayank_s/Desktop/template/farm_2/farm_2_images2"
        # base_path=self.base_pth
        if not os.path.exists(self.base_pth):
              print("base_path folder not present. Creating New folder...")
              os.makedirs(self.base_pth)
        self.loop=0
        print("ready to process process----------------------------------------------------------")

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
        # print("projection roi",msg.projection_roi)
        # print("cropped roi",msg.cropped_roi)
        #########################################3333
        # this is for projection roi
        image_msg=msg
        bridge = cv_bridge.CvBridge()
        cv_img = bridge.imgmsg_to_cv2(image_msg, 'passthrough')
        # print("image shape is ", cv_img.shape)
        image_np = cv_img
        image_np = cv2.cvtColor(image_np, cv2.COLOR_BAYER_BG2BGR, 3) 
        ###############################################3333
        show=False
        if show:
            cv2.namedWindow('cropped',cv2.WINDOW_NORMAL)
            cv2.resizeWindow('cropped', 600,600)
            cv2.moveWindow('cropped', 1500,220) 
            cv2.imshow("cropped", image_np)
            cv2.waitKey(1)
        
        ########################################3333
       
        self.loop+=1
          # base_path = "./xishui_new"
        # save_path=(self.base_pth +"/"  +self.position+'.jpg')
        save_path=(self.base_pth + "/" +str(self.loop)+"_" +self.position+'.jpg')
        cv2.imwrite(save_path, image_np, [cv2.IMWRITE_JPEG_QUALITY, 100])


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()