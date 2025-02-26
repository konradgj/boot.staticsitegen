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

    def test_text(self):
        tnode = TextNode("test", TextType.text)
        hnode = tnode.toHTMLNode()
        self.assertEqual(hnode.tag, None)
        self.assertEqual(hnode.value, "test")

    def test_textTypes(self):
        tnode1 = TextNode("test", TextType.bold)
        tnode2 = TextNode("test", TextType.italic)
        tnode3 = TextNode("test", TextType.code)
        hnode1 = tnode1.toHTMLNode()
        hnode2 = tnode2.toHTMLNode()
        hnode3 = tnode3.toHTMLNode()
        self.assertEqual(hnode1.tag, "b")
        self.assertEqual(hnode2.tag, "i")
        self.assertEqual(hnode3.tag, "code")

    def test_links(self):
        tnode = TextNode("test", TextType.link, "www.test.no")
        tnode1 = TextNode("test", TextType.image, "www.test.no")
        hnode = tnode.toHTMLNode()
        hnode1 = tnode1.toHTMLNode()
        self.assertEqual(hnode.propsToHTML(), ' href="www.test.no"')
        self.assertEqual(hnode1.propsToHTML(), ' src="www.test.no" alt="test"')


if __name__ == "__main__":
    unittest.main()
