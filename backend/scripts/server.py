import cv2
import numpy as np
import base64
from flask import Flask, request, jsonify
from objdetector import ObjectDetector

app = Flask(__name__)
detector = ObjectDetector()
tracked_objects = {}

def decode_img(image_data):
    img_bytes = base64.b64decode(image_data)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

@app.route("/track", methods=["POST"])
def track_objects():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    file = request.files["image"]
    np_img = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    image = decode_img(data["image"])
    results = detector.detect(image)
    frame = image.copy()  # copy image so og does not get edited
    frame = detector.b_boxes(frame, results)

    tracking_data = {}
    for track_id, bbox, conf, _ in detector.tracker.tracked_objects:
        x1, y1, x2, y2 = map(int, bbox)
        center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2

        tracking_data[str(track_id)] = {
            "id": track_id,
            "confidence": round(conf, 2),
            "bounding_box": {"x": x1, "y": y1, "width": x2 - x1, "height": y2 - y1},
            "position": {"x": center_x / 1000.0, "y": center_y / 1000.0}  # ARKit scale
        }

    return jsonify({"tracked_objects": tracking_data})

@app.route("/unity-track", methods=["POST"])
def receive_unity_data():
    data = request.get_json()

    if "object_name" not in data or "position" not in data:
        return jsonify({"error": "Invalid data format"}), 400

    object_name = data["object_name"]
    position = data["position"]

    tracked_objects[object_name] = position

    print(f"Received object from Unity: {object_name} at {position}")
    return jsonify({"status": "success", "tracked_objects": tracked_objects})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)