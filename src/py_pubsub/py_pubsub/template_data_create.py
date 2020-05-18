import rclpy
from rclpy.node import Node

# from tutorial_interfaces.msg import Num        # CHANGE
from traffic_light_msgs.msg import  TrafficLightStruct
import cv_bridge
import cv2
class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('temp_subs')#always new node name remember"
        self.subscription = self.create_subscription( TrafficLightStruct, '/snowball/perception/traffic_light/processor', self.listener_callback, 10)
        self.subscription
        print("ready to datasets storage----------------------------------------------------------")


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
        width=int(msg.projection_roi.width/2)
        height=int(msg.projection_roi.height/2)
        image_np = cv2.cvtColor(image_np, cv2.COLOR_BAYER_BG2BGR, 3) 
        # cv2.rectangle(image_np,(msg.projection_roi.x_offset,msg.projection_roi.y_offset),
        #               (msg.projection_roi.x_offset+msg.projection_roi.width,msg.projection_roi.y_offset+msg.projection_roi.height), (255,0,0), 2)
        # cv2.imshow('AI rectifier', image_np)
        # ch = cv2.waitKey(1)
        ################################################
        ################################################
        # this is for cropped roi

    #    x_offset=1012, y_offset=415, height=300, width=
        cropped_roi=msg.selected_box
        print('new data',cropped_roi)
        # crop_img = img[y:y+h, x:x+w]
        crop_img = image_np[cropped_roi.y_offset:cropped_roi.y_offset+cropped_roi.height, cropped_roi.x_offset:cropped_roi.x_offset+cropped_roi.width]
        
        # cY=int(cropped_roi.y_offset+(cropped_roi.height)/2)
        # cX=int(cropped_roi.x_offset+(cropped_roi.width)/2)
        # # cv2.circle(image_np, (cX, cY), 7, (0, 255, 255), -1)
        # cv2.circle(crop_img, (150, 150), 7, (0, 0, 255), -1)
        # cv2.rectangle(crop_img,(150-width,150-height),(150+width,150+height), (255,0,255), 2)
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