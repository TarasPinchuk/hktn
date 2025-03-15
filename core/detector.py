from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image


model = None


def load_model():
    global model
    if model is None:
        model = YOLO('yolov8n.pt')
    return model


def detect_objects(image, output_path):
    model = load_model()
    results = model.predict(source=image)
    detections = []
    if results:
        result = results[0]
        boxes = result.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            try:
                class_name = model.names[cls_id]
            except AttributeError:
                class_name = model.model.names[cls_id]
            detections.append({
                "class": class_name,
                "confidence": round(conf, 3),
                "bbox": [x1, y1, x2, y2]
            })
    else:
        detections = []

    if isinstance(image, Image.Image):
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    elif isinstance(image, np.ndarray):
        image_cv = image.copy()
    else:
        image_cv = cv2.imread(str(image))
    for det in detections:
        x1, y1, x2, y2 = det["bbox"]
        class_name = det["class"]
        conf = det["confidence"]
        cv2.rectangle(image_cv, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"{class_name} {conf:.2f}"
        cv2.putText(image_cv, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.imwrite(output_path, image_cv)
    return detections
