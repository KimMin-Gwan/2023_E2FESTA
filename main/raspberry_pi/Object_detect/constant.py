#PATH_TO_MODEL='D:/2023_E2FESTA/main/raspberry_pi/object_detect/model/mobile_SSD_v2_320x320_kr_ob.tflite'   # Path to .tflite model file
#PATH_TO_LABEL='D:/2023_E2FESTA/main/raspberry_pi/object_detect/model/labelmap.txt'   # Path to labelmap.txt file
import platform

PATH_TO_MODEL = "/home/pi/2023_E2FESTA/main/raspberry_pi/Object_detect/model/"
MODEL = "mobile_SSD_v2_320x320_kr_ob.tflite"
TPU_MODEL = "mobile_SSD_v2_320x320_kr_ob_edgetpu.tflite"
PATH_TO_LABEL = "/home/pi/2023_E2FESTA/main/raspberry_pi/Object_detect/model/labelmap.txt"

EDGETPU = False

MIN_CONF_THRESHOLD = 0.2
INPUT_MEAN = 127.5
INPUT_STD = 127.5

EDGETPU_SHARED_LIB = {
  'Linux': 'libedgetpu.so.1',
  'Darwin': 'libedgetpu.1.dylib',
  'Windows': "edgetpu.dll"
}[platform.system()]

DIST_THRESHOLD = 3000
WARN_THRESHOLD = 2000
DANG_THRESHOLD = 1200
STOP_THRESHOLD = 500

VIB_PIN = 17

VIB_CYCLE = 2
