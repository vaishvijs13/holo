import cv2
import torch
from ultralytics import YOLO
import numpy as np
from deep_sort_realtime.deepsort_tracker import DeepSort

class ObjectDetector:
    # good practices
    def __init__(self, model_path="yolov8n.pt"): # change later
        self.model = YOLO(model_path)
        self.tracker = DeepSort(max_age=30, n_init=3, nms_max_overlap=1.0) # using deep SORT

    def detect(self, frame):
        results = self.model(frame)
        return results

    def b_boxes(self, frame, results):
        detections = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                label = result.names[class_id]
                detections.append([x1, y1, x2, y2, confidence, class_id]) # store for obj tracking
        
        detections = np.array(detections) if detections else np.empty((0, 6)) # need to check if empty before passing thru deep SORT
        tracked_obj = self.tracker.update(detections)

        for track_id, bbox, conf, _ in tracked_obj:
            x1, y1, x2, y2 = map(int, bbox)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"ID {track_id}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return frame

    def run(self):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            results = self.detect(frame)
            frame = self.b_boxes(frame, results)
            cv2.imshow("HOLO", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = ObjectDetector()
    detector.run()
