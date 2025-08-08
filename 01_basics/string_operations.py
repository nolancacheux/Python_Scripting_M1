"""
String Operations Examples
==========================

This module demonstrates comprehensive string manipulation, formatting,
and processing techniques in Python. Includes practical examples for
text processing, validation, and transformation.

Author: Python Learning Examples
Date: 2025
"""

import re
import string
from datetime import datetime


def demonstrate_basic_string_operations():
    """Demonstrate fundamental string operations."""
    print("=== Basic String Operations ===")
    
    text = "  Hello, Python World!  "
    
    # Basic string methods
    print(f"Original: '{text}'")
    print(f"Length: {len(text)}")
    print(f"Stripped: '{text.strip()}'")
    print(f"Left strip: '{text.lstrip()}'")
    print(f"Right strip: '{text.rstrip()}'")
    print(f"Upper case: '{text.upper()}'")
    print(f"Lower case: '{text.lower()}'")
    print(f"Title case: '{text.title()}'")
    print(f"Capitalize: '{text.capitalize()}'")
    print(f"Swap case: '{text.swapcase()}'")


def demonstrate_string_searching():
    """Demonstrate string searching and checking methods."""
    print("\n=== String Searching ===")
    
    sentence = "The quick brown fox jumps over the lazy dog"
    
    # Finding substrings
    print(f"Text: '{sentence}'")
    print(f"Find 'fox': {sentence.find('fox')}")
    print(f"Find 'cat': {sentence.find('cat')}")  # Returns -1 if not found
    print(f"Index 'fox': {sentence.index('fox')}")  # Raises exception if not found
    print(f"Count 'the': {sentence.count('the')}")
    print(f"Count 'The': {sentence.count('The')}")
    
    # Boolean checks
    print(f"Starts with 'The': {sentence.startswith('The')}")
    print(f"Ends with 'dog': {sentence.endswith('dog')}")
    print(f"Contains 'quick': {'quick' in sentence}")
    print(f"Is alphabetic: '{sentence}'.isalpha() = {sentence.isalpha()}")
    print(f"Is digit: '123'.isdigit() = {'123'.isdigit()}")
    print(f"Is alphanumeric: 'abc123'.isalnum() = {'abc123'.isalnum()}")


def demonstrate_string_modification():
    """Demonstrate string modification methods."""
    print("\n=== String Modification ===")
    
    text = "Hello, World!"
    
    # Replace operations
    print(f"Original: '{text}'")
    print(f"Replace 'World' with 'Python': '{text.replace('World', 'Python')}'")
    print(f"Replace 'l' with 'L': '{text.replace('l', 'L')}'")
    print(f"Replace 'l' with 'L' (max 2): '{text.replace('l', 'L', 2)}'")
    
    # Case conversions with special cases
    mixed_text = "hELLo WoRLd"
    print(f"\nMixed case: '{mixed_text}'")
    print(f"Title: '{mixed_text.title()}'")
    print(f"Capitalize: '{mixed_text.capitalize()}'")
    
    # String alignment
    word = "Python"
    print(f"\nAlignment examples with '{word}':")
    print(f"Center (20): '{word.center(20)}'")
    print(f"Left align (20): '{word.ljust(20)}'")
    print(f"Right align (20): '{word.rjust(20)}'")
    print(f"Zero fill (10): '{word.zfill(10)}'")


def demonstrate_string_splitting_joining():
    """Demonstrate string splitting and joining operations."""
    print("\n=== String Splitting and Joining ===")
    
    # Splitting strings
    sentence = "apple,banana,cherry,date"
    words = sentence.split(',')
    print(f"CSV string: '{sentence}'")
    print(f"Split by comma: {words}")
    
    # Different split scenarios
    text = "one two three four five"
    print(f"\nText: '{text}'")
    print(f"Split (default): {text.split()}")
    print(f"Split by space: {text.split(' ')}")
    print(f"Split (max 2): {text.split(' ', 2)}")
    
    # Joining strings
    words_list = ['Python', 'is', 'awesome']
    print(f"\nWords list: {words_list}")
    print(f"Join with spaces: '{' '.join(words_list)}'")
    print(f"Join with hyphens: '{'-'.join(words_list)}'")
    print(f"Join with newlines:\n{chr(10).join(words_list)}")
    
    # Partition and rpartition
    email = "user@example.com"
    print(f"\nEmail: '{email}'")
    print(f"Partition by '@': {email.partition('@')}")
    print(f"RPartition by '.': {email.rpartition('.')}")


