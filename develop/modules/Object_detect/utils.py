import cv2
import numpy as np

class Bbox_maker:
    def __init__(self, labels):
        print("bbox maker ready")
        self.labels = labels
    
    # bbox making
    def make_bbox(self, frame, score, bbox, class_name):
        cv2.rectangle(frame, (bbox["xmin"], bbox["ymin"]), 
                      (bbox["xmax"], bbox["ymax"]), (10, 255, 0), 2)
        # get label
        object_name = self.labels[int(class_name)]
        accuracy = int(score *100)
        label = f'{object_name} : {accuracy}'
        labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        label_ymin = max(bbox['ymin'], labelSize[1] + 10)
        cv2.rectangle(frame, (bbox['xmin'], label_ymin-labelSize[1]-10),
                        (bbox['xmin']+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
        cv2.putText(frame, label, (bbox['xmin'], label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text
        return frame


    
class Image_Manager:
    def __init__(self, tool, labels):
        self.frame = None # 3차원 행렬
        self.tool = tool  # 지울 고려해야됨
        self.bbox_manager = Bbox_maker(labels)

        self.width = 0
        self.height = 0
        self.init_flag = False
        
    # 이번 루프에서 프레임 특징
    def recog_image(self, frame):
        self.frame = frame
        # 최초에 한번만 연산
        if not self.init_flag:
            self.height, self.width, _ = frame.shape
            self.init_flag == True
            
        return self.height, self.width
        
    # 해석기에 넣을 행렬 형태로 변환 (3차원 -> 4차원)
    def make_input_data(self):
        width, height = self.tool.get_tensor_size()
        rgb_image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        image_resized = cv2.resize(rgb_image, (width, height))
        input_data = np.expand_dims(image_resized, axis = 0) # 4차원 행렬로 재배치
        return input_data
    
    # bbox 만들기
    def make_bbox(self, score, bbox, class_name):
        self.frame = self.bbox_manager.make_bbox(self.frame, score, bbox, class_name)
        return
    
    def show_test_window(self):
        cv2.imshow('test_window', self.frame)
        return

    def get_bboxed_frame(self):
        return self.frame
    
        
        
    