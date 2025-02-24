from enum import Enum


class TextType(Enum):
    normal = "normal"
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
