import unittest
import sys
import os

# Add parent directory to path so we can import our module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.formatting import TextFormatter

class TestTextFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = TextFormatter()
    
    def test_remove_filler_words(self):
        # Test with default filler words
        text = "Uh, I think, like, this is, um, a test sentence, you know?"
        expected = "I think this is a test sentence?"
        result = self.formatter.remove_filler_words(text)
        self.assertEqual(result, expected)
        
        # Test with custom filler words
        custom_fillers = ["test", "sentence"]
        expected2 = "Uh, I think, like, this is, um, a, you know?"
        result2 = self.formatter.remove_filler_words(text, custom_fillers)
        self.assertEqual(result2, expected2)
    
    def test_fix_punctuation(self):
        # Test adding period
        text1 = "This is a test"
        expected1 = "This is a test."
        self.assertEqual(self.formatter.fix_punctuation(text1), expected1)
        
        # Test fixing spacing
        text2 = "This is a test,with bad spacing.And more issues"
        expected2 = "This is a test, with bad spacing. And more issues."
        self.assertEqual(self.formatter.fix_punctuation(text2), expected2)
        
        # Test fixing repeated punctuation
        text3 = "This is a test!!! With multiple punctuation..."
        expected3 = "This is a test! With multiple punctuation."
        self.assertEqual(self.formatter.fix_punctuation(text3), expected3)
    
    def test_fix_capitalization(self):
        # Test sentence capitalization
        text1 = "this is a test. another sentence. and another one."
        expected1 = "This is a test. Another sentence. And another one."
        self.assertEqual(self.formatter.fix_capitalization(text1), expected1)
        
        # Test proper noun capitalization
        text2 = "i went to france on monday in january."
        expected2 = "I went to France on Monday in January."
        self.assertEqual(self.formatter.fix_capitalization(text2), expected2)
    
    def test_format_text(self):
        # Test full formatting
        text = "um, this is, like, a test sentence on monday. i hope it works"
        expected = "This is a test sentence on Monday. I hope it works."
        result = self.formatter.format_text(text)
        self.assertEqual(result, expected)
        
        # Test with options disabled
        expected2 = "um, this is, like, a test sentence on monday. i hope it works."
        result2 = self.formatter.format_text(text, remove_fillers=False, fix_capitalization=False)
        self.assertEqual(result2, expected2)

if __name__ == '__main__':
    unittest.main()