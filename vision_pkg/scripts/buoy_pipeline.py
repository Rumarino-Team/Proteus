#!/usr/bin/python
import cv2
import rospy
from std_msgs.msg import Int32, Bool
from vision_helpers.buoy_tracking import ObjectTracker
from vision_helpers.buoy_detector import Detect

class VisionPipeline:
    def __init__(self):
        rospy.init_node("BuoyVisionNode")
        self.vision_yaw_pub = rospy.Publisher("yaw_current_vision", Int32, queue_size=1)
        self.vision_depth_pub = rospy.Publisher("depth_current_vision", Int32, queue_size=1)
        self.vision_activate_sub = rospy.Subscriber("ActivateBuoyVision", Bool, self.activate_pipeline_callback)
        self.active = False
        self.data_feeder = None
        self.object_detection = Detect()
        self.object_tracking = ObjectTracker()
        self.n_frame = 10
    
    def activate_pipeline_callback(self, msg):
        self.active = msg.data

    def feed_data(self, path):
        self.data_feeder = cv2.VideoCapture(path)
    
    def run_pipeline(self): 
        n_frame = self.n_frame
        current_frame = n_frame
        bbox = None 
        data_feed = self.data_feeder
        for i in range(2):
            success, img = data_feed.read()
        while self.active:
            success, img = data_feed.read() 
            if not success:
                print("Couldn't get image from given data path")
            if n_frame == current_frame:
                x,y,width,height = 0,0,0,0
                while width==0 or height==0:
                    x,y,width,height = self.object_detection.detect(img, bbox)
                bbox = self.object_tracking.init(img, x, y, width, height)
                current_frame = 0
            else:
                bbox = self.object_tracking.track(img)
                current_frame += 1
            
            if bbox is not None:
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(img, p1, p2, (255,0,0), 2, 1)
                self.send_data(bbox)
            else:
                cv2.putText(img, "Couldn't find object", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            #cv2.imshow("Tracking", img)
            #cv2.waitKey(1)

    def destroy_objects(self):
        self.data_feeder.release()
        cv2.destroyAllWindows()

    def send_data(self, data):
        centroid = (data[0] + int(data[2]/2), data[1] + int(data[3]/2))
        self.vision_yaw_pub.publish(centroid[0])
        self.vision_depth_pub.publish(centroid[1])

if __name__ == "__main__":
    pipeline = VisionPipeline()
    while not rospy.is_shutdown():
        if(pipeline.active):
            pipeline.feed_data(0)
            pipeline.run_pipeline()
            pipeline.destroy_objects()