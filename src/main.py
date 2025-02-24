from textnode import TextNode, TextType


def main():
    tn = TextNode("dummy text", TextType.bold, "https://www.boot.dev")
    print(tn)


main()
