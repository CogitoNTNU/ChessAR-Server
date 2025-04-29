import roboflow

rf = roboflow.Roboflow(api_key="dHpx1mGHqd4JK1WM8KRf")
model = rf.workspace().project("chessar-4kns8").version("2").model
prediction = model.download()