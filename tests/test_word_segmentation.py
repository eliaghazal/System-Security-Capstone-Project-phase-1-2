"""
Unit tests for word segmentation and improved scoring on text without spaces
"""

import unittest
from src.ciphers.caesar import CaesarCipher
from src.ciphers.transposition import TranspositionCipher
from src.attacks.caesar_bruteforce import CaesarBruteForce
from src.attacks.transposition_bruteforce import TranspositionBruteForce
from src.ai_recommender.recommender import AIRecommender


class TestWordSegmentation(unittest.TestCase):
    """Test cases for word segmentation functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.recommender = AIRecommender()
    
    def test_segment_simple_concatenation(self):
        """Test segmentation of simple concatenated words."""
        result = self.recommender._segment_text("helloworld")
        self.assertEqual(result, ["hello", "world"])
    
    def test_segment_multiple_words(self):
        """Test segmentation of multiple concatenated words."""
        result = self.recommender._segment_text("thequickbrownfox")
        self.assertEqual(result, ["the", "quick", "brown", "fox"])
    
    def test_segment_with_common_phrase(self):
        """Test segmentation of common phrase."""
        result = self.recommender._segment_text("attackatdawn")
        self.assertEqual(result, ["attack", "at", "dawn"])
    
    def test_segment_longer_phrase(self):
        """Test segmentation of longer phrase."""
        result = self.recommender._segment_text("meetmeatmidnight")
        self.assertEqual(result, ["meet", "me", "at", "midnight"])
    
    def test_segment_empty_string(self):
        """Test segmentation of empty string."""
        result = self.recommender._segment_text("")
        self.assertEqual(result, [])
    
    def test_segment_single_word(self):
        """Test segmentation of single known word."""
        result = self.recommender._segment_text("hello")
        self.assertEqual(result, ["hello"])


class TestCaesarWithoutSpaces(unittest.TestCase):
    """Test Caesar cipher brute force attack on text without spaces."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cipher = CaesarCipher()
        self.bruteforce = CaesarBruteForce()
        self.recommender = AIRecommender()
    
    def test_decrypt_without_space_simple(self):
        """Test decryption of simple text without space."""
        plaintext = "helloworld"
        key = 3
        ciphertext = self.cipher.encrypt(plaintext, key)
        
        candidates = self.bruteforce.attack(ciphertext)
        ranked = self.recommender.analyze_candidates(candidates, method='hybrid', top_n=3)
        
        # Correct key should be in top 3
        top_keys = [k for k, _, _, _ in ranked]
        self.assertIn(key, top_keys)
        
        # Correct key should ideally be #1
        best_key = ranked[0][0]
        self.assertEqual(best_key, key)
    
    def test_decrypt_without_space_longer(self):
        """Test decryption of longer text without spaces."""
        plaintext = "thequickbrownfox"
        key = 7
        ciphertext = self.cipher.encrypt(plaintext, key)
        
        candidates = self.bruteforce.attack(ciphertext)
        ranked = self.recommender.analyze_candidates(candidates, method='hybrid', top_n=3)
        
        # Correct key should be in top 3
        top_keys = [k for k, _, _, _ in ranked]
        self.assertIn(key, top_keys)
    
    def test_score_comparison_with_without_space(self):
        """Test that scoring works for both spaced and non-spaced text."""
        plaintext_with_space = "hello world"
        plaintext_without_space = "helloworld"
        
        score_with, _ = self.recommender.score_hybrid(plaintext_with_space)
        score_without, _ = self.recommender.score_hybrid(plaintext_without_space)
        
        # Both should have good scores (> 0.4)
        self.assertGreater(score_with, 0.4)
        self.assertGreater(score_without, 0.4)
    
    def test_dictionary_scoring_triggers_segmentation(self):
        """Test that dictionary scoring automatically segments concatenated text."""
        text = "helloworld"
        score, explanation = self.recommender.score_dictionary(text)
        
        # Should have found words after segmentation
        self.assertGreater(explanation['matched_count'], 0)
        self.assertGreater(score, 0.5)
        
        # Check that segmentation was used
        self.assertTrue(explanation.get('segmented', False))
    
    def test_different_ai_methods_work_without_spaces(self):
        """Test that all AI methods work on text without spaces."""
        text = "helloworld"
        
        # All methods should return positive scores
        dict_score, _ = self.recommender.score_dictionary(text)
        ngram_score, _ = self.recommender.score_ngram(text)
        lm_score, _ = self.recommender.score_language_model(text)
        hybrid_score, _ = self.recommender.score_hybrid(text)
        
        self.assertGreater(dict_score, 0.0)
        self.assertIsNotNone(ngram_score)
        self.assertGreater(lm_score, 0.0)
        self.assertGreater(hybrid_score, 0.0)


class TestTranspositionWithoutSpaces(unittest.TestCase):
    """Test transposition cipher handling of text without spaces."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cipher = TranspositionCipher()
        self.recommender = AIRecommender()
    
    def test_transposition_removes_spaces(self):
        """Test that transposition cipher removes spaces."""
        plaintext = "hello world"
        key = "KEY"
        ciphertext = self.cipher.encrypt(plaintext, key)
        
        # Ciphertext should not contain spaces
        self.assertNotIn(' ', ciphertext)
    
    def test_score_transposition_candidates(self):
        """Test scoring of transposition cipher candidates."""
        # Create some realistic candidates
        candidates = [
            ("ABC", "helloworld"),
            ("BAC", "xyz qrs abc"),
            ("CAB", "thequickbrownfox"),
        ]
        
        ranked = self.recommender.analyze_candidates(candidates, method='hybrid', top_n=3)
        
        # All candidates should be scored
        self.assertEqual(len(ranked), 3)
        
        # Scores should be in descending order
        for i in range(len(ranked) - 1):
            self.assertGreaterEqual(ranked[i][2], ranked[i+1][2])


if __name__ == '__main__':
    unittest.main()
