from ultralytics import YOLO
from pathlib import Path
import torch


def run_inference(input_path, output_path,threshold=0.5, display_mode= None,category_filter=None): #display mode and categpry_fiulter will be done later 
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)  # Create the output directory if it doesn't exist
    model = YOLO('yolo26m-seg.pt')
    predic_args = {
        'source': input_path,
        'device': 'cuda' if torch.cuda.is_available() else 'cpu',
        'conf': threshold,

    }
    results = model(**predic_args)  # Run inference on the input image or video using GPU
    # for result in results:
    #     # Save the results to the specified output directory
    #     class_names = result.names  # Get the class names from the result
    #     predicted_classes = result.boxes.cls.tolist()  # Get the predicted class names for each detected object
    #     predicted_scores = result.boxes.conf.tolist()  # Get the predicted scores for each detected object
    #     data = {}
    #     for cls, score in zip(predicted_classes, predicted_scores):
    #         class_name = class_names[int(cls)]  # Get the class name using the class index
    #         data[class_name] = score  # Store the class name and its corresponding score in the data dictionary
    
    # print(data)
    # return data  # Return the data dictionary containing class names and scores
    for r in results:
        if r.boxes is not None and len(r.boxes) >0:
            # Save preditced image with bounding boxes
            r.save(f'{output_path}/{input_path.name}')
            predicted_classes = r.boxes.cls.tolist()
            predicted_scores = r.boxes.conf.tolist()  
            class_names = r.names  #
            detections = []
            for object in predicted_classes:
                if object in class_names:
                    detections.append(class_names[object])
            #make a dictionary to return the results
            data = {
                'message': 'Inference completed successfully.',
                'labels': detections,
                'scores': predicted_scores,
                'total_objects_detected': len(r.boxes),
                'class_counts' : len(detections),
                'config': {
                    'threshold': threshold,
                    # 'display_mode': display_mode, 
                    # 'category_filter': category_filter,
                }
            }
            print('Inference Completed successfully')
            return data

        
        else:
            data = {
                'message': 'No objects detected in the input image or video.',
                'labels': [],
                'scores': [],
                'total_objects_detected': 0,
                'class_counts': 0,
                'config': {
                    'threshold': threshold,
                    # 'display_mode': display_mode, 
                    # 'category_filter': category_filter,
                }
            }
            print('no successful inference')
            return data