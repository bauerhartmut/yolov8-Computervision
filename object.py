class Object:
    def __init__(self, label = None, coords = None, text = None, interactions = None):
        self.coords = coords
        self.text = text
        self.interactions = interactions
        self.label = label

    def get_coords(self):
        return self.coords

    def get_text(self):
        return self.text

    def get_interactions(self):
        return self.interactions
    
    def get_label(self):
        return self.label

    def set_coords(self, coords):
        self.coords = coords

    def set_text(self, text):
        self.text = text

    def set_interactions(self, interactions):
        self.interactions = interactions

    def set_label(self, label):
        self.label = label



class Text:
    def __init__(self, content = None, coords = None, object = None):
        self.content = content
        self.coords = coords
        self.object = object

    def get_content(self):
        return self.content

    def get_coords(self):
        return self.coords

    def get_object(self):
        return self.object

    def set_content(self, content):
        self.content = content

    def set_coords(self, coords):
        self.coords = coords

    def set_object(self, object):
        self.object = object


class Interaction:
    def __init__(self, coords = None, object = None, interaction_type = None):
        self.coords = coords
        self.object = object
        self.interaction_type = interaction_type

    def get_coords(self):
        return self.coords

    def get_object(self):
        return self.object

    def get_interaction_type(self):
        return self._interactiontype

    def set_coords(self, coords):
        self.coords = coords

    def set_object(self, object):
        self.object = object

    def set_interaction_type(self, interaction_type):
        self.interaction_type = interaction_type