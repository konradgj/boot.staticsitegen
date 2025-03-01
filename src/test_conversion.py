import unittest

from conversion import (
    extractmdImages,
    extractmdLinks,
    splitNodes,
    splitNodesImage,
    splitNodesLinks,
    textToTextNode,
)
from textnode import TextNode, TextType


class TestConversion(unittest.TestCase):
    def test_textNode(self):
        node = TextNode("test", TextType.text)
        newNodes = splitNodes([node], "**", TextType.bold)
        self.assertEqual(newNodes[0].textType, TextType.text)

    def test_boldNode(self):
        node = TextNode("test", TextType.text)
        node2 = TextNode("this is a **bold word**", TextType.text)
        newNodes = splitNodes([node, node2], "**", TextType.bold)
        self.assertEqual(len(newNodes), 4)
        self.assertEqual(newNodes[2].textType, TextType.bold)

    def test_extractImages(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extractmdImages(text)
        self.assertListEqual(
            images,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extractLinks(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extractmdLinks(text)
        self.assertListEqual(
            links,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_splitNodeImage(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.text,
        )
        newNodes = splitNodesImage([node])
        self.assertListEqual(
            newNodes,
            [
                TextNode("This is text with an ", TextType.text),
                TextNode("image", TextType.image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.text),
                TextNode(
                    "second image", TextType.image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
        )

    def test_splitNodeLinks(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.text,
        )
        newNodes = splitNodesLinks([node])
        self.assertListEqual(
            newNodes,
            [
                TextNode("This is text with an ", TextType.text),
                TextNode("image", TextType.link, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.text),
                TextNode(
                    "second image", TextType.link, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
        )

    def test_textToNode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = textToTextNode(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.text),
                TextNode("text", TextType.bold),
                TextNode(" with an ", TextType.text),
                TextNode("italic", TextType.italic),
                TextNode(" word and a ", TextType.text),
                TextNode("code block", TextType.code),
                TextNode(" and an ", TextType.text),
                TextNode(
                    "obi wan image", TextType.image, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.text),
                TextNode("link", TextType.link, "https://boot.dev"),
            ],
        )
