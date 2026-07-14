# Smart Text Matcher 🚀

A powerful, flexible, and intelligent Python tool for text matching, pattern extraction, and content classification. Perfect for email extraction, phone number detection, keyword matching, and advanced regex-based text processing.

## Features ✨

- **Email Extraction**: Accurately extract email addresses from any text with precision
- **Phone Number Detection**: Find phone numbers in various formats (US, International E.164)
- **URL Extraction**: Detect and extract URLs from text content
- **Keyword Matching**: Search for multiple keywords with position tracking
- **Regex Support**: Use custom regex patterns for advanced pattern matching
- **Text Classification**: Classify documents based on keyword presence
- **Case-Sensitive Matching**: Optional case-sensitive/insensitive matching modes
- **Batch Processing**: Extract all patterns at once for efficiency
- **Custom Patterns**: Add your own regex patterns dynamically at runtime
- **Comprehensive Results**: Track all matches with position information and confidence scores

## Installation 📦

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Clone the Repository

```bash
git clone https://github.com/grintasimo4-svg/smart-text-matcher.git
cd smart-text-matcher
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Quick Start 🏃

### Basic Email Extraction

```python
from src.matcher import TextMatcher

# Initialize the matcher
matcher = TextMatcher()

# Extract emails
text = "Contact support@example.com or sales@company.co.uk for assistance"
emails = matcher.match_emails(text)

for email in emails:
    print(f"Found: {email.matched_text} at position {email.position}")
# Output:
# Found: support@example.com at position 8
# Found: sales@company.co.uk at position 34
```

### Phone Number Extraction

```python
# Extract phone numbers (US format)
text = "Call us at (555) 123-4567 or 555.987.6543"
phones = matcher.match_phones(text)

for phone in phones:
    print(f"Phone: {phone.matched_text}")

# Extract international phone numbers
text = "International: +1234567890 or +441234567890"
intl_phones = matcher.match_phones(text, international=True)
```

### URL Extraction

```python
# Extract URLs
text = "Visit https://www.example.com or http://example.org for more"
urls = matcher.match_urls(text)

for url in urls:
    print(f"URL: {url.matched_text}")
```

### Keyword Matching

```python
# Match keywords
text = "Python is great. I love Python programming. Python development is awesome!"
keywords = ["Python", "development", "awesome"]
matches = matcher.match_keywords(text, keywords)

for match in matches:
    print(f"'{match.matched_text}' found at position {match.position}")
```

### Advanced Regex Matching

```python
# Custom regex for specific patterns
text = "The numbers are 123, 456, and 789. Also 101, 202."
pattern = r"\d{3}"  # Match 3-digit numbers
results = matcher.match_regex(text, pattern)

for result in results:
    print(f"Match: {result.matched_text}")
```

### Text Classification

```python
# Classify text based on keywords
text = "I love Python and JavaScript. Programming is awesome! Software development rocks!"

keywords_map = {
    "languages": ["Python", "JavaScript"],
    "sentiment": ["love", "awesome", "rocks"],
    "category": ["programming", "development"]
}

classification = matcher.classify_text(text, keywords_map)

print(f"Categories found: {classification['matched_categories']}")
print(f"Matched keywords: {classification['matched_keywords']}")
```

### Extract All Patterns

```python
# Extract all known patterns at once
text = "Email: test@example.com, Phone: (555) 123-4567, Website: https://example.com"
all_matches = matcher.extract_all(text)

print(f"Emails: {all_matches['emails']}")
print(f"Phones: {all_matches['phones']}")
print(f"URLs: {all_matches['urls']}")
```

### Case-Sensitive Matching

```python
# Case-sensitive matcher
matcher_cs = TextMatcher(case_sensitive=True)

text = "Python and python are different"
results_cs = matcher_cs.match_keywords(text, ["Python"])
print(f"Case-sensitive matches: {len(results_cs)}")  # 1

# Case-insensitive (default)
results_ci = matcher.match_keywords(text, ["Python"])
print(f"Case-insensitive matches: {len(results_ci)}")  # 2
```

### Custom Patterns

```python
# Add custom pattern for hashtags
matcher.add_custom_pattern('hashtag', r'#\w+')

