from textnode import TextNode, TextType


def splitNodes(oldNodes: list[TextNode], delimeter: str, textType: TextType):
    newNodes = []
    for node in oldNodes:
        if node.textType != TextType.text:
            newNodes.append(node)
            continue
        split = node.text.split(delimeter)

        if len(split) == 1:
            newNodes.append(node)
            continue

        newNodes.extend(
            [
                TextNode(split[0], TextType.text),
                TextNode(split[1], textType),
                TextNode(split[2], TextType.text),
            ]
        )

    return newNodes
