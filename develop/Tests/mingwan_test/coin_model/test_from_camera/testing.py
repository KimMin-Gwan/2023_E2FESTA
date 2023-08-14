import os
import cv2
import numpy as np
import sys
import random
from tensorflow.lite.python.interpreter import Interpreter

# 인터프리터 불러오기
def get_interpreter(model_path):
    interpreter = Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter

def get_labels(lable_path):
    with open(lable_path, 'r') as f:
        labels = [line.strip() for line in f.readlines()]
    return labels

def object_detection(model_path, lblpath, min_conf=0.5, txt_only=False):
    camera = cv2.VideoCapture(0)

    interpreter = get_interpreter(model_path=model_path)
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    float_input = (input_details[0]['dtype'] == np.float32)
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]
    input_mean = 127.5
    input_std = 127.5
    
    labels = get_labels(lblpath)
    
    while True:
        ret, frame = camera.read()
        if ret:
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image_height, image_width, _ = frame.shape # height, width, dim
            image_resized = cv2.resize(image_rgb, (width, height))
            input_data = np.expand_dims(image_resized, axis = 0)
            
            if float_input:
                input_data = (np.float32(input_data) - input_mean) / input_std
                
            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()
            
            
            boxes = interpreter.get_tensor(output_details[1]['index'])[0] # boxes == bbox
            classes = interpreter.get_tensor(output_details[3]['index'])[0] # classes == 4
            scores = interpreter.get_tensor(output_details[0]['index'])[0] # output late
            
            for i in range(len(scores)):
                if ((scores[i] > min_conf) and (scores[i] <= 1.0)):
                    ymin = int(max(1, (boxes[i][0] * image_height)))
                    xmin = int(max(1, (boxes[i][1] * image_width)))
                    ymax = int(min(image_height, (boxes[i][2] * image_height)))
                    xmax = int(min(image_width, (boxes[i][3] * image_width)))
                    
                    # make bbox
                    #print(f'xmin : {xmin}, ymin : {ymin}')
                    #print(f'xmax : {xmax}, ymax : {ymax}')
                    
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)
                    # get label
                    object_name = labels[int(classes[i])]
                    accuracy = int(scores[i] *100)
                    label = f'{object_name} : {accuracy}'
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                    label_ymin = max(ymin, labelSize[1] + 10)
                    cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10),
                                  (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
                    cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text
            if txt_only == False:
                #rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                cv2.imshow('test_window', frame)
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    camera.release()
    cv2.destroyAllWindows()
    
def main():
    #PATH_TO_MODEL='/home/antl/Desktop/model_test/custom_model_lite/detect.tflite'   # Path to .tflite model file
    #PATH_TO_LABELS='/home/antl/Desktop/model_test/labelmap.txt'   # Path to labelmap.txt file

    PATH_TO_MODEL='C:/Users/IT/Documents/GitHub/2023_E2FESTA/develop/Tests/mingwan_test/coin_model/test_from_camera/mobile_SSD_v2_320x320_kr_ob.tflite'
    PATH_TO_LABELS='C:/Users/IT/Documents/GitHub/2023_E2FESTA/develop/Tests/mingwan_test/coin_model/test_from_camera/labelmap.txt'   # Path to labelmap.txt file
    min_conf_threshold=0.2  # Confidence threshold (try changing this to 0.01 if you don't see any detection results)
    object_detection(PATH_TO_MODEL, PATH_TO_LABELS, min_conf_threshold)
    
if __name__ == '__main__':
    main()