import cv2
import numpy as np
from os.path import dirname, abspath
import sys

'''
The following params need to be provided 
    names
    weights
    config
'''
class Detector:

    def __init__(self, **kwargs):
        self.names = kwargs['names']
        self.weights = kwargs['weights']
        self.config = kwargs['config']

        self.classes = []

        self.init()

    def tap(self, v):
        print(v)
        return v

    def resolveFilePath(self, name):
        return f'{dirname(abspath(__file__))}/{name}'

    def init(self):
        # self.net = cv2.dnn.readNet(file("config/yolov3_custom_4000.weights"), file("config/yolov3_custom.cfg"))
        self.network = cv2.dnn.readNet(self.resolveFilePath(self.weights), self.resolveFilePath(self.config))

        if(self.names):
            with open(self.resolveFilePath(self.names), "r") as f:
                self.classes = [line.strip() for line in f.readlines()]
        else:
            print("No names provided")

        
        self.layer_names = self.network.getLayerNames()
        self.output_layers = [self.layer_names[i[0] -1] for i in self.network.getUnconnectedOutLayers()]


    def imageToBytes(self, img):
        is_success, im_buf_arr = cv2.imencode(".jpg", img)
        byte_im = im_buf_arr.tobytes()
        return byte_im

    def detect(self, img_stream):
        img = np.fromstring(img_stream, dtype='uint8')
        img = cv2.imdecode(img, 1)
        img = cv2.resize(img, None, fx=0.8 ,fy=0.8)

        height, width, channels = img.shape

        # object detection
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.network.setInput(blob)
        outs = self.network.forward(self.output_layers)

        # showing information on screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.2:
                    # Object Detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # cv2.circle(img, (center_x, center_y), 10, (0, 255,0), 2)
                    # Bouding Boxes
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # number_objects_detected = len(boxes)
        # removing double labels
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        idx = 100
        # print(indexes)
        font = cv2.FONT_HERSHEY_SIMPLEX

        images = dict()
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(self.classes[class_ids[i]])

                # Cropping and saving ROI
                new_img = img[y:y + h, x:x + w]

                
                images[f'p{str(idx)}'] = self.imageToBytes(new_img)
                # cv2.imwrite('LicensePlates//' + 'p' + str(idx) + '.png', new_img)  # stores the new image
                idx += 1

                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # cv2.putText(img, label,(x,y -30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),1)
                # cv2.putText(img, "License Plate", (x,y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0),2)

        # cv2.imwrite("Detection.png", img)
        images['detection'] =  self.imageToBytes(img)
        
        return images

    def writeToFile(self, path, data):
        with open(path, 'wb') as f:
            f.write(data)
            f.close()
#loading yolo
# net = cv2.dnn.readNet(file("config/yolov3_custom_4000.weights"), file("config/yolov3_custom.cfg"))
# net = cv2.dnn.readNet("config\yolov4-obj_4000.weights", "config\olov4-obj.cfg")

# classes = []

# with open(file("config/model.names"), "r") as f:
#     classes = [line.strip() for line in f.readlines()]
#     print(classes)



# det = Detector(
#     weights='../config/yolov3_custom_4000.weights',
#     config='../config/yolov3_custom.cfg',
#     names='../config/model.names'
# )

# images = det.detect(sys.argv[1])

# print(images.keys)