def demonstrate_string_formatting():
    """Demonstrate various string formatting techniques."""
    print("\n=== String Formatting ===")
    
    name = "Alice"
    age = 30
    salary = 75000.5
    
    # f-strings (Python 3.6+) - Recommended
    print("=== f-strings ===")
    print(f"Name: {name}, Age: {age}")
    print(f"Salary: ${salary:,.2f}")
    print(f"Upper name: {name.upper()}")
    print(f"Age in 10 years: {age + 10}")
    
    # Format method
    print("\n=== format() method ===")
    print("Name: {}, Age: {}".format(name, age))
    print("Name: {0}, Age: {1}".format(name, age))
    print("Name: {n}, Age: {a}".format(n=name, a=age))
    print("Salary: ${:,.2f}".format(salary))
    
    # Old-style % formatting
    print("\n=== % formatting ===")
    print("Name: %s, Age: %d" % (name, age))
    print("Salary: $%.2f" % salary)
    
    # Advanced formatting
    print("\n=== Advanced formatting ===")
    pi = 3.14159265
    print(f"Pi to 2 decimals: {pi:.2f}")
    print(f"Pi in scientific notation: {pi:.2e}")
    print(f"Pi as percentage: {pi:.1%}")
    
    # Date formatting
    now = datetime.now()
    print(f"Current date: {now:%Y-%m-%d %H:%M:%S}")
    print(f"Formatted date: {now:%B %d, %Y}")


def demonstrate_string_validation():
    """Demonstrate string validation techniques."""
    print("\n=== String Validation ===")
    
    # Email validation (basic)
    def is_valid_email(email):
        """Basic email validation."""
        return '@' in email and '.' in email.split('@')[-1]
    
    emails = ["user@example.com", "invalid-email", "test@domain"]
    for email in emails:
        print(f"'{email}' is valid email: {is_valid_email(email)}")
    
    # Phone number validation
    def clean_phone_number(phone):
        """Clean and validate phone number."""
        # Remove non-digit characters
        digits = ''.join(c for c in phone if c.isdigit())
        
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits[0] == '1':
            return f"1-({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        else:
            return "Invalid phone number"
    
    phones = ["1234567890", "(123) 456-7890", "123-456-7890", "123456"]
    for phone in phones:
        print(f"'{phone}' -> {clean_phone_number(phone)}")
    
    # Password strength checker
    def check_password_strength(password):
        """Check password strength."""
        strength = 0
        feedback = []
        
        if len(password) >= 8:
            strength += 1
        else:
            feedback.append("At least 8 characters")
            
        if any(c.islower() for c in password):
            strength += 1
        else:
            feedback.append("Lowercase letter")
            
        if any(c.isupper() for c in password):
            strength += 1
        else:
            feedback.append("Uppercase letter")
            
        if any(c.isdigit() for c in password):
            strength += 1
        else:
            feedback.append("Number")
            
        if any(c in "!@#$%^&*" for c in password):
            strength += 1
        else:
            feedback.append("Special character")
        
        levels = ["Very Weak", "Weak", "Fair", "Good", "Strong"]
        return levels[min(strength, 4)], feedback
    
    passwords = ["weak", "StrongPass123!", "password", "Str0ng!"]
    for pwd in passwords:
        level, missing = check_password_strength(pwd)
        print(f"'{pwd}': {level}" + (f" (needs: {', '.join(missing)})" if missing else ""))


