from ultralytics import YOLO

model = YOLO("yolov26s.pt")

model.train(
    data="dataset/data.yaml",

    epochs=50,          
    imgsz=960,          
    batch=16,           
    device="cuda",
    workers=2,
    patience=10,

    close_mosaic=10,
    mosaic=1.0,

    hsv_h=0.01,
    hsv_s=0.5,
    hsv_v=0.3,
    scale=0.3,
    fliplr=0.5
)