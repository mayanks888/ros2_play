import rclpy
from rclpy.node import Node

# from tutorial_interfaces.msg import Num        # CHANGE
from traffic_light_msgs.msg import  TrafficLightStruct
import cv_bridge
import cv2
class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription( TrafficLightStruct, '/tl_bbox_info_new', self.listener_callback, 10)
        self.subscription
        print("ready to process process----------------------------------------------------------")


    def listener_callback(self, msg):
        print("projection roi",msg.projection_roi)
        print("cropped roi",msg.cropped_roi)
        
        #########################################3333
        # this is for projection roi
        image_msg=msg.raw_image
        bridge = cv_bridge.CvBridge()
        cv_img = bridge.imgmsg_to_cv2(image_msg, 'passthrough')
        # print("image shape is ", cv_img.shape)
        image_np = cv_img
        image_np = cv2.cvtColor(image_np, cv2.COLOR_BAYER_BG2BGR, 3) 
        cv2.rectangle(image_np,(msg.projection_roi.x_offset,msg.projection_roi.y_offset),
                      (msg.projection_roi.x_offset+msg.projection_roi.width,msg.projection_roi.y_offset+msg.projection_roi.height), (255,0,0), 2)
        cv2.imshow('AI rectifier', image_np)
        ch = cv2.waitKey(1)
        ################################################
        ################################################
        # this is for cropped roi

    #    x_offset=1012, y_offset=415, height=300, width=
        cropped_roi=msg.cropped_roi
        print('new data',cropped_roi)
        # crop_img = img[y:y+h, x:x+w]
        image_np = image_np[cropped_roi.y_offset:cropped_roi.y_offset+cropped_roi.height, cropped_roi.x_offset:cropped_roi.x_offset+cropped_roi.width]
        cv2.imshow("cropped", crop_img)
        cv2.waitKey(1)
       ######################################################3
        # image_msg=msg.raw_image
        # bridge = cv_bridge.CvBridge()
        # cv_img = bridge.imgmsg_to_cv2(image_msg, 'passthrough')
        # # print("image shape is ", cv_img.shape)
        # image_np = cv_img
        # image_np = cv2.cvtColor(image_np, cv2.COLOR_BAYER_BG2BGR, 3) 
        # cv2.rectangle(image_np,(msg.projection_roi.x_offset,msg.projection_roi.y_offset),
        #               (msg.projection_roi.x_offset+msg.projection_roi.width,msg.projection_roi.y_offset+msg.projection_roi.height), (255,0,0), 2)
        # cv2.imshow('AI rectifier', image_np)
        # ch = cv2.waitKey(1)
        ###################################################
        # self.get_logger().info('I heard: "%d"' % msg.detections) # CHANGE


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()