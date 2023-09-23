#PATH_TO_MODEL='D:/2023_E2FESTA/main/raspberry_pi/object_detect/model/mobile_SSD_v2_320x320_kr_ob.tflite'   # Path to .tflite model file
#PATH_TO_LABEL='D:/2023_E2FESTA/main/raspberry_pi/object_detect/model/labelmap.txt'   # Path to labelmap.txt file
import platform
PATH_TO_MODEL = "C:/Users/antl/Documents/GitHub/2023_E2FESTA/main/server/Socket_maker/Object_detect/model/"
MODEL = "mobile_SSD_v2_320x320_kr_ob.tflite"
TPU_MODEL = "mobile_SSD_v2_320x320_kr_ob_edgetpu.tflite"
PATH_TO_LABEL = "C:/Users/antl/Documents/GitHub/2023_E2FESTA/main/server/Socket_maker/Object_detect/model/labelmap.txt"

# "C:/Users/antl/Documents/GitHub/2023_E2FESTA/main/server/Socket_maker/Object_detect/model/labelmap.txt"

EDGETPU = False

MIN_CONF_THRESHOLD = 0.2
INPUT_MEAN = 127.5
INPUT_STD = 127.5

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
