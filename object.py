class Object:
    def __init__(self, label = None, coords = None, text = [], interactions = [], container = None):
        self.coords = coords
        self.text = text
        self.interactions = interactions
        self.label = label
        self.container = container

    def get_coords(self):
        return self.coords

    def get_text(self):
        return self.text

    def get_interactions(self):
        return self.interactions
    
    def get_label(self):
        return self.label
    
    def get_container(self):
        return self.container

    def set_coords(self, coords):
        self.coords = coords

    def set_text(self, text):
        self.text = text

    def set_interactions(self, interactions):
        self.interactions = interactions

    def set_label(self, label):
        self.label = label

    def set_container(self, container):
        self.container = container

    def add_text(self, text):
        if not self.text:
            self.text = []
        self.text.append(text)

    def add_interaction(self, interaction):
        if not self.interactions:
            self.interactions = []
        self.interactions.append(interaction)

    def text_to_dict(self):

        if self.text is None:
            self.text = []

        dict = {}

        for t in self.text:
           
            if t.get_content() in dict:
                dict[t.get_content()].append(t.get_coords())
            else:
                dict[t.get_content()] = t.get_coords()

        return dict
    
    def interactions_to_dict(self):

        if self.interactions is None:
            self.interactions = []

        dict = {}

        for t in self.interactions:

            if t.get_interaction_type() in dict:
                dict[t.get_interaction_type()].append(t.get_coords())
            else:
                
                dict[t.get_interaction_type()] = t.get_coords()

        return dict


class Text:
    def __init__(self, content = "", coords = [], object = None):
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
    def __init__(self, coords = None, object = None, interaction_type = None, text = None):
        self.coords = coords
        self.object = object
        self.interaction_type = interaction_type
        self.text = text

    def get_coords(self):
        return self.coords

    def get_object(self):
        return self.object

    def get_interaction_type(self):
        return self.interaction_type
    
    def get_text(self):
        return self.text

    def set_coords(self, coords):
        self.coords = coords

    def set_object(self, object):
        self.object = object

    def set_interaction_type(self, interaction_type):
        self.interaction_type = interaction_type

    def set_text(self, text):
        self.text = text

class Container:

    def __init__(self, layer = None, label = None, object = None):
        self.layer = layer
        self.label = label
        self.object = object

    def get_layer(self):
        return self.layer
    
    def get_label(self):
        return self.label
    
    def get_object(self):
        return self.object
    
    def set_layer(self, layer):
        self.layer = layer

    def set_label(self, label):
        self.label = label

    def set_object(self, object):
        self.object = object