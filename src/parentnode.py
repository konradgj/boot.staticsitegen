from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag=tag, children=children, props=props)

    def toHTML(self):
        if self.tag == None:
            raise ValueError("missing tag")
        if self.children == None:
            raise ValueError("missing children")
        if len(self.children) == 0:
            raise ValueError("children list empty")
        mid = ""
        for child in self.children:
            mid += child.toHTML()
        start = f"<{self.tag}{self.propsToHTML()}>"
        end = f"</{self.tag}>"
        return start + mid + end
