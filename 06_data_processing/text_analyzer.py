#!/usr/bin/env python3
"""
Text Analyzer Script - Word Count and Frequency Analysis

This script demonstrates various text analysis techniques including word counting,
frequency analysis, sentiment analysis, and text statistics.

Author: Python Learning Series
Dependencies: collections, re, string
"""

import re
import string
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
import sys
import unicodedata


class TextAnalyzer:
    """
    A comprehensive text analysis class that provides methods for
    analyzing text content including word frequency, statistics, and patterns.
    """
    
    def __init__(self, text: Optional[str] = None):
        """
        Initialize the TextAnalyzer.
        
        Args:
            text: Optional text to analyze
        """
        self.original_text = text if text else ""
        self.processed_text = ""
        self.sentences = []
        self.words = []
        self.stop_words = self._load_stop_words()
        
        if text:
            self.load_text(text)
    
    def _load_stop_words(self) -> set:
        """
        Load common English stop words.
        
        Returns:
            set: Set of stop words
        """
        # Common English stop words
        stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'i', 'me', 'my', 'we', 'our', 'you',
            'your', 'this', 'these', 'they', 'them', 'their', 'have', 'had',
            'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may',
            'might', 'must', 'can', 'shall', 'am', 'been', 'being', 'or',
            'but', 'not', 'no', 'nor', 'so', 'if', 'then', 'than', 'when',
            'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few',
            'more', 'most', 'other', 'some', 'such', 'only', 'own', 'same',
            'up', 'out', 'over', 'under', 'again', 'further', 'once', 'here',
            'there', 'during', 'before', 'after', 'above', 'below', 'between'
        }
        return stop_words
    
    def load_text(self, text: str) -> bool:
        """
        Load text for analysis.
        
        Args:
            text: Text to analyze
            
        Returns:
            bool: True if text loaded successfully
        """
        try:
            self.original_text = text
            self.processed_text = self._preprocess_text(text)
            self.sentences = self._split_sentences(text)
            self.words = self._extract_words(self.processed_text)
            
            print(f"Text loaded successfully")
            print(f"Characters: {len(self.original_text)}")
            print(f"Words: {len(self.words)}")
            print(f"Sentences: {len(self.sentences)}")
            
            return True
            
        except Exception as e:
            print(f"Error loading text: {e}")
            return False
    
    def load_from_file(self, file_path: str, encoding: str = 'utf-8') -> bool:
        """
        Load text from a file.
        
        Args:
            file_path: Path to the text file
            encoding: File encoding
            
        Returns:
            bool: True if file loaded successfully
        """
        try:
            if not Path(file_path).exists():
                print(f"Error: File '{file_path}' not found.")
                return False
            
            with open(file_path, 'r', encoding=encoding) as file:
                text = file.read()
            
            print(f"Successfully loaded text from '{file_path}'")
            return self.load_text(text)
            
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def _preprocess_text(self, text: str, remove_punctuation: bool = False,
                        to_lowercase: bool = True) -> str:
        """
        Preprocess text for analysis.
        
        Args:
            text: Input text
            remove_punctuation: Whether to remove punctuation
            to_lowercase: Whether to convert to lowercase
            
        Returns:
            str: Preprocessed text
        """
        try:
            # Normalize unicode characters
            text = unicodedata.normalize('NFKD', text)
            
            # Convert to lowercase if requested
            if to_lowercase:
                text = text.lower()
            
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Remove punctuation if requested
            if remove_punctuation:
                text = text.translate(str.maketrans('', '', string.punctuation))
            
            return text
            
        except Exception as e:
            print(f"Error preprocessing text: {e}")
            return text
    
    def _split_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences.
        
        Args:
            text: Input text
            
        Returns:
            List[str]: List of sentences
        """
        try:
            # Simple sentence splitting using regex
            sentences = re.split(r'[.!?]+', text)
            
            # Clean up sentences
            sentences = [s.strip() for s in sentences if s.strip()]
            
            return sentences
            
        except Exception as e:
            print(f"Error splitting sentences: {e}")
            return []
    
    def _extract_words(self, text: str) -> List[str]:
        """
        Extract words from text.
        
        Args:
            text: Input text
            
        Returns:
            List[str]: List of words
        """
        try:
            # Extract words using regex (alphanumeric characters and apostrophes)
            words = re.findall(r"\b[a-zA-Z']+\b", text.lower())
            
            # Remove single character words (except 'a' and 'i')
            words = [word for word in words if len(word) > 1 or word in ['a', 'i']]
            
            return words
            
        except Exception as e:
            print(f"Error extracting words: {e}")
            return []
    
    def get_basic_statistics(self) -> Dict:
        """
        Get basic text statistics.
        
        Returns:
            Dict: Dictionary containing basic statistics
        """
        if not self.original_text:
            print("No text loaded.")
            return {}
        
        try:
            stats = {
                'character_count': len(self.original_text),
                'character_count_no_spaces': len(self.original_text.replace(' ', '')),
                'word_count': len(self.words),
                'sentence_count': len(self.sentences),
                'paragraph_count': len([p for p in self.original_text.split('\n\n') if p.strip()]),
                'average_word_length': sum(len(word) for word in self.words) / len(self.words) if self.words else 0,
                'average_sentence_length': len(self.words) / len(self.sentences) if self.sentences else 0,
                'unique_words': len(set(self.words)),
                'lexical_diversity': len(set(self.words)) / len(self.words) if self.words else 0
            }
            
            print("=== BASIC TEXT STATISTICS ===")
            print(f"Characters (with spaces): {stats['character_count']:,}")
            print(f"Characters (no spaces): {stats['character_count_no_spaces']:,}")
            print(f"Words: {stats['word_count']:,}")
            print(f"Unique words: {stats['unique_words']:,}")
            print(f"Sentences: {stats['sentence_count']:,}")
            print(f"Paragraphs: {stats['paragraph_count']:,}")
            print(f"Average word length: {stats['average_word_length']:.2f}")
            print(f"Average sentence length: {stats['average_sentence_length']:.2f}")
            print(f"Lexical diversity: {stats['lexical_diversity']:.3f}")
            
            return stats
            
        except Exception as e:
            print(f"Error calculating statistics: {e}")
            return {}
    
    def get_word_frequency(self, top_n: int = 20, 
                          exclude_stop_words: bool = True) -> List[Tuple[str, int]]:
        """
        Get word frequency analysis.
        
        Args:
            top_n: Number of top words to return
            exclude_stop_words: Whether to exclude stop words
            
        Returns:
            List[Tuple[str, int]]: List of (word, count) tuples
        """
        if not self.words:
            print("No words available for analysis.")
            return []
        
        try:
            # Filter words if needed
            if exclude_stop_words:
                filtered_words = [word for word in self.words if word not in self.stop_words]
            else:
                filtered_words = self.words
            
            # Count word frequencies
            word_freq = Counter(filtered_words)
            top_words = word_freq.most_common(top_n)
            
            print(f"=== TOP {top_n} WORD FREQUENCIES ===")
            print("(Excluding stop words)" if exclude_stop_words else "(Including all words)")
            
            for i, (word, count) in enumerate(top_words, 1):
                percentage = (count / len(filtered_words)) * 100
                print(f"{i:2d}. {word:<15} {count:4d} ({percentage:5.2f}%)")
            
            return top_words
            
        except Exception as e:
            print(f"Error analyzing word frequency: {e}")
            return []
    
    def get_character_frequency(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """
        Get character frequency analysis.
        
        Args:
            top_n: Number of top characters to return
            
        Returns:
            List[Tuple[str, int]]: List of (character, count) tuples
        """
        if not self.original_text:
            print("No text available for analysis.")
            return []
        
        try:
            # Count only alphabetic characters
            chars = [c.lower() for c in self.original_text if c.isalpha()]
            char_freq = Counter(chars)
            top_chars = char_freq.most_common(top_n)
            
            print(f"=== TOP {top_n} CHARACTER FREQUENCIES ===")
            
            for i, (char, count) in enumerate(top_chars, 1):
                percentage = (count / len(chars)) * 100
                print(f"{i:2d}. {char.upper():<3} {count:5d} ({percentage:5.2f}%)")
            
            return top_chars
            
        except Exception as e:
            print(f"Error analyzing character frequency: {e}")
            return []
    
    def get_word_length_distribution(self) -> Dict[int, int]:
        """
        Get distribution of word lengths.
        
        Returns:
            Dict[int, int]: Dictionary mapping word length to count
        """
        if not self.words:
            print("No words available for analysis.")
            return {}
        
        try:
            length_dist = Counter(len(word) for word in self.words)
            
            print("=== WORD LENGTH DISTRIBUTION ===")
            print("Length | Count | Percentage")
            print("-" * 30)
            
            total_words = len(self.words)
            for length in sorted(length_dist.keys()):
                count = length_dist[length]
                percentage = (count / total_words) * 100
                print(f"{length:6d} | {count:5d} | {percentage:9.2f}%")
            
            return dict(length_dist)
            
        except Exception as e:
            print(f"Error analyzing word length distribution: {e}")
            return {}
    
    def find_patterns(self, pattern: str, case_sensitive: bool = False) -> List[str]:
        """
        Find patterns in the text using regular expressions.
        
        Args:
            pattern: Regex pattern to search for
            case_sensitive: Whether search should be case sensitive
            
        Returns:
            List[str]: List of matches
        """
        if not self.original_text:
            print("No text available for pattern search.")
            return []
        
        try:
            flags = 0 if case_sensitive else re.IGNORECASE
            matches = re.findall(pattern, self.original_text, flags)
            
            print(f"=== PATTERN SEARCH: '{pattern}' ===")
            print(f"Found {len(matches)} matches")
            
            if matches:
                # Show unique matches with counts
                match_counts = Counter(matches)
                for match, count in match_counts.most_common():
                    print(f"  '{match}': {count} times")
            
            return matches
            
        except Exception as e:
            print(f"Error finding patterns: {e}")
            return []
    
    def get_readability_metrics(self) -> Dict[str, float]:
        """
        Calculate basic readability metrics.
        
        Returns:
            Dict[str, float]: Dictionary containing readability metrics
        """
        if not self.words or not self.sentences:
            print("Insufficient text for readability analysis.")
            return {}
        
        try:
            # Count syllables (approximation)
            def count_syllables(word):
                word = word.lower()
                vowels = 'aeiouy'
                syllable_count = 0
                prev_was_vowel = False
                
                for char in word:
                    if char in vowels:
                        if not prev_was_vowel:
                            syllable_count += 1
                        prev_was_vowel = True
                    else:
                        prev_was_vowel = False
                
                # Handle silent 'e' at the end
                if word.endswith('e') and syllable_count > 1:
                    syllable_count -= 1
                
                return max(1, syllable_count)
            
            total_syllables = sum(count_syllables(word) for word in self.words)
            total_words = len(self.words)
            total_sentences = len(self.sentences)
            
            # Flesch Reading Ease Score
            if total_sentences > 0 and total_words > 0:
                flesch_score = (206.835 - 
                              (1.015 * (total_words / total_sentences)) - 
                              (84.6 * (total_syllables / total_words)))
            else:
                flesch_score = 0
            
            # Flesch-Kincaid Grade Level
            if total_sentences > 0 and total_words > 0:
                fk_grade = (0.39 * (total_words / total_sentences) + 
                          11.8 * (total_syllables / total_words) - 15.59)
            else:
                fk_grade = 0
            
            # Automated Readability Index
            characters = sum(len(word) for word in self.words)
            if total_sentences > 0 and total_words > 0:
                ari = (4.71 * (characters / total_words) + 
                      0.5 * (total_words / total_sentences) - 21.43)
            else:
                ari = 0
            
            metrics = {
                'flesch_reading_ease': flesch_score,
                'flesch_kincaid_grade': max(0, fk_grade),
                'automated_readability_index': max(0, ari),
                'average_syllables_per_word': total_syllables / total_words if total_words > 0 else 0,
                'total_syllables': total_syllables
            }
            
            print("=== READABILITY METRICS ===")
            print(f"Flesch Reading Ease: {metrics['flesch_reading_ease']:.2f}")
            
            # Interpret Flesch score
            if flesch_score >= 90:
                difficulty = "Very Easy"
            elif flesch_score >= 80:
                difficulty = "Easy"
            elif flesch_score >= 70:
                difficulty = "Fairly Easy"
            elif flesch_score >= 60:
                difficulty = "Standard"
            elif flesch_score >= 50:
                difficulty = "Fairly Difficult"
            elif flesch_score >= 30:
                difficulty = "Difficult"
            else:
                difficulty = "Very Difficult"
            
            print(f"Reading Level: {difficulty}")
            print(f"Flesch-Kincaid Grade: {metrics['flesch_kincaid_grade']:.1f}")
            print(f"Automated Readability Index: {metrics['automated_readability_index']:.1f}")
            print(f"Average Syllables per Word: {metrics['average_syllables_per_word']:.2f}")
            
            return metrics
            
        except Exception as e:
            print(f"Error calculating readability metrics: {e}")
            return {}
    
    def analyze_sentiment(self) -> Dict[str, Union[float, int]]:
        """
        Perform basic sentiment analysis using word lists.
        
        Returns:
            Dict: Sentiment analysis results
        """
        if not self.words:
            print("No words available for sentiment analysis.")
            return {}
        
        try:
            # Simple positive and negative word lists
            positive_words = {
                'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
                'awesome', 'brilliant', 'outstanding', 'perfect', 'beautiful',
                'happy', 'joy', 'love', 'like', 'best', 'better', 'success',
                'successful', 'win', 'winning', 'positive', 'optimistic',
                'pleased', 'delighted', 'thrilled', 'excited', 'cheerful'
            }
            
            negative_words = {
                'bad', 'terrible', 'awful', 'horrible', 'disgusting', 'hate',
                'dislike', 'worst', 'worse', 'fail', 'failure', 'negative',
                'pessimistic', 'sad', 'angry', 'mad', 'disappointed', 'upset',
                'frustrated', 'annoying', 'irritating', 'boring', 'stupid',
                'ridiculous', 'pathetic', 'useless', 'worthless', 'disaster'
            }
            
            positive_count = sum(1 for word in self.words if word in positive_words)
            negative_count = sum(1 for word in self.words if word in negative_words)
            neutral_count = len(self.words) - positive_count - negative_count
            
            total_sentiment_words = positive_count + negative_count
            
            if total_sentiment_words > 0:
                sentiment_score = (positive_count - negative_count) / total_sentiment_words
            else:
                sentiment_score = 0.0
            
            # Classify overall sentiment
            if sentiment_score > 0.1:
                overall_sentiment = "Positive"
            elif sentiment_score < -0.1:
                overall_sentiment = "Negative"
            else:
                overall_sentiment = "Neutral"
            
            results = {
                'positive_words': positive_count,
                'negative_words': negative_count,
                'neutral_words': neutral_count,
                'sentiment_score': sentiment_score,
                'overall_sentiment': overall_sentiment,
                'total_words': len(self.words)
            }
            
            print("=== SENTIMENT ANALYSIS ===")
            print(f"Positive words: {positive_count}")
            print(f"Negative words: {negative_count}")
            print(f"Neutral words: {neutral_count}")
            print(f"Sentiment score: {sentiment_score:.3f}")
            print(f"Overall sentiment: {overall_sentiment}")
            
            return results
            
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return {}
    
    def export_analysis(self, filename: str) -> bool:
        """
        Export analysis results to a file.
        
        Args:
            filename: Output filename
            
        Returns:
            bool: True if export successful
        """
        if not self.original_text:
            print("No text to analyze.")
            return False
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("TEXT ANALYSIS REPORT\n")
                f.write("=" * 50 + "\n\n")
                
                # Basic statistics
                stats = self.get_basic_statistics()
                f.write("BASIC STATISTICS:\n")
                f.write("-" * 20 + "\n")
                for key, value in stats.items():
                    f.write(f"{key}: {value}\n")
                
                f.write("\n")
                
                # Top words
                f.write("TOP 20 WORDS (excluding stop words):\n")
                f.write("-" * 40 + "\n")
                word_freq = self.get_word_frequency(20, exclude_stop_words=True)
                for i, (word, count) in enumerate(word_freq, 1):
                    f.write(f"{i:2d}. {word:<15} {count:4d}\n")
                
                f.write("\n")
                
                # Readability metrics
                readability = self.get_readability_metrics()
                f.write("READABILITY METRICS:\n")
                f.write("-" * 20 + "\n")
                for key, value in readability.items():
                    f.write(f"{key}: {value}\n")
                
                f.write("\n")
                
                # Sentiment analysis
                sentiment = self.analyze_sentiment()
                f.write("SENTIMENT ANALYSIS:\n")
                f.write("-" * 20 + "\n")
                for key, value in sentiment.items():
                    f.write(f"{key}: {value}\n")
            
            print(f"Analysis exported to: {filename}")
            return True
            
        except Exception as e:
            print(f"Error exporting analysis: {e}")
            return False


def create_sample_text() -> str:
    """
    Create sample text for demonstration.
    
    Returns:
        str: Sample text
    """
    return """
    The art of data analysis has evolved tremendously in recent years. With the advent of 
    powerful computing tools and sophisticated algorithms, we can now process vast amounts 
    of information with unprecedented speed and accuracy. This technological revolution has 
    opened new frontiers in scientific research, business intelligence, and social sciences.
    
    Machine learning and artificial intelligence represent the cutting edge of this field. 
    These technologies enable computers to learn from data, identify patterns, and make 
    predictions without being explicitly programmed for each specific task. The applications 
    are virtually limitless, spanning from medical diagnosis to financial forecasting, 
    from autonomous vehicles to natural language processing.
    
    However, with great power comes great responsibility. As we develop more advanced 
    analytical tools, we must also address ethical considerations and ensure that our 
    technologies are used for the benefit of humanity. Privacy, fairness, and transparency 
    are crucial aspects that must be carefully considered in any data analysis project.
    
    The future of data analysis looks incredibly promising. As we continue to generate 
    more data than ever before, the need for skilled analysts and robust analytical 
    frameworks will only grow. Those who master these skills will be well-positioned 
    to contribute to solving some of the world's most pressing challenges.
    """


def main():
    """
    Demonstrate the TextAnalyzer class with various analysis techniques.
    
    Usage Examples:
    1. Analyze text file:
       python text_analyzer.py path/to/text.txt
       
    2. Analyze sample text:
       python text_analyzer.py
       
    3. Perform specific analysis:
       analyzer = TextAnalyzer(text)
       analyzer.get_word_frequency(10)
       analyzer.analyze_sentiment()
    """
    print("Text Analyzer - Demonstration")
    print("=" * 40)
    
    try:
        # Check if file path provided as command line argument
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            print(f"Loading text from: {file_path}")
            analyzer = TextAnalyzer()
            if not analyzer.load_from_file(file_path):
                print("Failed to load file. Using sample text instead.")
                analyzer.load_text(create_sample_text())
        else:
            print("No file path provided. Using sample text...")
            analyzer = TextAnalyzer(create_sample_text())
        
        if not analyzer.original_text:
            print("No text available for analysis. Exiting.")
            return
        
        print(f"\nAnalyzing text...")
        print(f"Text preview: {analyzer.original_text[:200]}...")
        
        # Perform comprehensive analysis
        print("\n" + "="*50)
        print("COMPREHENSIVE TEXT ANALYSIS")
        print("="*50)
        
        # 1. Basic Statistics
        print("\n")
        analyzer.get_basic_statistics()
        
        # 2. Word Frequency Analysis
        print("\n")
        analyzer.get_word_frequency(15, exclude_stop_words=True)
        
        # 3. Character Frequency Analysis
        print("\n")
        analyzer.get_character_frequency(10)
        
        # 4. Word Length Distribution
        print("\n")
        analyzer.get_word_length_distribution()
        
        # 5. Readability Metrics
        print("\n")
        analyzer.get_readability_metrics()
        
        # 6. Sentiment Analysis
        print("\n")
        analyzer.analyze_sentiment()
        
        # 7. Pattern Search Examples
        print("\n")
        print("=== PATTERN SEARCH EXAMPLES ===")
        
        # Find email patterns
        analyzer.find_patterns(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        
        # Find words ending in 'ing'
        analyzer.find_patterns(r'\b\w+ing\b', case_sensitive=False)
        
        # Find words starting with capital letters
        analyzer.find_patterns(r'\b[A-Z][a-z]+\b')
        
        # 8. Export Results
        output_file = "text_analysis_report.txt"
        if analyzer.export_analysis(output_file):
            print(f"\nDetailed analysis report saved to: {output_file}")
        
        print(f"\nAnalysis complete!")
        
        # Additional insights
        stats = analyzer.get_basic_statistics()
        if stats:
            print(f"\nKEY INSIGHTS:")
            print(f"- Text complexity: {stats['lexical_diversity']:.1%} unique words")
            print(f"- Average sentence length: {stats['average_sentence_length']:.1f} words")
            print(f"- Most efficient reading level based on word variety")
            
    except Exception as e:
        print(f"Error in main execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()