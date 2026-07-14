"""Core matching engine for text pattern extraction and matching."""

import re
from typing import List, Dict, Any, Pattern
from dataclasses import dataclass


@dataclass
class MatchResult:
    """Data class to store matching results."""
    matched_text: str
    match_type: str
    position: int
    confidence: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            'matched_text': self.matched_text,
            'match_type': self.match_type,
            'position': self.position,
            'confidence': self.confidence
        }


class TextMatcher:
    """Main text matching engine with support for emails, phones, keywords, and regex."""

    # Predefined regex patterns
    PATTERNS = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'phone': r'(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b',
        'phone_intl': r'\+?[1-9]\d{1,14}',  # International E.164 format
        'url': r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)',
    }

    def __init__(self, case_sensitive: bool = False):
        """Initialize the TextMatcher.
        
        Args:
            case_sensitive (bool): Whether matching should be case-sensitive. Defaults to False.
        """
        self.case_sensitive = case_sensitive
        self.compiled_patterns: Dict[str, Pattern] = {}
        self._compile_patterns()

    def _compile_patterns(self) -> None:
        """Compile regex patterns for better performance."""
        flags = 0 if self.case_sensitive else re.IGNORECASE
        for pattern_name, pattern_str in self.PATTERNS.items():
            self.compiled_patterns[pattern_name] = re.compile(pattern_str, flags)

    def match_emails(self, text: str) -> List[MatchResult]:
        """Extract all email addresses from text.
        
        Args:
            text (str): The text to search in.
            
        Returns:
            List[MatchResult]: List of found emails with their positions.
        """
        results = []
        pattern = self.compiled_patterns['email']
        for match in pattern.finditer(text):
            results.append(MatchResult(
                matched_text=match.group(),
                match_type='email',
                position=match.start()
            ))
        return results

    def match_phones(self, text: str, international: bool = False) -> List[MatchResult]:
        """Extract phone numbers from text.
        
        Args:
            text (str): The text to search in.
            international (bool): Use international E.164 format. Defaults to False.
            
        Returns:
            List[MatchResult]: List of found phone numbers with their positions.
        """
        results = []
        pattern_key = 'phone_intl' if international else 'phone'
        pattern = self.compiled_patterns[pattern_key]
        for match in pattern.finditer(text):
            results.append(MatchResult(
                matched_text=match.group(),
                match_type='phone',
                position=match.start()
            ))
        return results

    def match_urls(self, text: str) -> List[MatchResult]:
        """Extract URLs from text.
        
        Args:
            text (str): The text to search in.
            
        Returns:
            List[MatchResult]: List of found URLs with their positions.
        """
        results = []
        pattern = self.compiled_patterns['url']
        for match in pattern.finditer(text):
            results.append(MatchResult(
                matched_text=match.group(),
                match_type='url',
                position=match.start()
            ))
        return results

    def match_keywords(self, text: str, keywords: List[str]) -> List[MatchResult]:
        """Search for multiple keywords in text.
        
        Args:
            text (str): The text to search in.
            keywords (List[str]): List of keywords to search for.
            
        Returns:
            List[MatchResult]: List of found keywords with their positions.
        """
        results = []
        search_text = text if self.case_sensitive else text.lower()
        
        for keyword in keywords:
            search_keyword = keyword if self.case_sensitive else keyword.lower()
            start = 0
            while True:
                pos = search_text.find(search_keyword, start)
                if pos == -1:
                    break
                results.append(MatchResult(
                    matched_text=text[pos:pos + len(keyword)],
                    match_type='keyword',
                    position=pos
                ))
                start = pos + 1
        
        # Sort by position
        results.sort(key=lambda x: x.position)
        return results

    def match_regex(self, text: str, pattern: str, group: int = 0) -> List[MatchResult]:
        """Match text using a custom regex pattern.
        
        Args:
            text (str): The text to search in.
            pattern (str): The regex pattern to use.
            group (int): Which group to extract from the match. Defaults to 0 (full match).
            
        Returns:
            List[MatchResult]: List of matches with their positions.
            
        Raises:
            re.error: If the regex pattern is invalid.
        """
        results = []
        try:
            flags = 0 if self.case_sensitive else re.IGNORECASE
            regex = re.compile(pattern, flags)
            for match in regex.finditer(text):
                results.append(MatchResult(
                    matched_text=match.group(group) if group <= len(match.groups()) else match.group(),
                    match_type='regex',
                    position=match.start()
                ))
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")
        
        return results

    def classify_text(self, text: str, keywords_map: Dict[str, List[str]]) -> Dict[str, Any]:
        """Classify text based on keyword presence.
        
        Args:
            text (str): The text to classify.
            keywords_map (Dict[str, List[str]]): Dictionary mapping categories to keywords.
            
        Returns:
            Dict[str, Any]: Classification results with matched categories and keywords.
        """
        classification = {
            'text': text,
            'matched_categories': [],
            'matched_keywords': {},
            'all_matches': []
        }
        
        for category, keywords in keywords_map.items():
            matches = self.match_keywords(text, keywords)
            if matches:
                classification['matched_categories'].append(category)
                classification['matched_keywords'][category] = [
                    m.to_dict() for m in matches
                ]
                classification['all_matches'].extend(matches)
        
        return classification

    def extract_all(self, text: str) -> Dict[str, List[MatchResult]]:
        """Extract all known patterns from text in one call.
        
        Args:
            text (str): The text to extract from.
            
        Returns:
            Dict[str, List[MatchResult]]: Dictionary with all extraction results.
        """
        return {
            'emails': self.match_emails(text),
            'phones': self.match_phones(text),
            'urls': self.match_urls(text)
        }

    def add_custom_pattern(self, name: str, pattern: str) -> None:
        """Add a custom regex pattern.
        
        Args:
            name (str): Name for the pattern.
            pattern (str): Regex pattern string.
        """
        flags = 0 if self.case_sensitive else re.IGNORECASE
        try:
            self.compiled_patterns[name] = re.compile(pattern, flags)
            self.PATTERNS[name] = pattern
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")

    def match_with_custom_pattern(self, text: str, pattern_name: str) -> List[MatchResult]:
        """Match text using a custom pattern.
        
        Args:
            text (str): The text to search in.
            pattern_name (str): Name of the custom pattern.
            
        Returns:
            List[MatchResult]: List of matches.
            
        Raises:
            KeyError: If pattern name is not found.
        """
        if pattern_name not in self.compiled_patterns:
            raise KeyError(f"Pattern '{pattern_name}' not found. Available patterns: {list(self.compiled_patterns.keys())}")
        
        results = []
        pattern = self.compiled_patterns[pattern_name]
        for match in pattern.finditer(text):
            results.append(MatchResult(
                matched_text=match.group(),
                match_type=pattern_name,
                position=match.start()
            ))
        return results