text = "I love #python and #coding #awesome #development"
hashtags = matcher.match_with_custom_pattern(text, 'hashtag')

for tag in hashtags:
    print(f"Hashtag: {tag.matched_text}")
```

## API Reference 📚

### TextMatcher Class

#### Constructor
```python
TextMatcher(case_sensitive: bool = False)
```

**Parameters:**
- `case_sensitive` (bool): Set to True for case-sensitive matching. Defaults to False.

#### Methods

##### `match_emails(text: str) -> List[MatchResult]`
Extract all email addresses from text.

**Example:**
```python
emails = matcher.match_emails("Contact: admin@site.com")
```

##### `match_phones(text: str, international: bool = False) -> List[MatchResult]`
Extract phone numbers from text.

**Parameters:**
- `text` (str): The text to search in
- `international` (bool): Use international E.164 format (default: False)

**Example:**
```python
# US format
us_phones = matcher.match_phones("Call (555) 123-4567")

# International format
intl_phones = matcher.match_phones("+1234567890", international=True)
```

##### `match_urls(text: str) -> List[MatchResult]`
Extract URLs from text.

**Example:**
```python
urls = matcher.match_urls("Visit https://example.com")
```

##### `match_keywords(text: str, keywords: List[str]) -> List[MatchResult]`
Search for multiple keywords in text.

**Parameters:**
- `text` (str): The text to search in
- `keywords` (List[str]): List of keywords to find

**Example:**
```python
results = matcher.match_keywords(text, ["Python", "Java", "C++"])
```

##### `match_regex(text: str, pattern: str, group: int = 0) -> List[MatchResult]`
Match text using a custom regex pattern.

**Parameters:**
- `text` (str): The text to search in
- `pattern` (str): The regex pattern
- `group` (int): Which capture group to extract (default: 0 = full match)

**Example:**
```python
results = matcher.match_regex(text, r"\d+")
```

##### `classify_text(text: str, keywords_map: Dict[str, List[str]]) -> Dict[str, Any]`
Classify text based on keyword presence.

**Returns:**
```python
{
    'text': str,                      # Original text
    'matched_categories': List[str],  # Categories found
    'matched_keywords': Dict,         # Detailed keyword matches
    'all_matches': List              # All MatchResult objects
}
```

##### `extract_all(text: str) -> Dict[str, List[MatchResult]]`
Extract all known patterns (emails, phones, URLs) in one call.

**Returns:**
```python
{
    'emails': List[MatchResult],
    'phones': List[MatchResult],
    'urls': List[MatchResult]
}
```

##### `add_custom_pattern(name: str, pattern: str) -> None`
Add a custom regex pattern for later use.

**Example:**
```python
matcher.add_custom_pattern('zipcode', r'\d{5}')
```

##### `match_with_custom_pattern(text: str, pattern_name: str) -> List[MatchResult]`
Match using a previously added custom pattern.

**Example:**
```python
results = matcher.match_with_custom_pattern(text, 'zipcode')
```

### MatchResult Class

```python
@dataclass
class MatchResult:
    matched_text: str      # The matched text
    match_type: str        # Type of match (email, phone, url, keyword, regex, etc.)
    position: int          # Position in the original text
    confidence: float      # Confidence score (default 1.0)
    
    def to_dict() -> Dict[str, Any]
        # Convert result to dictionary format
```

**Example:**
```python
result = MatchResult(
    matched_text="test@example.com",
    match_type="email",
    position=0,
    confidence=1.0
)

