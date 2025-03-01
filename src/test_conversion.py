import unittest

from conversion import splitNodes
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
