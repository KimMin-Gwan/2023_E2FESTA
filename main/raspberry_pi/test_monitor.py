from flask import Flask, render_template, Response
from flask import send_file # 인프라 서치에서 한국어 반환 위해
import cv2, io # 핸드카메라&스냅샷 위해
from Monitoring.constant import SUB,BUS,TRAFT
import Monitoring.monitor
import numpy as np
import Camera.camera_master
import naviUtils.class_Information

if __name__=="__main__":
    camera = Camera.Camera_Master()

    info=naviUtils.class_Information.Information()

    monitor=Monitoring.monitor.Monitor(info=info)
    monitor.start_monitor(camera=camera)