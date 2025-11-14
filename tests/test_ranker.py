"""Tests for plaintext ranker."""
import pytest
from cipher_cryptanalysis.recommender import PlaintextRanker


class TestPlaintextRanker:
    """Test cases for plaintext ranker."""
    
    def test_initialization_default(self):
        """Test ranker initialization with default method."""
        ranker = PlaintextRanker()
        assert ranker.scoring_method == 'hybrid'
    
    def test_initialization_custom_method(self):
        """Test ranker initialization with custom method."""
        ranker = PlaintextRanker(scoring_method='dictionary')
        assert ranker.scoring_method == 'dictionary'
    
    def test_initialization_invalid_method(self):
        """Test ranker initialization with invalid method."""
        with pytest.raises(ValueError):
            PlaintextRanker(scoring_method='invalid_method')
    
    def test_score_dictionary(self):
        """Test scoring with dictionary method."""
        ranker = PlaintextRanker(scoring_method='dictionary')
        
        good_text = "the cat and dog"
        bad_text = "xyz qrs tuv"
        
        assert ranker.score(good_text) > ranker.score(bad_text)
    
    def test_score_bigram(self):
        """Test scoring with bigram method."""
        ranker = PlaintextRanker(scoring_method='bigram')
        
        good_text = "the and that"
        bad_text = "xyz qrs"
        
        assert ranker.score(good_text) > ranker.score(bad_text)
    
    def test_score_trigram(self):
        """Test scoring with trigram method."""
        ranker = PlaintextRanker(scoring_method='trigram')
        
        good_text = "the and ing"
        score = ranker.score(good_text)
        assert score > 0.0
    
    def test_score_frequency(self):
        """Test scoring with frequency method."""
        ranker = PlaintextRanker(scoring_method='frequency')
        
        english_text = "the quick brown fox"
        score = ranker.score(english_text)
        assert score > 0.0
    
    def test_score_perplexity(self):
        """Test scoring with perplexity method."""
        ranker = PlaintextRanker(scoring_method='perplexity')
        
        english_text = "the quick brown fox"
        score = ranker.score(english_text)
        assert score > 0.0
    
    def test_score_hybrid(self):
        """Test scoring with hybrid method."""
        ranker = PlaintextRanker(scoring_method='hybrid')
        
        good_text = "the quick brown fox jumps"
        bad_text = "xyz qrs tuv wxy abc"
        
        assert ranker.score(good_text) > ranker.score(bad_text)
    
    def test_rank_basic(self):
        """Test basic ranking of candidates."""
        ranker = PlaintextRanker(scoring_method='dictionary')
        
        candidates = [
            (1, "xyz qrs tuv"),
            (2, "the cat sat"),
            (3, "abc def ghi"),
        ]
        
        results = ranker.rank(candidates, top_n=3)
        
        # Check we get 3 results
        assert len(results) == 3
        
        # Check format: (key, plaintext, score)
        assert all(len(r) == 3 for r in results)
        
        # Check that "the cat sat" is ranked first
        best_key, best_text, best_score = results[0]
        assert best_text == "the cat sat"
    
    def test_rank_top_n(self):
        """Test that ranking respects top_n parameter."""
        ranker = PlaintextRanker()
        
        candidates = [(i, f"text {i}") for i in range(10)]
        
        results = ranker.rank(candidates, top_n=5)
        assert len(results) == 5
        
        results = ranker.rank(candidates, top_n=3)
        assert len(results) == 3
    
    def test_rank_sorted_by_score(self):
        """Test that results are sorted by score."""
        ranker = PlaintextRanker(scoring_method='dictionary')
        
        candidates = [
            (1, "xyz"),
            (2, "the and that"),
            (3, "qrs"),
            (4, "cat dog"),
            (5, "tuv"),
        ]
        
        results = ranker.rank(candidates, top_n=5)
        
        # Scores should be in descending order
        scores = [score for _, _, score in results]
        assert scores == sorted(scores, reverse=True)
    
    def test_explain_score(self):
        """Test score explanation."""
        ranker = PlaintextRanker()
        
        text = "the quick brown fox"
        explanation = ranker.explain_score(text)
        
        # Should return dict with all scoring methods
        expected_keys = ['dictionary', 'bigram', 'trigram', 'frequency', 
                        'perplexity', 'hybrid']
        assert all(key in explanation for key in expected_keys)
        
        # All scores should be non-negative
        assert all(score >= 0.0 for score in explanation.values())
    
    def test_explain_score_empty_text(self):
        """Test score explanation for empty text."""
        ranker = PlaintextRanker()
        
        explanation = ranker.explain_score("")
        
        # Should still return all methods, with zero or low scores
        assert len(explanation) == 6
    
    def test_rank_with_explanation(self):
        """Test ranking with full explanation."""
        ranker = PlaintextRanker(scoring_method='dictionary')
        
        candidates = [
            (1, "the cat"),
            (2, "xyz qrs"),
        ]
        
        results = ranker.rank_with_explanation(candidates, top_n=2)
        
        # Check we get list of dicts
        assert len(results) == 2
        assert all(isinstance(r, dict) for r in results)
        
        # Check dict structure
        for result in results:
            assert 'key' in result
            assert 'plaintext' in result
            assert 'score' in result
            assert 'explanation' in result
            
            # Explanation should have all methods
            assert len(result['explanation']) == 6
    
    def test_rank_with_explanation_sorted(self):
        """Test that explanation results are sorted."""
        ranker = PlaintextRanker(scoring_method='hybrid')
        
        candidates = [
            (1, "xyz"),
            (2, "the cat and dog"),
            (3, "qrs tuv"),
        ]
        
        results = ranker.rank_with_explanation(candidates, top_n=3)
        
        # Scores should be in descending order
        scores = [r['score'] for r in results]
        assert scores == sorted(scores, reverse=True)
        
        # Best result should be "the cat and dog"
        assert results[0]['plaintext'] == "the cat and dog"
    
    def test_all_scoring_methods(self):
        """Test that all scoring methods work."""
        methods = ['dictionary', 'bigram', 'trigram', 'frequency', 
                  'perplexity', 'hybrid']
        
        text = "the quick brown fox"
        
        for method in methods:
            ranker = PlaintextRanker(scoring_method=method)
            score = ranker.score(text)
            assert score >= 0.0, f"Method {method} failed"
