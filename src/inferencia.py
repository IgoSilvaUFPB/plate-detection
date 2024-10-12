import os 

import numpy as np
import cv2
import matplotlib.pyplot as plt

from ultralytics import YOLO

BEST_MODEL_PATH = "runs/detect/train2/weights/best.pt"

if not os.path.exists(BEST_MODEL_PATH):
    raise FileNotFoundError("Modelo não encontrado, por favor cheque o caminho do arquivo.")
    
model = YOLO(BEST_MODEL_PATH)

def inferencia(img_path: str) -> np.ndarray:
    resultado = model.predict(img_path)

    imagem_com_pred = resultado[0]

    return imagem_com_pred

def plot_img_result(imagem_com_pred) -> None:
    plt.imshow(cv2.cvtColor(imagem_com_pred.plot(), cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()