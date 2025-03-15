import re
from enum import Enum

from htmlnode import HTMLNode
from parentnode import ParentNode
from textnode import TextNode, TextType


class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "ulist"
    ordered_list = "olist"


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


def md_to_blocks(md):
    split = md.split("\n\n")
    blocks = []
    for block in split:
        if block == "":
            continue
        blocks.append(block.strip())

    return blocks


def block_to_blocktype(block):
    if re.match(r"\#{1,6}", block[:6]):
        return BlockType.heading
    if block[:3] == "```" and block[-3:] == "```":
        return BlockType.code
    split = block.split("\n")
    if all(c[0] == ">" for c in split):
        return BlockType.quote
    if all(p[:2] == "- " for p in split):
        return BlockType.unordered_list
    if all(re.match(r"\d{1}\. ", p) for p in split):
        return BlockType.ordered_list

    return BlockType.paragraph


def block_to_HTMLNode(block, btype: BlockType):
    if btype == BlockType.paragraph:
        tnodes = textToTextNode(block)
        childnodes = map(lambda n: n.toHTMLNode(), tnodes)
        return HTMLNode("p", None, childnodes)
    if btype == BlockType.heading:
        match = re.findall(r"\#{1,6} ", block)
        hnum = len(match[0])
        block = block[hnum:]
        tnodes = textToTextNode(block)
        childnodes = map(lambda n: n.toHTMLNode(), tnodes)
        return HTMLNode(f"h{hnum-1}", None, childnodes)
    if btype == BlockType.quote:
        block = block.replace(">", "")
        tnodes = textToTextNode(block)
        childnodes = map(lambda n: n.toHTMLNode(), tnodes)
        return HTMLNode("blockquote", None, childnodes)
    if btype == BlockType.unordered_list:
        blocks = block.replace("\n", "").split("- ")[1:]
        childnodes = []
        for b in blocks:
            tnodes = textToTextNode(b)
            leafnodes = map(lambda n: n.toHTMLNode(), tnodes)
            childnodes.append(HTMLNode("li", None, leafnodes))
        return HTMLNode("ul", None, childnodes)
    if btype == BlockType.ordered_list:
        blocks = block.replace("\n", "")
        blocks = re.split(r"\d{1}\. ", blocks)[1:]
        childnodes = []
        for b in blocks:
            tnodes = textToTextNode(b)
            leafnodes = map(lambda n: n.toHTMLNode(), tnodes)
            childnodes.append(HTMLNode("li", None, leafnodes))
        return HTMLNode("ol", None, childnodes)
    if btype == BlockType.code:
        block = block.replace("```", "").strip("\n")
        childnode = TextNode(block, TextType.code).toHTMLNode()
        return HTMLNode("pre", None, [childnode])


def md_to_HTMLNode(md):
    blocks = md_to_blocks(md)
    childnodes = []
    for block in blocks:
        btype = block_to_blocktype(block)
        node = block_to_HTMLNode(block, btype)
        childnodes.append(node)

    return ParentNode("div", childnodes)
