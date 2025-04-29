import roboflow


rf = roboflow.Roboflow(api_key="dHpx1mGHqd4JK1WM8KRf")  # replace with your API key
project = rf.workspace("chess-piece-detection-lydqy").project("chess-piece-detection-5ipnt")
model = project.version(3).model

# # Run a prediction
# prediction = model.predict("your_image.jpg", confidence=40, overlap=30).json()


# rf = roboflow.Roboflow(api_key="dHpx1mGHqd4JK1WM8KRf")
# project = rf.workspace().project("chess-piece-detection-5ipnt")
# model = project.version("3").model

# rf = roboflow.Roboflow(api_key="dHpx1mGHqd4JK1WM8KRf")
# model = rf.workspace().project("chess-piece-detection-5ipnt").version("3").model
prediction = model.download(format="yolov8")