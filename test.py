import torch
from PIL import Image

def load_model():
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')  
    model.conf = 0.80
    return model

model = load_model()

image = "yeye.jpg"

results = model(image)

print(results.pandas().xyxy[0])