import cv2
import numpy as np
from DB import Database
import os

path = ""  # Add images dataset full path
DB = Database()

path, dirs, images = next(os.walk(path))
file_count = len(images)


