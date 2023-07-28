output_directory = '/home/antl/Desktop/model_test/custom_model_lite'
last_model_path = '/home/antl/Desktop/model_test/training'
pipeline_file = '/home/antl/Desktop/model_test/models/mymodel/pipeline_file.config'

"""
import os
import sys
os.system(f"python3 /home/antl/Desktop/model_test/models/research/object_detection/export_tflite_graph_tf2.py \
            --trained_checkpoint_dir {last_model_path} \
            --output_directory {output_directory} \
            --pipeline_config_path {pipeline_file}")
"""
# Convert exported graph file into TFLite model file
import tensorflow as tf

converter = tf.lite.TFLiteConverter.from_saved_model('/home/antl/Desktop/model_test/custom_model_lite/saved_model')
tflite_model = converter.convert()

with open('/home/antl/Desktop/model_test/custom_model_lite/detect.tflite', 'wb') as f:
    f.write(tflite_model)