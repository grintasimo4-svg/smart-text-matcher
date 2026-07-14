#!/usr/bin/env python3
"""
Smart Text Matcher - Command Line Interface (CLI)
A powerful text matching and pattern extraction tool accessible from terminal.
"""

import argparse
import sys
import json
from pathlib import Path
from typing import List, Dict, Any
from src.matcher import TextMatcher
from src.utils import read_text_file, format_results


class TextMatcherCLI:
    """Command-line interface for Smart Text Matcher."""

    def __init__(self):
        """Initialize the CLI."""
        self.matcher = TextMatcher()
        self.results = {}

    def setup_parser(self) -> argparse.ArgumentParser:
        """Set up argument parser with all options."""
        parser = argparse.ArgumentParser(
            prog='smart-text-matcher',
            description='🚀 Smart Text Matcher - Powerful text matching and pattern extraction tool',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog='''
Examples:
  # Extract emails from a file
  python main.py --file data.txt --mode emails
  
  # Extract all patterns from direct text
  python main.py --text "Contact: test@example.com or call (555) 123-4567" --mode all
  
  # Extract URLs with JSON output
  python main.py --text "Visit https://example.com" --mode urls --format json
  
  # Use custom regex pattern
  python main.py --text "The numbers are 123, 456, and 789" --mode regex --pattern "\\d{3}"
  
  # Case-sensitive matching
  python main.py --text "Python and python" --mode keywords --keywords Python --case-sensitive
            '''
        )

        # Input options (mutually exclusive)
        input_group = parser.add_mutually_exclusive_group(required=True)
        input_group.add_argument(
            '--file', '-f',
            type=str,
            help='Path to text file to process'
        )
        input_group.add_argument(
            '--text', '-t',
            type=str,
            help='Direct text input to process'
        )

        # Matching mode
        parser.add_argument(
            '--mode', '-m',
            type=str,
            choices=['emails', 'phones', 'urls', 'keywords', 'regex', 'all'],
            default='all',
            help='Type of pattern matching to perform (default: all)'
        )

        # Optional parameters
        parser.add_argument(
            '--pattern', '-p',
            type=str,
            help='Custom regex pattern (used with --mode regex)'
        )

        parser.add_argument(
            '--keywords', '-k',
            type=str,
            nargs='+',
            help='Keywords to search for (used with --mode keywords)'
        )

        parser.add_argument(
            '--international',
            action='store_true',
            help='Use international E.164 format for phone numbers'
        )

        parser.add_argument(
            '--case-sensitive',
            action='store_true',
            help='Enable case-sensitive matching'
        )

        parser.add_argument(
            '--format', '-o',
            type=str,
            choices=['text', 'json', 'csv'],
            default='text',
            help='Output format (default: text)'
        )

        parser.add_argument(
            '--output', '-O',
            type=str,
            help='Save results to output file'
        )

        parser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help='Enable verbose output'
        )

        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s 1.0.0'
        )

        return parser

    def get_input_text(self, args: argparse.Namespace) -> str:
        """Get input text from file or direct argument."""
        if args.file:
            try:
                text = read_text_file(args.file)
                if args.verbose:
                    print(f"📄 Loaded file: {args.file} ({len(text)} characters)")
                return text
            except FileNotFoundError:
                print(f"❌ Error: File not found: {args.file}")
                sys.exit(1)
            except IOError as e:
                print(f"❌ Error reading file: {e}")
                sys.exit(1)
        else:
            return args.text

    def initialize_matcher(self, args: argparse.Namespace) -> None:
        """Initialize matcher with appropriate settings."""
        self.matcher = TextMatcher(case_sensitive=args.case_sensitive)
        if args.verbose and args.case_sensitive:
            print("🔤 Case-sensitive matching enabled")

    def process_emails(self, text: str) -> Dict[str, Any]:
        """Extract email addresses."""
        results = self.matcher.match_emails(text)
        return {
            'type': 'Emails',
            'count': len(results),
            'matches': [r.to_dict() for r in results]
        }

    def process_phones(self, text: str, international: bool) -> Dict[str, Any]:
        """Extract phone numbers."""
        results = self.matcher.match_phones(text, international=international)
        return {
            'type': 'Phone Numbers',
            'count': len(results),
            'matches': [r.to_dict() for r in results]
        }

    def process_urls(self, text: str) -> Dict[str, Any]:
        """Extract URLs."""
        results = self.matcher.match_urls(text)
        return {
            'type': 'URLs',
            'count': len(results),
            'matches': [r.to_dict() for r in results]
        }

    def process_keywords(self, text: str, keywords: List[str]) -> Dict[str, Any]:
        """Search for keywords."""
        if not keywords:
            print("❌ Error: Keywords required for --mode keywords")
            sys.exit(1)
        results = self.matcher.match_keywords(text, keywords)
        return {
            'type': 'Keywords',
            'count': len(results),
            'keywords_searched': keywords,
            'matches': [r.to_dict() for r in results]
        }

    def process_regex(self, text: str, pattern: str) -> Dict[str, Any]:
        """Match custom regex pattern."""
        if not pattern:
            print("❌ Error: Pattern required for --mode regex")
            sys.exit(1)
        try:
            results = self.matcher.match_regex(text, pattern)
            return {
                'type': 'Regex Matches',
                'pattern': pattern,
                'count': len(results),
                'matches': [r.to_dict() for r in results]
            }
        except ValueError as e:
            print(f"❌ Regex Error: {e}")
            sys.exit(1)

    def process_all(self, text: str, international: bool) -> Dict[str, Any]:
        """Extract all pattern types."""
        all_results = self.matcher.extract_all(text)
        return {
            'type': 'All Patterns',
            'emails': {
                'count': len(all_results['emails']),
                'matches': [r.to_dict() for r in all_results['emails']]
            },
            'phones': {
                'count': len(all_results['phones']),
                'matches': [r.to_dict() for r in all_results['phones']]
            },
            'urls': {
                'count': len(all_results['urls']),
                'matches': [r.to_dict() for r in all_results['urls']]
            }
        }

    def format_text_output(self, results: Dict[str, Any]) -> str:
        """Format results as readable text."""
        output = []
        output.append("\n" + "="*70)
        output.append("🎯 SMART TEXT MATCHER - RESULTS")
        output.append("="*70 + "\n")

        if results.get('type') == 'All Patterns':
            for pattern_type in ['emails', 'phones', 'urls']:
                count = results[pattern_type]['count']
                output.append(f"📧 {pattern_type.upper()}: {count} found")
                if results[pattern_type]['matches']:
                    for i, match in enumerate(results[pattern_type]['matches'], 1):
                        output.append(f"   {i}. {match['matched_text']} (pos: {match['position']})")
                else:
                    output.append(f"   No {pattern_type} found")
                output.append("")
        else:
            output.append(f"📋 Type: {results.get('type', 'Unknown')}")
            if 'pattern' in results:
                output.append(f"🔍 Pattern: {results['pattern']}")
            if 'keywords_searched' in results:
                output.append(f"🔑 Keywords: {', '.join(results['keywords_searched'])}")
            output.append(f"✅ Total Matches: {results.get('count', 0)}\n")

            if results.get('matches'):
                output.append("📍 Details:")
                for i, match in enumerate(results['matches'], 1):
                    output.append(f"   {i}. {match['matched_text']}")
                    output.append(f"      Position: {match['position']}")
                    output.append(f"      Type: {match['match_type']}")
                    if match['confidence'] < 1.0:
                        output.append(f"      Confidence: {match['confidence']:.2%}")
                    output.append("")
            else:
                output.append("❌ No matches found")

        output.append("="*70 + "\n")
        return "\n".join(output)

    def format_json_output(self, results: Dict[str, Any]) -> str:
        """Format results as JSON."""
        return json.dumps(results, indent=2, ensure_ascii=False)

    def format_csv_output(self, results: Dict[str, Any]) -> str:
        """Format results as CSV."""
        output = []
        
        if results.get('type') == 'All Patterns':
            all_matches = []
            for pattern_type in ['emails', 'phones', 'urls']:
                all_matches.extend(results[pattern_type]['matches'])
            matches = all_matches
        else:
            matches = results.get('matches', [])

        if not matches:
            return "No matches found"

        # CSV header
        output.append("matched_text,match_type,position,confidence")

        # CSV rows
        for match in matches:
            row = f"{match['matched_text']},{match['match_type']},{match['position']},{match['confidence']}"
            output.append(row)

        return "\n".join(output)

    def output_results(self, results: Dict[str, Any], format_type: str, output_file: str = None) -> None:
        """Output results in specified format."""
        if format_type == 'json':
            output = self.format_json_output(results)
        elif format_type == 'csv':
            output = self.format_csv_output(results)
        else:  # text
            output = self.format_text_output(results)

        # Print to stdout
        print(output)

        # Save to file if specified
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(output)
                print(f"✅ Results saved to: {output_file}")
            except IOError as e:
                print(f"❌ Error saving file: {e}")
                sys.exit(1)

    def run(self, args: argparse.Namespace) -> None:
        """Execute the CLI with provided arguments."""
        try:
            # Get input text
            text = self.get_input_text(args)

            if not text:
                print("❌ Error: Empty input text")
                sys.exit(1)

            if args.verbose:
                print(f"📊 Processing {len(text)} characters...")
                print(f"🔧 Mode: {args.mode}")

            # Initialize matcher
            self.initialize_matcher(args)

            # Process based on mode
            if args.mode == 'emails':
                results = self.process_emails(text)
            elif args.mode == 'phones':
                results = self.process_phones(text, args.international)
            elif args.mode == 'urls':
                results = self.process_urls(text)
            elif args.mode == 'keywords':
                results = self.process_keywords(text, args.keywords)
            elif args.mode == 'regex':
                results = self.process_regex(text, args.pattern)
            elif args.mode == 'all':
                results = self.process_all(text, args.international)
            else:
                print(f"❌ Error: Unknown mode: {args.mode}")
                sys.exit(1)

            # Output results
            self.output_results(results, args.format, args.output)

        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
            sys.exit(130)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)


def main():
    """Main entry point for CLI."""
    cli = TextMatcherCLI()
    parser = cli.setup_parser()

    # Parse arguments
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    # Run CLI
    cli.run(args)


if __name__ == '__main__':
    main()
