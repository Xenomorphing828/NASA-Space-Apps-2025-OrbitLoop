import os
import cv2
import time
from ultralytics import YOLO

def find_trained_model():
    print("🔍 Searching for trained model...")
    
    possible_paths = [
        # Current directory
        'best.pt',
        'space_debris_model.pt',
        
        # Roboflow download locations
        'space debris detection.v1i.yolov8/best.pt',
        'space-debris-detection-bxlp3-1/best.pt',
        
        # Training output locations
        'runs/detect/train/weights/best.pt',
        'runs/detect/space_debris_v1/weights/best.pt',
        'runs/detect/space_debris/weights/best.pt',
        'runs/detect/train2/weights/best.pt',
        
        # Parent directories
        '../best.pt',
        '../runs/detect/train/weights/best.pt',
        '../../best.pt',
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Found the model: {path}")
            return path
    
    print("Deep searching for model files...")
    home_dir = os.path.expanduser("~")
    for root, dirs, files in os.walk(home_dir):
        for file in files:
            if file == "best.pt" and "detect" in root and "weights" in root:
                model_path = os.path.join(root, file)
                print(f"Found your model: {model_path}")
                return model_path
                
    print("No trained model found. Please train your model first.")
    return None

def check_webcam():
    print("Checking webcam...")
    for i in range(3):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"Webcam found at index {i}")
                cap.release()
                return i
            cap.release()
    print("No webcam detected!")
    return None

def main():
    print("SPACE DEBRIS DETECTOR")
    print("=" * 50)
    
    # Step 1: Find the trained model
    model_path = find_trained_model()
    if model_path is None:
        print("\n💡 To train your model, run:")
        print("   from ultralytics import YOLO")
        print("   model = YOLO('yolov8n.pt')")
        print("   model.train(data='data.yaml', epochs=100, imgsz=640)")
        return
    
    # Step 2: Load the model
    print(f"Loading the space debris model...")
    try:
        model = YOLO(model_path)
        print("The model has been loaded successfully")
        
        if hasattr(model, 'names'):
            print(f"Model detects: {list(model.names.values())}")
    except Exception as e:
        print(f"Error loading the model: {e}")
        return
    
    # Step 3: Check webcam
    camera_index = check_webcam()
    if camera_index is None:
        return
    
    # Step 4: Start detection with the model
    print("\n Starting SPACE DEBRIS detection with the model...")
    print("   Press 'Q' to quit")
    print("   Press 'S' to save screenshot")
    print("-" * 50)
    
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    frame_count = 0
    detection_count = 0
    start_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame")
            break
        
        frame_count += 1
        
        # Run detection with the trained model
        results = model(frame, conf=0.5)  # Confidence threshold
        
        # Display results
        annotated_frame = results[0].plot()
        
        # Count detections
        if len(results[0].boxes) > 0:
            detection_count += 1
        
        # Calculate stats
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time if elapsed_time > 0 else 0
        detection_rate = (detection_count / frame_count) * 100
        
        # Add info overlay
        cv2.putText(annotated_frame, f"FPS: {fps:.1f}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(annotated_frame, f"Detections: {detection_count}", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(annotated_frame, "YOUR TRAINED MODEL - Press 'Q' to quit", (10, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Show class labels if available
        if hasattr(model, 'names'):
            classes_text = "Classes: " + ", ".join(model.names.values())
            cv2.putText(annotated_frame, classes_text, (10, 120), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 255), 1)
        
        cv2.imshow('Space Debris Detection - YOUR TRAINED MODEL', annotated_frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('Q'):
            break
        elif key == ord('s') or key == ord('S'):
            filename = f"my_debris_detection_{int(time.time())}.jpg"
            cv2.imwrite(filename, annotated_frame)
            print(f"Screenshot saved: {filename}")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    
    print("\n Detection completed")
    print(f"Your model processed {frame_count} frames")
    print(f"Debris detections: {detection_count}")
    print(f"Detection rate: {detection_rate:.1f}%")

if __name__ == "__main__":
    main()