"""Unit tests for the TextMatcher class."""

import unittest
from src.matcher import TextMatcher, MatchResult


class TestTextMatcher(unittest.TestCase):
    """Test cases for TextMatcher."""

    def setUp(self):
        """Set up test fixtures."""
        self.matcher = TextMatcher()
        self.matcher_case_sensitive = TextMatcher(case_sensitive=True)

    def test_match_emails(self):
        """Test email extraction."""
        text = "Contact us at support@example.com or sales@company.co.uk"
        results = self.matcher.match_emails(text)
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].matched_text, "support@example.com")
        self.assertEqual(results[1].matched_text, "sales@company.co.uk")
        self.assertEqual(results[0].match_type, "email")

    def test_match_phones(self):
        """Test phone number extraction."""
        text = "Call us at (555) 123-4567 or 555.987.6543"
        results = self.matcher.match_phones(text)
        
        self.assertGreaterEqual(len(results), 1)
        self.assertTrue(any('555' in r.matched_text for r in results))

    def test_match_urls(self):
        """Test URL extraction."""
        text = "Visit https://www.example.com or http://example.org for more info"
        results = self.matcher.match_urls(text)
        
        self.assertEqual(len(results), 2)
        self.assertTrue(results[0].matched_text.startswith('http'))

    def test_match_keywords(self):
        """Test keyword matching."""
        text = "Python is great. I love Python programming."
        keywords = ["Python", "programming"]
        results = self.matcher.match_keywords(text, keywords)
        
        self.assertGreaterEqual(len(results), 2)
        matched_texts = [r.matched_text for r in results]
        self.assertIn("Python", matched_texts)
        self.assertIn("programming", matched_texts)

    def test_match_keywords_case_sensitive(self):
        """Test case-sensitive keyword matching."""
        text = "Python is great. python is cool."
        keywords = ["Python"]
        
        # Case-insensitive (default)
        results_insensitive = self.matcher.match_keywords(text, keywords)
        self.assertEqual(len(results_insensitive), 2)
        
        # Case-sensitive
        results_sensitive = self.matcher_case_sensitive.match_keywords(text, keywords)
        self.assertEqual(len(results_sensitive), 1)

    def test_match_regex(self):
        """Test regex pattern matching."""
        text = "The numbers are 123, 456, and 789."
        pattern = r"\d+"
        results = self.matcher.match_regex(text, pattern)
        
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0].matched_text, "123")
        self.assertEqual(results[1].matched_text, "456")
        self.assertEqual(results[2].matched_text, "789")

    def test_match_regex_invalid_pattern(self):
        """Test regex with invalid pattern."""
        text = "Test text"
        invalid_pattern = r"[invalid("
        
        with self.assertRaises(ValueError):
            self.matcher.match_regex(text, invalid_pattern)

    def test_classify_text(self):
        """Test text classification."""
        text = "I love Python and JavaScript. Programming is awesome!"
        keywords_map = {
            "languages": ["Python", "JavaScript"],
            "sentiment": ["love", "awesome"]
        }
        
        results = self.matcher.classify_text(text, keywords_map)
        
        self.assertIn("languages", results['matched_categories'])
        self.assertIn("sentiment", results['matched_categories'])
        self.assertIn("languages", results['matched_keywords'])
        self.assertIn("sentiment", results['matched_keywords'])

    def test_extract_all(self):
        """Test extracting all known patterns."""
        text = "Email: test@example.com, Phone: (555) 123-4567, Website: https://example.com"
        results = self.matcher.extract_all(text)
        
        self.assertIn('emails', results)
        self.assertIn('phones', results)
        self.assertIn('urls', results)
        self.assertGreater(len(results['emails']), 0)
        self.assertGreater(len(results['urls']), 0)

    def test_add_custom_pattern(self):
        """Test adding custom regex patterns."""
        # Add pattern for hashtags
        self.matcher.add_custom_pattern('hashtag', r'#\w+')
        
        text = "I love #python and #coding #awesome"
        results = self.matcher.match_with_custom_pattern(text, 'hashtag')
        
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0].matched_text, "#python")
        self.assertEqual(results[1].matched_text, "#coding")
        self.assertEqual(results[2].matched_text, "#awesome")

    def test_match_result_to_dict(self):
        """Test MatchResult.to_dict() method."""
        result = MatchResult(
            matched_text="test@example.com",
            match_type="email",
            position=0,
            confidence=0.95
        )
        
        result_dict = result.to_dict()
        
        self.assertEqual(result_dict['matched_text'], "test@example.com")
        self.assertEqual(result_dict['match_type'], "email")
        self.assertEqual(result_dict['position'], 0)
        self.assertEqual(result_dict['confidence'], 0.95)

    def test_empty_text(self):
        """Test matching on empty text."""
        text = ""
        
        self.assertEqual(len(self.matcher.match_emails(text)), 0)
        self.assertEqual(len(self.matcher.match_phones(text)), 0)
        self.assertEqual(len(self.matcher.match_urls(text)), 0)

    def test_no_matches(self):
        """Test when no patterns match."""
        text = "This is just plain text without any special content."
        
        self.assertEqual(len(self.matcher.match_emails(text)), 0)
        self.assertEqual(len(self.matcher.match_phones(text)), 0)
        self.assertEqual(len(self.matcher.match_urls(text)), 0)


if __name__ == '__main__':
    unittest.main()
