import cv2
import rospy
import cv_bridge as bridge
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist

center = 0
pub = rospy.Publisher('/robot/cmd_vel', Twist, queue_size=10)

def image_callback(image):
    global center
    br = bridge.CvBridge()
    try:
        cv_image = br.imgmsg_to_cv2(image, desired_encoding="bgr8")
    except bridge.CvBridgeError as e:
        print(e)
    threshold = 64
    cv_grey = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    _, cv_bin = cv2.threshold(cv_grey, threshold, 255, cv2.THRESH_BINARY)
    start = 0 
    end = 0

    img_copy = cv_bin[720,:]
    flag = 0

    for i in range(800):
        px = img_copy[i]
        if px == 0 and flag == 0:
            start = i
            flag = 1
        if flag == 1 and px == 255:
            end = i
            flag = 2
            break

    if flag == 1:
        end = 799

    center = int((end + start)/2)
    print(center)
    correct_position()
    


def get_image():
    rospy.init_node('getImage', anonymous=True)
    rospy.Subscriber("/rrbot/camera1/image_raw", Image, image_callback)
    rospy.spin()


def correct_position():
    vel_msg = Twist()
    speed = set_velocity(vel_msg)
    pub.publish(speed)

def set_velocity(vel_msg):
    vel_msg.linear.y = 0.0
    vel_msg.linear.z = 0.0
    vel_msg.angular.y = 0.0
    vel_msg.angular.x = 0.0

    if center == 0:
        vel_msg.linear.x = 0.0
        vel_msg.angular.z = -0.5
    elif center < 350:
        vel_msg.linear.x = 0.0
        vel_msg.angular.z = 0.5
    elif center > 450:
        vel_msg.linear.x = 0.0
        vel_msg.angular.z = -0.5
    else:
        vel_msg.linear.x = 0.15
        vel_msg.angular.z = 0.0
    
    return vel_msg


if __name__ == '__main__':
    get_image()
