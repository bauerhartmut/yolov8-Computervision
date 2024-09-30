from ultralytics import YOLO
import Containers

model = YOLO("Computer_Vision_1.3.0.onnx")

results = model("Unbenannt.PNG", save=True)

coords_dict = {}

con = Containers.Container()

i = 0

for result in results:
    for box in result.boxes:

        if model.names[int(box.cls)] == "window":
            coords = box.xyxy[0].tolist()

            new_coords = con.convert_xyxy_to_xyxyxyxy(coords=coords)
            coords_dict[f"{model.names[int(box.cls)]}_{i}"] = new_coords
            con.add_coords_dict(coords_dict=coords_dict)
        
            i+=1

container_map = con.create_container_map()
print(container_map)

