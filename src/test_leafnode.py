import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leafToHtmlp(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.toHTML(), "<p>Hello, world!</p>")

    def test_leafToHtmla(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.toHTML(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_noTag(self):
        node = LeafNode(None, "test")
        self.assertEqual(node.toHTML(), "test")

    def test_noValue(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.toHTML)


if __name__ == "__name__":
    unittest.main()
