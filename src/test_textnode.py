import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a text node", TextType.bold)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("b", TextType.bold)
        self.assertNotEqual(node, node2)
        node2 = TextNode("This is a text node", TextType.bold, "url")
        self.assertNotEqual(node, node2)
        node2 = TextNode("This is a text node", TextType.italic)
        self.assertNotEqual(node, node2)

    def test_urlNone(self):
        node = TextNode("a", TextType.italic)
        self.assertEqual(node.url, None)


if __name__ == "__main__":
    unittest.main()
