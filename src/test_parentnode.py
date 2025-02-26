import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_withChildren(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.toHTML(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_withGrandChildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.toHTML(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_emptyTag(self):
        node = ParentNode(None, [LeafNode("a", "child")])
        self.assertRaises(ValueError, node.toHTML)

    def test_emptyChildren(self):
        node = ParentNode("a", None)
        self.assertRaises(ValueError, node.toHTML)

    def test_emptyChildList(self):
        node = ParentNode("a", [])
        self.assertRaises(ValueError, node.toHTML)
