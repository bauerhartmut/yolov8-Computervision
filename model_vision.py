from ultralytics import YOLO
import numpy as np
from mss import mss
from PIL import Image, ImageOps
import json
import time
import logging
import multiprocessing
import pytesseract
import re
import object
import Containers

class Vision:
    
    def __init__(self, model):
        self.model = model = YOLO(model, task="detect")
        
    def start_vision(self):

        logging.getLogger('ultralytics').setLevel(logging.WARNING)

        sct = mss()
        monitor = sct.monitors[1]

        labels = self.model.names
        labels = list(labels.values())

        object_dict = {label: "" for label in labels}

        label_objects = {label: "" for label in labels}

        try: 
            for label_object in label_objects:

                with open("label_discribtion.json", "r") as f:
                    json_data = json.load(f)

                label_objects[label_object] = json_data[label_object]
        except:
            print(f"Die Labels in discribtion.json sind entweder falsch geschrieben oder stimmen nicht mit dem des Models überein. Das sind die gültigen Label: {labels}")

    
        while True:
            
            label_count = {label: 0 for label in labels}
            label_dict = {label: [] for label in labels}
            temp_dict = {label: 0 for label in labels}
            screen = np.array(sct.grab(monitor))
            screen = screen[:, :, :3]
            results = self.model(screen)

            data = {}

            variables = {label: 0 for label in labels}

            container_map = self.create_container_map(results=results, label_objects=label_objects)

            obj_list = []

            for result in results:
                for box in result.boxes:

                    label = self.model.names[int(box.cls)]  
                    coords = box.xyxy[0].tolist()

                    if "Container" in label_objects[label]: 

                        if self.contains_key(container_map, "Toplayer", f"{label}_{temp_dict[label]}"):
                            container = object.Container(layer="Toplayer", label=label)
                        else:
                            container = object.Container(layer="Bottomlayer", label=label)

                        temp_dict[label]+=1
                            
                        if "Object" in label_objects[label]:

                            obj = object.Object(label=label, coords=coords, container=container)
                            container.set_object(object=obj)
                            obj_list.append(obj)

            all_boxes = []

            for result in results:
                for box in result.boxes:
                    box_dict = {}
                    box_dict[self.model.names[int(box.cls)]] = box.xyxy[0].tolist()
                    all_boxes.append(box_dict)

            print(all_boxes)
            

            for obj in obj_list:

                if obj.get_container().get_layer() == "Toplayer":
                    boxes = self.get_boxes_inside_boundingboxes(results=results, coords=obj.get_coords())


                    for boxes_dict in boxes:
                         for key, coords in boxes_dict.items():

                            if "Text" in label_objects[key]:
                                text = object.Text(content=self.read_image(screen, coords=coords), coords=coords, object=obj)
                                obj.add_text(text)


                            if "Interaction" in label_objects[key]:
                                interaction = object.Interaction(coords=coords, object=object, interaction_type=1)
                                obj.add_interaction(interaction)

                            coords_to_remove = coords 
            
                            all_boxes = [box for box in all_boxes if not (key in box and box[key] == coords_to_remove)]

                if obj.get_container().get_layer() == "Bottomlayer":
                    boxes = self.get_boxes_inside_boundingboxes(results=results, coords=obj.get_coords())

                    boxes_to_keep = []  # Liste für die zu behaltenden Boxen

                    for boxes_dict in boxes:
                        for key, coords in boxes_dict.items():
                            if any(key in box and box[key] == coords for box in all_boxes):
                                boxes_to_keep.append(boxes_dict)

                    boxes = boxes_to_keep

                    for boxes_dict in boxes:
                         for key, coords in boxes_dict.items():

                            if "Text" in label_objects[key]:
                                text = object.Text(content=self.read_image(screen, coords=coords), coords=coords, object=obj)
                                obj.add_text(text)


                            if "Interaction" in label_objects[key]:
                                interaction = object.Interaction(coords=coords, object=object, interaction_type=1)
                                obj.add_interaction(interaction)

            for obj in obj_list:
                data[f"{obj.get_label()}_{label_count[obj.get_label()]}"] = [obj.get_container().get_layer(), [obj.text_to_dict()], [obj.interactions_to_dict()]]
                label_count[obj.get_label()]+=1

            with open("view_output.json", "w") as f:
                   json.dump(data, f, indent=5)
            time.sleep(0.1)

    def contains_key(self, data, outer_key, search_key):
        if outer_key in data:
    
            inner_dict = data[outer_key]
            if search_key in inner_dict[0]:
                return True
        return False
    
    def get_boxes_inside_boundingboxes(self, results, coords):

        boxes = []

        for result in results:
            for box in result.boxes:

                if coords == box.xyxy[0].tolist():
                    continue
                else:
                    x1, y1, x2, y2 = box.xyxy[0]

                    middle_x = (x2 + x1) / 2
                    middle_y = (y2 + y1) / 2

                    if coords[0] <= middle_x <= coords[2] and coords[1] <= middle_y <= coords[3]:
                        label = self.model.names[int(box.cls)]
                        if  label not in boxes:
                            box_dict = {}
                            box_dict[label] = box.xyxy[0].tolist()
                            boxes.append(box_dict)
        
        return boxes
                            
    def read_image(self, image, coords):

        pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'  # Tesseract path

        
        # Konvertiere die Koordinaten in Ganzzahlen
        coords = [int(x) for x in coords]
        x1, y1, x2, y2 = coords
            

        try:
            # Füge Puffer hinzu, um das Zuschneiden etwas großzügiger zu machen
            x1 -= 5
            y1 -= 5
            x2 += 5
            y2 += 5

            # Verwende die crop() Methode, um den Bereich des Bildes zu extrahieren
            image = image[y1:y2, x1:x2]
        except Exception as e:
            print(f"Error cropping image: {e}")
            x1, y1, x2, y2 = coords
            image = image[y1:y2, x1:x2]
            pass


        text = pytesseract.image_to_string(image)

        # Bereinige den Text, um nicht druckbare Zeichen zu entfernen
        text = re.sub(r'[^\x00-\x7F]+', '', text)
        text = text.replace('\n', '')

        return text

    def create_container_map(self, results, label_objects):

        i = 0
        con = Containers.Container()

        for result in results:
                for box in result.boxes:

                    label = self.model.names[int(box.cls)]

                    if "Container" in label_objects[label]:

                        obj = object.Object(label=f"{label}_{i}", coords=box.xyxy[0].tolist())
                        i+=1

                        con_dict = {obj.get_label(): con.convert_xyxy_to_xyxyxyxy(obj.get_coords())}

                        con.add_coords_dict(coords_dict=con_dict)

        container_map = con.create_container_map()

        return container_map



class Api:

    def __init__(self) -> None:
        pass

    def get_data(self, label = None):
        with open("view_output.json") as f:
            data = json.load(f)
        
        if not label:
            return data
        else:
            
            new_data = {}

            for key in data:

                if key.split("_")[0] == label:
                    new_data[key] = data[key]
                
                
            return new_data

vision = Vision("Computer_Vision_1.3.0.onnx")
vision.start_vision()
    

