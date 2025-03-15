import unittest

from conversion import (
    BlockType,
    block_to_blocktype,
    extractmdImages,
    extractmdLinks,
    md_to_blocks,
    md_to_HTMLNode,
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

    def test_md_to_blocks(self):
        text = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        block = md_to_blocks(text)
        self.assertListEqual(
            block,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_blocktype(self):
        heading = "## HELLO"
        code = "```\n this is coce \n```"
        quote = ">this\n>is\n>quote"
        ulist = "- 1\n- 2\n- 3"
        olist = "1. one\n2. two\n3. three"
        para = "blab balab bla"
        self.assertEqual(block_to_blocktype(heading), BlockType.heading)
        self.assertEqual(block_to_blocktype(code), BlockType.code)
        self.assertEqual(block_to_blocktype(quote), BlockType.quote)
        self.assertEqual(block_to_blocktype(ulist), BlockType.unordered_list)
        self.assertEqual(block_to_blocktype(olist), BlockType.ordered_list)
        self.assertEqual(block_to_blocktype(para), BlockType.paragraph)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = md_to_HTMLNode(md)
        html = node.toHTML()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_headerblock(self):
        md = "### Title"
        node = md_to_HTMLNode(md)
        html = node.toHTML()
        self.assertEqual(html, "<div><h3>Title</h3></div>")

    def test_quoteblock(self):
        md = """>TEEST\n>quote"""
        node = md_to_HTMLNode(md)
        html = node.toHTML()
        self.assertEqual(html, "<div><blockquote>TEEST quote</blockquote></div>")

    def test_ulistblock(self):
        md = "- 1\n- 2\n- 3"
        node = md_to_HTMLNode(md)
        html = node.toHTML()
        self.assertEqual(html, "<div><ul><li>1</li><li>2</li><li>3</li></ul></div>")

    def test_olistblock(self):
        md = "1. a\n2. b\n3. c"
        node = md_to_HTMLNode(md)
        html = node.toHTML()
        self.assertEqual(html, "<div><ol><li>a</li><li>b</li><li>c</li></ol></div>")

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = md_to_HTMLNode(md)
        html = node.toHTML()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )
