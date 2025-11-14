"""Tests for text scoring functions."""
import pytest
from cipher_cryptanalysis.recommender import TextScorer


class TestTextScorer:
    """Test cases for text scoring methods."""
    
    def test_initialization(self):
        """Test scorer initialization."""
        scorer = TextScorer()
        assert scorer is not None
    
    def test_dictionary_score_good_text(self):
        """Test dictionary scoring with good English text."""
        scorer = TextScorer()
        
        # Common words (cat and dog are not in the basic common list)
        text = "the and the"
        score = scorer.dictionary_score(text)
        assert score == 1.0  # All words are common
    
    def test_dictionary_score_mixed_text(self):
        """Test dictionary scoring with mixed text."""
        scorer = TextScorer()
        
        # Mix of common and uncommon words
        text = "the xyzabc and qwerty"
        score = scorer.dictionary_score(text)
        assert 0.0 < score < 1.0  # Some words are common
    
    def test_dictionary_score_gibberish(self):
        """Test dictionary scoring with gibberish."""
        scorer = TextScorer()
        
        text = "xyzabc qwerty zxcvbn"
        score = scorer.dictionary_score(text)
        assert score == 0.0  # No common words
    
    def test_dictionary_score_empty(self):
        """Test dictionary scoring with empty text."""
        scorer = TextScorer()
        assert scorer.dictionary_score("") == 0.0
        assert scorer.dictionary_score("123 456") == 0.0  # No alphabetic
    
    def test_dictionary_score_case_insensitive(self):
        """Test that dictionary scoring is case-insensitive."""
        scorer = TextScorer()
        
        assert scorer.dictionary_score("THE CAT") == scorer.dictionary_score("the cat")
        assert scorer.dictionary_score("The Cat") == scorer.dictionary_score("the cat")
    
    def test_bigram_score_good_text(self):
        """Test bigram scoring with good English text."""
        scorer = TextScorer()
        
        # "the" contains common bigrams "th" and "he"
        text = "the"
        score = scorer.bigram_score(text)
        assert score > 0.0
    
    def test_bigram_score_common_bigrams(self):
        """Test bigram scoring recognizes common bigrams."""
        scorer = TextScorer()
        
        # Text with common bigrams should score higher
        good_text = "the and that"
        bad_text = "xqz zyx qxz"
        
        assert scorer.bigram_score(good_text) > scorer.bigram_score(bad_text)
    
    def test_bigram_score_empty(self):
        """Test bigram scoring with empty/short text."""
        scorer = TextScorer()
        
        assert scorer.bigram_score("") == 0.0
        assert scorer.bigram_score("a") == 0.0
    
    def test_trigram_score_good_text(self):
        """Test trigram scoring with good English text."""
        scorer = TextScorer()
        
        # "the" is a very common trigram
        text = "the"
        score = scorer.trigram_score(text)
        assert score > 0.0
    
    def test_trigram_score_common_trigrams(self):
        """Test trigram scoring recognizes common trigrams."""
        scorer = TextScorer()
        
        good_text = "the and ing"
        bad_text = "xyz qrs tuv"
        
        assert scorer.trigram_score(good_text) > scorer.trigram_score(bad_text)
    
    def test_trigram_score_empty(self):
        """Test trigram scoring with empty/short text."""
        scorer = TextScorer()
        
        assert scorer.trigram_score("") == 0.0
        assert scorer.trigram_score("ab") == 0.0
    
    def test_frequency_score_english_text(self):
        """Test frequency scoring with English text."""
        scorer = TextScorer()
        
        # English text should have reasonable frequency score
        english_text = "the quick brown fox jumps over the lazy dog"
        score = scorer.frequency_score(english_text)
        assert score > 0.0
    
    def test_frequency_score_comparison(self):
        """Test that English-like text scores higher than random."""
        scorer = TextScorer()
        
        english_text = "this is a test of the emergency broadcast system"
        random_text = "aaaaaaaaaa bbbbbbbbb ccccccccc"
        
        # English should score higher (better fit to expected distribution)
        assert scorer.frequency_score(english_text) > scorer.frequency_score(random_text)
    
    def test_frequency_score_empty(self):
        """Test frequency scoring with empty text."""
        scorer = TextScorer()
        assert scorer.frequency_score("") == 0.0
    
    def test_perplexity_score_english_text(self):
        """Test perplexity scoring with English text."""
        scorer = TextScorer()
        
        english_text = "the quick brown fox"
        score = scorer.perplexity_score(english_text)
        assert score > 0.0
    
    def test_perplexity_score_comparison(self):
        """Test that English-like text scores higher than gibberish."""
        scorer = TextScorer()
        
        english_text = "the cat and the dog"
        gibberish = "xqz pqr mnb"
        
        assert scorer.perplexity_score(english_text) > scorer.perplexity_score(gibberish)
    
    def test_perplexity_score_empty(self):
        """Test perplexity scoring with empty/short text."""
        scorer = TextScorer()
        
        assert scorer.perplexity_score("") == 0.0
        assert scorer.perplexity_score("ab") == 0.0
    
    def test_hybrid_score_default_weights(self):
        """Test hybrid scoring with default weights."""
        scorer = TextScorer()
        
        text = "the quick brown fox"
        score = scorer.hybrid_score(text)
        
        # Should return a reasonable score
        assert 0.0 <= score <= 1.0
        assert score > 0.0
    
    def test_hybrid_score_custom_weights(self):
        """Test hybrid scoring with custom weights."""
        scorer = TextScorer()
        
        text = "the quick brown fox"
        weights = {
            'dictionary': 1.0,
            'bigram': 0.0,
            'trigram': 0.0,
            'frequency': 0.0,
            'perplexity': 0.0,
        }
        
        # Should be same as dictionary score
        hybrid = scorer.hybrid_score(text, weights)
        dictionary = scorer.dictionary_score(text)
        
        # Allow small difference due to normalization
        assert abs(hybrid - dictionary) < 0.1
    
    def test_hybrid_score_comparison(self):
        """Test that hybrid score distinguishes good from bad text."""
        scorer = TextScorer()
        
        good_text = "the quick brown fox jumps over the lazy dog"
        bad_text = "xyz qrs tuv wxy abc def ghi jkl"
        
        assert scorer.hybrid_score(good_text) > scorer.hybrid_score(bad_text)
    
    def test_all_scores_on_same_text(self):
        """Test all scoring methods on the same text."""
        scorer = TextScorer()
        
        text = "the cat sat on the mat"
        
        # All methods should return non-negative scores
        assert scorer.dictionary_score(text) >= 0.0
        assert scorer.bigram_score(text) >= 0.0
        assert scorer.trigram_score(text) >= 0.0
        assert scorer.frequency_score(text) >= 0.0
        assert scorer.perplexity_score(text) >= 0.0
        assert scorer.hybrid_score(text) >= 0.0