def demonstrate_regular_expressions():
    """Demonstrate basic regular expressions with strings."""
    print("\n=== Regular Expressions ===")
    
    text = "Contact us at support@example.com or call 123-456-7890"
    
    # Find email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    print(f"Text: {text}")
    print(f"Found emails: {emails}")
    
    # Find phone numbers
    phone_pattern = r'\b\d{3}-\d{3}-\d{4}\b'
    phones = re.findall(phone_pattern, text)
    print(f"Found phone numbers: {phones}")
    
    # Replace patterns
    censored = re.sub(r'\b\d{3}-\d{3}-\d{4}\b', 'XXX-XXX-XXXX', text)
    print(f"Censored: {censored}")
    
    # Split by patterns
    data = "apple,banana;cherry:date"
    items = re.split(r'[,;:]', data)
    print(f"Data: {data}")
    print(f"Split by separators: {items}")


def demonstrate_text_processing():
    """Demonstrate practical text processing examples."""
    print("\n=== Text Processing Examples ===")
    
    # Word frequency counter
    def count_words(text):
        """Count word frequency in text."""
        # Convert to lowercase and remove punctuation
        text = text.lower()
        # Remove punctuation
        translator = str.maketrans('', '', string.punctuation)
        text = text.translate(translator)
        
        words = text.split()
        word_count = {}
        
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1
        
        return word_count
    
    sample_text = "The quick brown fox jumps over the lazy dog. The dog was really lazy."
    word_freq = count_words(sample_text)
    print(f"Text: {sample_text}")
    print("Word frequency:")
    for word, count in sorted(word_freq.items()):
        print(f"  '{word}': {count}")
    
    # Title case converter (proper)
    def to_title_case(text):
        """Convert text to proper title case."""
        # Words that should remain lowercase (unless at start)
        minor_words = {'a', 'an', 'and', 'as', 'at', 'but', 'by', 'for', 
                      'if', 'in', 'nor', 'of', 'on', 'or', 'so', 'the', 
                      'to', 'up', 'yet'}
        
        words = text.split()
        result = []
        
        for i, word in enumerate(words):
            word = word.lower()
            if i == 0 or word not in minor_words:
                word = word.capitalize()
            result.append(word)
        
        return ' '.join(result)
    
    titles = [
        "the quick brown fox",
        "gone with the wind",
        "to be or not to be"
    ]
    
    print("\nTitle case conversion:")
    for title in titles:
        print(f"'{title}' -> '{to_title_case(title)}'")
    
    # Text statistics
    def text_statistics(text):
        """Calculate basic text statistics."""
        stats = {
            'characters': len(text),
            'characters_no_spaces': len(text.replace(' ', '')),
            'words': len(text.split()),
            'sentences': text.count('.') + text.count('!') + text.count('?'),
            'paragraphs': len([p for p in text.split('\n\n') if p.strip()])
        }
        return stats
    
    sample = """This is a sample text. It has multiple sentences!
    
    This is a second paragraph. How interesting?"""
    
    stats = text_statistics(sample)
    print(f"\nText statistics for: '{sample[:30]}...'")
    for key, value in stats.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")


def main():
    """Main function to run all demonstrations."""
    print("Python String Operations Examples")
    print("=" * 50)
    
    demonstrate_basic_string_operations()
    demonstrate_string_searching()
    demonstrate_string_modification()
    demonstrate_string_splitting_joining()
    demonstrate_string_formatting()
    demonstrate_string_validation()
    demonstrate_regular_expressions()
    demonstrate_text_processing()
    
    print("\n" + "=" * 50)
    print("All string operations examples completed!")


if __name__ == "__main__":
    main()


# Usage Examples:
"""
To run this script:
    python string_operations.py

Key concepts covered:
1. Basic string operations (strip, case conversion, etc.)
2. String searching and checking methods
3. String modification and replacement
4. String splitting and joining
5. String formatting (f-strings, format(), %)
6. String validation techniques
7. Regular expressions basics
8. Practical text processing examples

Best practices demonstrated:
- Use f-strings for modern string formatting
- Validate input data appropriately
- Use appropriate string methods for each task
- Handle edge cases in text processing
- Use regular expressions for complex patterns
- Consider performance for large text processing
- Include proper error handling
"""