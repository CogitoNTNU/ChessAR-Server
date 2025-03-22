from ultralytics import YOLO
import matplotlib.pyplot as plt
import numpy as np

def train_edge_detection_yolo() -> None:
    model = YOLO('yolo11n.pt')  # Load the model
    model.train(
        data='datasets/data.yaml',
        epochs=5,
        imgsz=640
    )

def run_edge_detection_yolo(model_path: str, image_path: str) -> None:
    model = YOLO(model_path)  # Load the model
    results = model.predict(source=image_path)

    test_image = results[0].plot(line_width=2)
    plt.imshow(test_image)

    plt.savefig('edge_result.png')


if __name__ == '__main__':
    # train_edge_detection_yolo()
    run_edge_detection_yolo('train3/weights/best.pt', 'test_images/image1.jpg')