import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_emptyNode(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_propsSpace(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(node.propsToHTML()[0], " ")

    def test_emptyPropsDict(self):
        node = HTMLNode(props={})
        self.assertEqual(node.propsToHTML(), "")

    def test_toHTML(self):
        node = HTMLNode()
        # self.assertRaises(NotImplementedError, node.toHTML)


if __name__ == "__main__":
    unittest.main()
