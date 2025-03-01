import unittest

from conversion import extractmdImages, extractmdLinks, splitNodes
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
