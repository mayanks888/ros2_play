import sys
import os
print("my sys path",sys.path)
# os.system('./install/setup.bash')
# PYTHONPAth=
# sys.path.append(('/home/mayank_s/playing_ros/dev_ws_rectifer/src/py_pubsub/py_pubsub', '/home/mayank_s/playing_ros/dev_ws_rectifer/install/py_pubsub/lib/python3.6/site-packages', '/home/mayank_s/playing_ros/dev_ws_rectifer/install/traffic_light_msgs/lib/python3.6/site-packages', '/home/mayank_s/playing_ros/dev_ws_rectifer/install/rectifier/lib/python3.6/site-packages', '/opt/ros/dashing/lib/python3.6/site-packages', '/usr/lib/python36.zip', '/usr/lib/python3.6', '/usr/lib/python3.6/lib-dynload', '/home/mayank_s/.local/lib/python3.6/site-packages', '/usr/local/lib/python3.6/dist-packages', '/usr/lib/python3/dist-packages'))
# # sys.path.append(os.getcwd())
# sys.path=['/home/mayank_s/playing_ros/dev_ws_rectifer/src/py_pubsub/py_pubsub', '/home/mayank_s/playing_ros/dev_ws_rectifer/install/py_pubsub/lib/python3.6/site-packages', '/home/mayank_s/playing_ros/dev_ws_rectifer/install/traffic_light_msgs/lib/python3.6/site-packages', '/home/mayank_s/playing_ros/dev_ws_rectifer/install/rectifier/lib/python3.6/site-packages', '/opt/ros/dashing/lib/python3.6/site-packages', '/usr/lib/python36.zip', '/usr/lib/python3.6', '/usr/lib/python3.6/lib-dynload', '/home/mayank_s/.local/lib/python3.6/site-packages', '/usr/local/lib/python3.6/dist-packages', '/usr/lib/python3/dist-packages']

# print("my sys path after",sys.path)
import rclpy
from rclpy.node import Node

# from traffic_light_msgs.msg import TrafficLightData
from traffic_light_msgs.msg import TrafficLightStruct, Detection2D

# from traffic_light_msgs.srv import TestService


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(TrafficLightStruct, 'mayank_topic', 10)     # CHANGE
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        # msg = Num() 
        mydata=TrafficLightStruct()

        #############################################33
        detect_data=Detection2D()
        detect_data.id=1
        detect_data.score=0.20
        mydata.detections.append(detect_data)
        detect_data=Detection2D()
        detect_data.id=40
        detect_data.score=0.80
        mydata.detections.append(detect_data)
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # mydata.selected_box.id=1
        # mydata.selected_box.score=0.20
        # mydata.detections.append(mydata.selected_box)
        # mydata.selected_box.id=40
        # mydata.selected_box.score=0.80
        # mydata.detections.append(mydata.selected_box)
        # mydata=1
        # mydata.detected_box= [-1.0, 10.0, 10.0, 10.0, 10.0, 10.0]
        another_time_msg=self.get_clock().now().to_msg()  
        #############################################################33
        mytime=rclpy.clock.Clock().now()
        # ###############################################################                                        # CHANGE
        # msg.num = self.i    
        mydata.header.stamp=another_time_msg                                  # CHANGE
        self.publisher_.publish(mydata)
   
        print("my data is ", mydata.selected_box)
        print("my new_time is ", mytime.to_msg())

        print("my time is ", mydata.header.stamp)
        # self.get_logger().info('Publishing: "%d"' % mydata.detected_box)  # CHANGE
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
