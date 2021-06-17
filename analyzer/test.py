# from imageai.Detection.Custom import CustomObjectDetection
# import os
#
# execution_path = os.getcwd()
#
# prediction = CustomObjectDetection()
# prediction.setModelTypeAsYOLOv3()
# prediction.setModelPath(os.path.join(execution_path, "detection_model-ex-001--loss-0098.050.h5"))
# prediction.setJsonPath(os.path.join(execution_path, "model_class.json"))
# prediction.loadModel()
#
# detections, probabilities = prediction.detectObjectsFromImage(input_image=os.path.join(execution_path, "5.jpg"), output_image_path=os.path.join(execution_path, "5_res.jpg"))
# for detection in detections:
#     print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])