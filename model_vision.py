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
from shapely.geometry import Polygon

class Vision:
    
    def __init__(self, model):
        self.model = model = YOLO(model, task="detect")
        print(self.model.names)
        
    def start_vision(self, num):

        logging.getLogger('ultralytics').setLevel(logging.WARNING)

        sct = mss()
        monitors = sct.monitors
        monitor = monitors[num]

        labels = self.model.names
        labels = list(labels.values())

        label_objects = {label: "" for label in labels}

        try: 
            for label_object in label_objects:

                with open("label_discribtion.json", "r") as f:
                    json_data = json.load(f)

                label_objects[label_object] = json_data[label_object]
        except:
            print(f"Die Labels in discribtion.json sind entweder falsch geschrieben oder stimmen nicht mit dem des Models überein. Das sind die gültigen Label: {labels}")


    
        while True:
            
            screen = np.array(sct.grab(monitor))
            screen = screen[:, :, :3]
            results = self.model(screen)

            data = {label: [] for label in self.model.names.values()}

            for result in results:
                for box in result.boxes:

                    label = self.model.names[int(box.cls)]

                    data[label].append(box.xyxy.tolist()[0])

            obj_label = []

            for key in label_objects:

                if label_objects[key] == "Object":

                    obj_label.append(key)

            objects = []

            for label in obj_label:

                for coords in data[label]:

                    obj = object.Object(label=label, coords=coords)
                    objects.append(obj)

            property_labels = []

            for key in label_objects:

                if label_objects[key] == "Property":

                    property_labels.append(key)

            intersections = {}

            for property in property_labels:

                property_coords = data[property]

                for coords in property_coords:

                    for obj in objects:

                        intersections[self.calculate_intersection(coords, obj.get_coords())] = [property, obj]
            
            sorted_keys = sorted(intersections, reverse=True)

            i = 0

            for key in sorted_keys:

                intersections[key][1].set_property(intersections[key][0])

                if i == len(property_labels)-1:

                    break  

                i+=1

            
            for obj in objects:

                if obj.get_property() == "toplayer":

                    for key in data:

                        if label_objects[key] == "Interaction":

                            for coords in data[key]:

                                if self.is_box_inside_box(coords, obj.get_coords()):

                                    interaction = object.Interaction(coords=coords, object=obj, interaction_type=1)

                                    obj.add_interaction(interaction)

                                    data[key].remove(coords)

                        if label_objects[key] == "Text":

                            for coords in data[key]:

                                if self.is_box_inside_box(coords, obj.get_coords()):

                                    text = object.Text(coords=coords, object=obj)

                                    obj.add_text(text)

                                    data[key].remove(coords)

            for obj in objects:

                if obj.get_property() == "bottomlayer":

                    for key in data:

                        if label_objects[key] == "Interaction":

                            for coords in data[key]:

                                if self.is_box_inside_box(coords, obj.get_coords()):

                                    interaction = object.Interaction(label=key, coords=coords, object=obj, interaction_type=1)

                                    obj.add_interaction(interaction)

                                    data[key].remove(coords)

                        if label_objects[key] == "Text":

                            for coords in data[key]:

                                if self.is_box_inside_box(coords, obj.get_coords()):

                                    text = object.Text(coords=coords, object=obj)

                                    obj.add_text(text)

                                    data[key].remove(coords)

            
            del json_data

            json_data = []

            i = 0

            data_dict = {"Object": []}

            for obj in objects:

                temp_dict = {"index": f"{obj.get_label()}_{i}",
                             "label": obj.get_label(),
                             "property": obj.get_property(),
                             "coords": obj.get_coords(),
                             "textes": obj.num_of_text(),
                             "interactions": obj.interactions_to_list()
                            }
                
                data_dict["Object"].append(temp_dict)

                i+=1

            with open("view_output.json", "w") as f:

                json.dump(data_dict, f, indent=4)
    

    def contains_key(self, data, outer_key, search_key):
        if outer_key in data:
    
            inner_dict = data[outer_key]
            if search_key in inner_dict[0]:
                return True
        return False
    
                            
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
    
    def calculate_intersection(self, box1, box2):

        try:
            rect_1 = self.convert_xyxy_to_xyxyxyxy(coords=box1)
            rect_2 = self.convert_xyxy_to_xyxyxyxy(coords=box2)

            rect_1 = Polygon(rect_1)
            rect_2 = Polygon(rect_2)

            poly_intersection = rect_1.intersection(rect_2)

            return poly_intersection.area
        
        except:

            return 0

    def convert_xyxy_to_xyxyxyxy(self, coords):
        """Korrigiere die Reihenfolge der Punkte, um ein valides Polygon zu erstellen"""
        coords_1 = (coords[0], coords[1])  # (x1, y1)
        coords_2 = (coords[2], coords[1])  # (x2, y1)
        coords_3 = (coords[2], coords[3])  # (x2, y2)
        coords_4 = (coords[0], coords[3])  # (x1, y2)

        return_coords = [coords_1, coords_2, coords_3, coords_4]

        return return_coords
    
    def is_box_inside_box(self, box1, box2):

        x1, y1, x2, y2 = box1

        middle_x = (x2 + x1) / 2
        middle_y = (y2 + y1) / 2

        if middle_x > box2[0] and middle_x < box2[2]:

            if middle_y > box2[1] and middle_y < box2[3]:

                return True
            
        return False
        

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

vision = Vision("Computer_Vision_1.5.3.onnx")
vision.start_vision(2)
    

