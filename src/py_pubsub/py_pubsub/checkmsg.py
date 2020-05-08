import rclpy
from rclpy.node import Node
# from traffic_light_msgs.msg import TrafficLightData
# from traffic_light_msgs.msg import RectifierData
from traffic_light_msgs.msg import RectifierData
# from traffic_light_msgs.srv import TestService
# # from tutorial_interfaces.msg import Num
# from tutorial_interfaces.msg import Num    # CHANGE

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(RectifierData, 'mayank_topic', 10)     # CHANGE
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        # msg = Num() 
        mydata=RectifierData()
        # mydata=1
        mydata.detected_box= [-1.0, 10.0, 10.0, 10.0, 10.0, 10.0]
        another_time_msg=self.get_clock().now().to_msg()  
        #############################################################33
        mytime=rclpy.clock.Clock().now()
        # ###############################################################                                        # CHANGE
        # msg.num = self.i    
        # mydata.header.stamp=another_time_msg                                  # CHANGE
        self.publisher_.publish(mydata)
        print("my data is ", mydata.detected_box)
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