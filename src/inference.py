import os 

import numpy as np
import cv2
import matplotlib.pyplot as plt

from ultralytics import YOLO
from ultralytics.engine.results import Results


BEST_MODEL_PATH = "runs/detect/train/weights/best.pt"

if not os.path.exists(BEST_MODEL_PATH):
    raise FileNotFoundError("Model not found. Please check the model path.")
    
model = YOLO(BEST_MODEL_PATH)

def inference(img_path: str) -> np.ndarray:
    results = model.predict(img_path)

    img_with_preds = results[0]

    return img_with_preds

def plot_img_result(img_with_preds: Results) -> None:
    plt.imshow(cv2.cvtColor(img_with_preds.plot(), cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()