result_dict = result.to_dict()
# {'matched_text': 'test@example.com', 'match_type': 'email', 'position': 0, 'confidence': 1.0}
```

## Running Tests 🧪

### Run All Tests
```bash
python -m pytest tests/
```

### Run with Coverage Report
```bash
python -m pytest tests/ --cov=src
```

### Run Specific Test File
```bash
python -m pytest tests/test_matcher.py
```

### Run Specific Test
```bash
python -m pytest tests/test_matcher.py::TestTextMatcher::test_match_emails
```

### Run Tests with Verbose Output
```bash
python -m pytest tests/ -v
```

## Project Structure 📁

```
smart-text-matcher/
│
├── src/
│   ├── __init__.py              # Package initialization
│   ├── matcher.py               # Core matching engine (230+ lines)
│   └── utils.py                 # Utility functions for file I/O
│
├── tests/
│   ├── __init__.py              # Tests package
│   └── test_matcher.py          # Comprehensive unit tests (13 test cases)
│
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── .gitignore                   # Git ignore rules
└── LICENSE                      # MIT License (optional)
```

## Use Cases 💡

1. **Email List Extraction**: Extract all emails from documents, web content, or logs
2. **Contact Information Harvesting**: Automatically find emails and phone numbers
3. **Log Analysis**: Search and classify logs based on specific keywords
4. **Document Classification**: Categorize documents by content patterns
5. **Data Validation**: Validate and extract structured data from unstructured text
6. **Web Scraping**: Extract specific information from web pages
7. **Social Media Analysis**: Find hashtags, mentions, and trending keywords
8. **Customer Support**: Automatically classify support tickets by keywords
9. **Resume Parsing**: Extract contact information and keywords from resumes
10. **Business Intelligence**: Analyze text data for sentiment and classification

## Performance Notes ⚡

- **Pre-compiled patterns**: Regex patterns are compiled once for optimal performance
- **Case-insensitive is faster**: Case-insensitive matching outperforms case-sensitive
- **Batch processing**: Use `extract_all()` for multiple pattern types
- **Sorted results**: Matches are sorted by position for easy sequential processing
- **Memory efficient**: Uses generators internally for large text processing

## Advanced Features 🎯

### Error Handling

```python
try:
    # Invalid regex pattern
    results = matcher.match_regex(text, "[invalid(")
except ValueError as e:
    print(f"Regex error: {e}")

try:
    # Non-existent custom pattern
    results = matcher.match_with_custom_pattern(text, 'unknown')
except KeyError as e:
    print(f"Pattern not found: {e}")
```

### Result Processing

```python
# Convert results to dictionaries
results = matcher.match_emails(text)
result_dicts = [r.to_dict() for r in results]

# JSON serialization
import json
json_output = json.dumps(result_dicts)
```

## Contributing 🤝

Contributions are welcome! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes with clear commit messages
4. **Write** or update tests as needed
5. **Run** tests to ensure everything passes (`pytest tests/`)
6. **Push** to the branch (`git push origin feature/amazing-feature`)
7. **Open** a Pull Request with a clear description

## License 📄

This project is licensed under the MIT License. See the LICENSE file for details.

## Roadmap 🗺️

- [x] Basic email extraction
- [x] Phone number detection (US & International)
- [x] URL extraction
- [x] Keyword matching with position tracking
- [x] Regex support for custom patterns
- [x] Text classification
- [x] Comprehensive unit tests
- [ ] Credit card detection (PCI-DSS compliant)
- [ ] Social security number detection
- [ ] Performance benchmarking utilities
- [ ] Web API interface (FastAPI)
- [ ] CLI tool for command-line usage
- [ ] Machine learning-based pattern detection
- [ ] Multi-language support
- [ ] Advanced text preprocessing
- [ ] Export to multiple formats (CSV, JSON, Excel)

## Troubleshooting 🔧

### Issue: Pattern not found
```python
# Check available patterns
print(matcher.compiled_patterns.keys())
```

### Issue: Incorrect matches
- Ensure the regex pattern is correctly formed
- Test your pattern with a regex tester first
- Consider case-sensitivity settings

### Issue: Performance with large text
```python
# Use batch extraction instead of multiple calls
results = matcher.extract_all(large_text)  # Faster than individual calls
```

## Support 💬

For issues, questions, or suggestions, please:
- Open an issue on GitHub
- Check existing issues for solutions
- Provide detailed examples with your question

## Authors ✍️

- **Smart Text Matcher Team** - Initial development and maintenance
- **grintasimo4-svg** - Project creator and lead developer

## Acknowledgments 🙏

Thanks to the Python community for excellent libraries like `regex`, `pytest`, and all the developers who contributed feedback and ideas.

---

**Made with ❤️ for developers and data enthusiasts worldwide**

*Last updated: 2026 | Version 1.0.0*
