from roboflow import Roboflow
from ultralytics import YOLO
import os

# Download dataset from Roboflow
rf = Roboflow(api_key="FeO2WyC1a98GpYtizM5B")  # Get from Roboflow settings
project = rf.workspace("nsst3gp-9l3x6").project("space-debris-detection-bxlp3")
dataset = project.version(1).download("yolov8")

# Load YOLOv8 model
model = YOLO('yolov8n.pt')  # Use 'yolov8s.pt' for better accuracy

# Train the model
results = model.train(
    data=f'{dataset.location}/data.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    patience=10,
    name='space_debris_v1'
)

print("Training completed! Model saved in runs/detect/space_debris_v1/")