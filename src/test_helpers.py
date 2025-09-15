import unittest

from helpers import extractTitle

class TestHelpers(unittest.TestCase):
  def test_extractTitle(self):
    md = "# Title\n something here\n more here"
    title = extractTitle(md)
    self.assertEqual(title, "Title")
  
  def test_extractTitleUnHappy(self):
    md = " Title\n something here\n more here"
    with self.assertRaises(ValueError):
       extractTitle(md)

if __name__ == "__name__":
    unittest.main()