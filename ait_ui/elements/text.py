from .element import Element
class Text(Element):
    def __init__(self,id = None, value = None):
        super().__init__(id, value)
        self.tag = "p"
        self.value_name = "innerHTML"
        