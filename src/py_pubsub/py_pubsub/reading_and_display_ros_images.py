import rclpy
from rclpy.node import Node

# from tutorial_interfaces.msg import Num        # CHANGE
from traffic_light_msgs.msg import  TrafficLightStruct
from sensor_msgs.msg import Image
import cv_bridge
import cv2
class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('reading_image')
        self.subscription = self.create_subscription( Image, '/apollo/sensor/camera/traffic/image_short', self.listener_callback, 10)
        # self.subscription = self.create_subscription( Image, '/apollo/perception/traffic_light', self.listener_callback, 10)
        self.subscription
        print("ready to process process----------------------------------------------------------")


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
        
        cv2.namedWindow('cropped',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('cropped', 600,600)
        cv2.moveWindow('cropped', 1500,220) 

        cv2.imshow("cropped", image_np)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()