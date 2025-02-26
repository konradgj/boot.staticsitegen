from enum import Enum

from htmlnode import HTMLNode


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
                return HTMLNode(None, self.text)
            case TextType.bold:
                return HTMLNode("b", self.text)
            case TextType.italic:
                return HTMLNode("i", self.text)
            case TextType.code:
                return HTMLNode("code", self.text)
            case TextType.link:
                return HTMLNode("a", self.text, None, {"href": self.url})
            case TextType.image:
                return HTMLNode("img", "", None, {"src": self.url, "alt": self.text})
