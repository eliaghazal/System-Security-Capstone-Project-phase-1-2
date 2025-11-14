"""Scoring functions for plaintext quality assessment."""
import re
from typing import Dict, Set
from collections import Counter
import math
from .language_stats import (
    COMMON_ENGLISH_WORDS,
    COMMON_BIGRAMS,
    COMMON_TRIGRAMS,
    LETTER_FREQUENCIES,
)


class TextScorer:
    """
    Collection of scoring methods for evaluating plaintext quality.
    
    Provides dictionary-based, n-gram, frequency analysis, and combined scoring.
    """
    
    def __init__(self):
        """Initialize the text scorer."""
        self.common_words = COMMON_ENGLISH_WORDS
        self.bigrams = COMMON_BIGRAMS
        self.trigrams = COMMON_TRIGRAMS
        self.letter_freq = LETTER_FREQUENCIES
    
    def dictionary_score(self, text: str) -> float:
        """
        Score text based on the proportion of common English words.
        
        Args:
            text: The text to score
        
        Returns:
            Score between 0 and 1 (higher is better)
        """
        if not text:
            return 0.0
        
        # Extract words (lowercase, alphabetic only)
        words = re.findall(r'[a-zA-Z]+', text.lower())
        
        if not words:
            return 0.0
        
        # Count how many words are in the common words list
        common_count = sum(1 for word in words if word in self.common_words)
        
        return common_count / len(words)
    
    def bigram_score(self, text: str) -> float:
        """
        Score text based on English bigram frequencies.
        
        Args:
            text: The text to score
        
        Returns:
            Average bigram frequency score (higher is better)
        """
        if len(text) < 2:
            return 0.0
        
        # Extract only alphabetic characters and convert to lowercase
        clean_text = ''.join(c.lower() for c in text if c.isalpha())
        
        if len(clean_text) < 2:
            return 0.0
        
        # Generate bigrams
        bigrams = [clean_text[i:i+2] for i in range(len(clean_text) - 1)]
        
        # Calculate average frequency
        total_score = sum(self.bigrams.get(bg, 0.0) for bg in bigrams)
        
        return total_score / len(bigrams) if bigrams else 0.0
    
    def trigram_score(self, text: str) -> float:
        """
        Score text based on English trigram frequencies.
        
        Args:
            text: The text to score
        
        Returns:
            Average trigram frequency score (higher is better)
        """
        if len(text) < 3:
            return 0.0
        
        # Extract only alphabetic characters and convert to lowercase
        clean_text = ''.join(c.lower() for c in text if c.isalpha())
        
        if len(clean_text) < 3:
            return 0.0
        
        # Generate trigrams
        trigrams = [clean_text[i:i+3] for i in range(len(clean_text) - 2)]
        
        # Calculate average frequency
        total_score = sum(self.trigrams.get(tg, 0.0) for tg in trigrams)
        
        return total_score / len(trigrams) if trigrams else 0.0
    
    def frequency_score(self, text: str) -> float:
        """
        Score text based on letter frequency analysis (chi-squared test).
        
        Compares the letter frequency distribution to expected English distribution.
        Lower chi-squared value is better, so we return the inverse.
        
        Args:
            text: The text to score
        
        Returns:
            Score based on frequency analysis (higher is better)
        """
        if not text:
            return 0.0
        
        # Extract only alphabetic characters and convert to lowercase
        clean_text = ''.join(c.lower() for c in text if c.isalpha())
        
        if not clean_text:
            return 0.0
        
        # Count letter frequencies
        letter_count = Counter(clean_text)
        total_letters = len(clean_text)
        
        # Calculate chi-squared statistic
        chi_squared = 0.0
        for letter, expected_freq in self.letter_freq.items():
            observed_count = letter_count.get(letter, 0)
            observed_freq = (observed_count / total_letters) * 100
            expected_count = (expected_freq / 100) * total_letters
            
            if expected_count > 0:
                chi_squared += ((observed_count - expected_count) ** 2) / expected_count
        
        # Return inverse of chi-squared (lower chi-squared = better fit = higher score)
        # Add 1 to avoid division by zero and normalize
        return 1000.0 / (chi_squared + 1.0)
    
    def perplexity_score(self, text: str) -> float:
        """
        Calculate a simple perplexity-like score using n-gram probabilities.
        
        Lower perplexity indicates the text is more likely to be valid English.
        We return the inverse so higher scores are better.
        
        Args:
            text: The text to score
        
        Returns:
            Perplexity-based score (higher is better)
        """
        if len(text) < 3:
            return 0.0
        
        # Extract only alphabetic characters
        clean_text = ''.join(c.lower() for c in text if c.isalpha())
        
        if len(clean_text) < 3:
            return 0.0
        
        # Calculate log probability using bigrams and trigrams
        log_prob = 0.0
        count = 0
        
        # Bigram probabilities
        for i in range(len(clean_text) - 1):
            bigram = clean_text[i:i+2]
            prob = self.bigrams.get(bigram, 0.01)  # Small default probability
            log_prob += math.log(prob + 0.001)  # Add small value to avoid log(0)
            count += 1
        
        # Calculate average log probability
        avg_log_prob = log_prob / count if count > 0 else -100
        
        # Convert to perplexity-like score (higher is better)
        return math.exp(avg_log_prob / 10.0)  # Normalize
    
    def hybrid_score(self, text: str, weights: Dict[str, float] = None) -> float:
        """
        Combined score using multiple methods with configurable weights.
        
        Args:
            text: The text to score
            weights: Dictionary of method weights (default: equal weights)
                     Keys: 'dictionary', 'bigram', 'trigram', 'frequency', 'perplexity'
        
        Returns:
            Weighted combined score (higher is better)
        """
        if weights is None:
            # Default equal weights
            weights = {
                'dictionary': 0.3,
                'bigram': 0.2,
                'trigram': 0.2,
                'frequency': 0.2,
                'perplexity': 0.1,
            }
        
        # Calculate individual scores
        scores = {
            'dictionary': self.dictionary_score(text),
            'bigram': self.bigram_score(text),
            'trigram': self.trigram_score(text),
            'frequency': self.frequency_score(text),
            'perplexity': self.perplexity_score(text),
        }
        
        # Normalize scores to 0-1 range for fair combination
        # Dictionary score is already 0-1
        # Bigram and trigram scores need normalization (typical max ~3.5)
        scores['bigram'] = min(scores['bigram'] / 3.5, 1.0)
        scores['trigram'] = min(scores['trigram'] / 3.5, 1.0)
        # Frequency score is already normalized
        scores['frequency'] = min(scores['frequency'] / 100.0, 1.0)
        # Perplexity score is already normalized
        scores['perplexity'] = min(scores['perplexity'], 1.0)
        
        # Calculate weighted sum
        total_score = sum(scores[method] * weight 
                         for method, weight in weights.items() 
                         if method in scores)
        
        return total_score
