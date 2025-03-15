from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
    text = "text"
    bold = "bold"
    italic = "italic"
    code = "code"
    link = "link"
    image = "image"


class TextNode:
    def __init__(self, text, textType: TextType, url=None) -> None:
        self.text = text
        self.textType = textType
        self.url = url

    def __eq__(self, obj: object, /) -> bool:
        if self.__dict__ == obj.__dict__:
            return True
        return False

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.textType.value}, {self.url})"

    def toHTMLNode(self):
        match self.textType:
            case TextType.text:
                return LeafNode(None, self.text.replace("\n", " "))
            case TextType.bold:
                return LeafNode("b", self.text)
            case TextType.italic:
                return LeafNode("i", self.text)
            case TextType.code:
                return LeafNode("code", self.text)
            case TextType.link:
                return LeafNode("a", self.text, {"href": self.url})
            case TextType.image:
                return LeafNode("img", "", {"src": self.url, "alt": self.text})
