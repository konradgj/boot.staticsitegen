import re

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


def extractmdImages(text: str):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extractmdLinks(text: str):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def splitNodesImage(oldNodes: list[TextNode]):
    newNodes = []
    for node in oldNodes:
        if node.textType != TextType.text:
            newNodes.append(node)
            continue

        nstring = node.text
        images = extractmdImages(node.text)
        for image in images:
            ialt = image[0]
            ilink = image[1]
            istring = f"![{ialt}]({ilink})"
            split = nstring.split(istring, maxsplit=1)

            newNodes.extend(
                [
                    TextNode(split[0], TextType.text),
                    TextNode(ialt, TextType.image, ilink),
                ]
            )

            if split[1] == "":
                return newNodes
            nstring = split[1]
        newNodes.append(TextNode(nstring, TextType.text))
    return newNodes


def splitNodesLinks(oldNodes: list[TextNode]):
    newNodes = []
    for node in oldNodes:
        if node.textType != TextType.text:
            newNodes.append(node)
            continue

        nstring = node.text
        images = extractmdLinks(node.text)
        for image in images:
            ialt = image[0]
            ilink = image[1]
            istring = f"[{ialt}]({ilink})"
            split = nstring.split(istring, maxsplit=1)

            newNodes.extend(
                [
                    TextNode(split[0], TextType.text),
                    TextNode(ialt, TextType.link, ilink),
                ]
            )

            if split[1] == "":
                return newNodes
            nstring = split[1]
        newNodes.append(TextNode(nstring, TextType.text))
    return newNodes


def textToTextNode(text: str):
    node = TextNode(text, TextType.text)
    nodes = splitNodes([node], "**", TextType.bold)
    nodes = splitNodes(nodes, "_", TextType.italic)
    nodes = splitNodes(nodes, "`", TextType.code)
    nodes = splitNodesImage(nodes)
    nodes = splitNodesLinks(nodes)

    return nodes
