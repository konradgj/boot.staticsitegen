from htmlnode import HTMLNode


class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag, value, None, props)

    def toHTML(self):
        if self.value == None:
            raise ValueError("Leaf nodes must have a value")
        if self.tag == None:
            return self.value
        start = f"<{self.tag}{self.propsToHTML()}>"
        end = f"</{self.tag}>"
        return start + f"{self.value}" + end
