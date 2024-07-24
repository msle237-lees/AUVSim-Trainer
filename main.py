from ultralytics import YOLO

model = YOLO('yolov8n.pt')

results = model.train(
    data='machine_vision/data.yaml',
    imgsz=640,
    epochs=200,
    batch_size=8
)