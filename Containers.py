class Container:

    def __init__(self, coords_dict=None):
        
        if coords_dict is not None:
            corner_coords_dict = {}
            for key, coords in coords_dict.items():
                #fügt alle 4 eckpunkte zu den boundingboxes hinzu
                #coords_1 ist oben links, coords_2 ist unten rechts, coords_3 ist oben rechts und coords_4 unten links
                coords_1 = coords[0], coords[1]
                coords_2 = coords[2], coords[3]
                coords_3 = coords[2], coords[1]
                coords_4 = coords[0], coords[3]

                corners = [coords_1, coords_2, coords_3, coords_4]
                corner_coords_dict[key] = corners

            self.coords_dict = corner_coords_dict

        self.coords_dict = coords_dict

    def get_coords(self):
        return self.coords_dict
    
    def set_coords(self, coords_dict):
        """achtung hier muss auf die formatierung geachtet werden sonst fickst du das programm
        gleiche formatierung wie in dem konstruktor"""
        self.coords_dict = coords_dict

    def add_coords_dict(self, coords_dict):
        """achtung hier muss auf die formatierung geachtet werden sonst fickst du das programm
        gleiche formatierung wie in dem konstruktor"""
        if self.coords_dict is None:
            self.coords_dict = {} 
        self.coords_dict.update(coords_dict)

    def convert_xyxy_to_xyxyxyxy(self, coords):
        """Bitte nur vierecke mit winkel von 90° sonst bist du blöd"""
        coords_1 = (coords[0], coords[1])
        coords_2 = (coords[2], coords[3])
        coords_3 = (coords[2], coords[1])
        coords_4 = (coords[0], coords[3])

        return_coords = [coords_1, coords_2, coords_3, coords_4]

        return return_coords
    

    def create_container_map(self):
        """bitte zuerst container hinzufügen"""

        coords_dict = self.coords_dict
        corner_dict = {}
        layers = {"Toplayer": [], "Bottomlayer": []}

        for key, corners in coords_dict.items():
            for key1, corners1 in coords_dict.items():
                corner_1 = corner_2 = corner_3 = corner_4 = False

                if corners1[0][0] > corners[0][0] and corners1[0][1] > corners[0][1]:
                    corner_1 = True
                if corners1[1][0] < corners[1][0] and corners1[1][1] < corners[1][1]:
                    corner_2 = True
                if corners1[2][0] < corners[2][0] and corners1[2][1] > corners[2][1]:
                    corner_3 = True
                if corners1[3][0] > corners[3][0] and corners1[3][1] < corners[3][1]:
                    corner_4 = True

                corner_list = (corner_1, corner_2, corner_3, corner_4)

                # Stelle sicher, dass wir die Fenster nur einmal hinzufügen
                if key not in corner_dict:  # Verhindert Duplikate
                    corner_dict[key] = (key1, corner_list)

        # Hinzufügen der Fenster zu den Schichten
        for key, (key1, corner_list) in corner_dict.items():
            if not any(corner_list):  # Wenn alle Ecken False sind, in Toplayer
                toplayer = {key: coords_dict[key]}
                layers["Toplayer"].append(toplayer)
            else:  # Wenn eine Ecke True ist, in Bottomlayer
                bottomlayer = {key: coords_dict[key]}
                layers["Bottomlayer"].append(bottomlayer)

        return layers

    
