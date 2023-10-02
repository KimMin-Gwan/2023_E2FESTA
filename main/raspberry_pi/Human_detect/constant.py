#PATH_TO_MODEL='D:/2023_E2FESTA/main/raspberry_pi/object_detect/model/mobile_SSD_v2_320x320_kr_ob.tflite'   # Path to .tflite model file
#PATH_TO_LABEL='D:/2023_E2FESTA/main/raspberry_pi/object_detect/model/labelmap.txt'   # Path to labelmap.txt file
import platform
import cv2

PATH_TO_MODEL = "/home/pi/2023_E2FESTA/main/raspberry_pi/Human_detect/model/"
MODEL = "mobilenet_ssd_v2_coco_quant_postprocess.tflite"
TPU_MODEL = "mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite"
PATH_TO_LABEL = "/home/pi/2023_E2FESTA/main/raspberry_pi/Human_detect/model/coco_labels.txt"

EDGETPU = True

MIN_CONF_THRESHOLD = 0.5  # 최소값
SELECT_OBJ = "person"  # 타겟
TOP_K = 5  # 보여주는 오브젝트 갯수
FONT =cv2.FONT_HERSHEY_SIMPLEX
MIN_COUNT = 30

EDGETPU_SHARED_LIB = {
  'Linux': 'libedgetpu.so.1',
  'Darwin': 'libedgetpu.1.dylib',
  'Windows': "edgetpu.dll"
}[platform.system()]

DIST_THRESHOLD = 2000
WARN_THRESHOLD = 1500
DANG_THRESHOLD = 1000
STOP_THRESHOLD = 500

VIB_PIN = 17

VIB_CYCLE = 2
