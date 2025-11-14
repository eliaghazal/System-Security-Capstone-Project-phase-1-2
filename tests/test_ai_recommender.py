"""
Unit tests for AI Recommender system
"""

import unittest
from src.ai_recommender.recommender import AIRecommender


class TestAIRecommender(unittest.TestCase):
    """Test cases for AI Recommender."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.recommender = AIRecommender()
    
    def test_score_dictionary_english_text(self):
        """Test dictionary scoring with valid English text."""
        text = "the quick brown fox jumps over the lazy dog"
        score, explanation = self.recommender.score_dictionary(text)
        # Should have reasonable score for common English words
        self.assertGreater(score, 0.2)
        self.assertIn('matched_words', explanation)
        self.assertGreater(explanation['matched_count'], 0)
    
    def test_score_dictionary_gibberish(self):
        """Test dictionary scoring with gibberish."""
        text = "xyz qrs fgh jkl"
        score, explanation = self.recommender.score_dictionary(text)
        # Should have low score for nonsense words
        self.assertLess(score, 0.3)
    
    def test_score_ngram_english(self):
        """Test n-gram scoring with English text."""
        text = "the quick brown fox"
        score, explanation = self.recommender.score_ngram(text)
        # Should give reasonable score
        self.assertIsNotNone(score)
        self.assertIn('log_likelihood', explanation)
    
    def test_score_ngram_gibberish(self):
        """Test n-gram scoring with gibberish."""
        text = "xqz pwf"
        score, explanation = self.recommender.score_ngram(text)
        # Should have lower score than valid English
        self.assertLess(score, -3.0)
    
    def test_score_language_model(self):
        """Test language model scoring."""
        text = "hello world this is a test"
        score, explanation = self.recommender.score_language_model(text)
        self.assertIsNotNone(score)
        self.assertIn('char_score', explanation)
        self.assertIn('bigram_score', explanation)
    
    def test_score_hybrid(self):
        """Test hybrid scoring combines all methods."""
        text = "the quick brown fox"
        score, explanation = self.recommender.score_hybrid(text)
        self.assertIsNotNone(score)
        self.assertIn('components', explanation)
        self.assertIn('dictionary', explanation['components'])
        self.assertIn('ngram', explanation['components'])
        self.assertIn('language_model', explanation['components'])
    
    def test_analyze_candidates(self):
        """Test analyzing multiple candidates."""
        candidates = [
            (0, "xyz qrs abc"),
            (3, "the quick brown"),
            (5, "hello world"),
        ]
        
        ranked = self.recommender.analyze_candidates(candidates, method='hybrid', top_n=3)
        
        self.assertEqual(len(ranked), 3)
        # Check that results are sorted by score
        for i in range(len(ranked) - 1):
            self.assertGreaterEqual(ranked[i][2], ranked[i+1][2])
    
    def test_analyze_candidates_different_methods(self):
        """Test that different methods work."""
        candidates = [(i, "test message") for i in range(5)]
        
        for method in ['dictionary', 'ngram', 'language_model', 'hybrid']:
            ranked = self.recommender.analyze_candidates(candidates, method=method, top_n=3)
            self.assertEqual(len(ranked), 3)
    
    def test_tokenize(self):
        """Test text tokenization."""
        text = "Hello, World! This is a test."
        words = self.recommender._tokenize(text)
        expected = ['hello', 'world', 'this', 'is', 'a', 'test']
        self.assertEqual(words, expected)
    
    def test_hybrid_weights(self):
        """Test hybrid scoring with custom weights."""
        text = "hello world"
        score1, _ = self.recommender.score_hybrid(text, alpha=1.0, beta=0.0, gamma=0.0)
        score2, _ = self.recommender.score_hybrid(text, alpha=0.0, beta=1.0, gamma=0.0)
        score3, _ = self.recommender.score_hybrid(text, alpha=0.0, beta=0.0, gamma=1.0)
        
        # Different weights should produce different scores
        self.assertNotEqual(score1, score2)
        self.assertNotEqual(score2, score3)


if __name__ == '__main__':
    unittest.main()
