#Import YOLO pre-trained AI Model that is used to classify animals in images.
from ultralytics import YOLO

#Load pre-trained YOLO model and store as model
model = YOLO('yolov8x.pt')

#Detect animal in image
results = model('/Users/christoffeljansevanvuuren/Desktop/VSCode/Assignment3/Multiple_Animal_Test_Image.webp')

for result in results:
    print(result.boxes)
    result.show()