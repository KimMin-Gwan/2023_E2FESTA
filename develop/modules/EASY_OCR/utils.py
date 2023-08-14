from matplotlib import pyplot as plt
from imutils.perspective import four_point_transform
from imutils.contours import sort_contours
import imutils
from easyocr import Reader
import cv2
import requests
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import time
import copy
import pickle
import torch
px=[-1,1,1,-1]
py=[-1,-1,1,1]
