class Object:
    def __init__(self, coords, text, interactions):
        self._coords = coords
        self._text = text
        self._interactions = interactions

    def get_coords(self):
        return self._coords

    def get_text(self):
        return self._text

    def get_interactions(self):
        return self._interactions

    def set_coords(self, coords):
        self._coords = coords

    def set_text(self, text):
        self._text = text

    def set_interactions(self, interactions):
        self._interactions = interactions


class Text:
    def __init__(self, content, coords, object):
        self._content = content
        self._coords = coords
        self._object = object

    def get_content(self):
        return self._content

    def get_coords(self):
        return self._coords

    def get_object(self):
        return self._object

    def set_content(self, content):
        self._content = content

    def set_coords(self, coords):
        self._coords = coords

    def set_object(self, object_):
        self._object = object_


class Interaction:
    def __init__(self, coords, object, interaction_type):
        self._coords = coords
        self._object = object
        self._interaction_type = interaction_type

    def get_coords(self):
        return self._coords

    def get_object(self):
        return self._object

    def get_interaction_type(self):
        return self._interaction_type

    def set_coords(self, coords):
        self._coords = coords

    def set_object(self, object_):
        self._object = object_

    def set_interaction_type(self, interaction_type):
        self._interaction_type = interaction_type