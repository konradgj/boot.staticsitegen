from conversion import splitNodes
from textnode import TextNode, TextType


def main():
    node = TextNode("This is text with a `code block` word", TextType.text)
    new_nodes = splitNodes([node], "`", TextType.code)
    print(new_nodes)


main()
