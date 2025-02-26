from htmlnode import HTMLNode
from textnode import TextNode, TextType


def main():
    tn = TextNode("dummy text", TextType.bold, "https://www.boot.dev")
    print(tn)

    test = HTMLNode(
        props={
            "href": "https://www.google.com",
            "target": "_blank",
        }
    )

    print(test)


main()
