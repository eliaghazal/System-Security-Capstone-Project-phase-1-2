"""AI-based plaintext ranker for cryptanalysis."""
from typing import List, Tuple, Dict, Callable
from .scorer import TextScorer


class PlaintextRanker:
    """
    AI-based plaintext ranker that scores and ranks potential plaintexts.
    
    Uses multiple scoring methods (dictionary, n-grams, frequency analysis,
    perplexity) and provides explainable rankings.
    """
    
    def __init__(self, scoring_method: str = 'hybrid'):
        """
        Initialize the plaintext ranker.
        
        Args:
            scoring_method: Scoring method to use
                           Options: 'dictionary', 'bigram', 'trigram', 'frequency',
                           'perplexity', 'hybrid'
        """
        self.scorer = TextScorer()
        self.scoring_method = scoring_method
        self._validate_scoring_method()
    
    def _validate_scoring_method(self):
        """Validate that the scoring method is supported."""
        valid_methods = ['dictionary', 'bigram', 'trigram', 'frequency', 
                        'perplexity', 'hybrid']
        if self.scoring_method not in valid_methods:
            raise ValueError(
                f"Invalid scoring method: {self.scoring_method}. "
                f"Must be one of {valid_methods}"
            )
    
    def score(self, text: str) -> float:
        """
        Score a single text using the configured scoring method.
        
        Args:
            text: The text to score
        
        Returns:
            Score value (higher is better)
        """
        if self.scoring_method == 'dictionary':
            return self.scorer.dictionary_score(text)
        elif self.scoring_method == 'bigram':
            return self.scorer.bigram_score(text)
        elif self.scoring_method == 'trigram':
            return self.scorer.trigram_score(text)
        elif self.scoring_method == 'frequency':
            return self.scorer.frequency_score(text)
        elif self.scoring_method == 'perplexity':
            return self.scorer.perplexity_score(text)
        elif self.scoring_method == 'hybrid':
            return self.scorer.hybrid_score(text)
        else:
            raise ValueError(f"Unknown scoring method: {self.scoring_method}")
    
    def rank(
        self,
        candidates: List[Tuple[int, str]],
        top_n: int = 5
    ) -> List[Tuple[int, str, float]]:
        """
        Rank a list of plaintext candidates.
        
        Args:
            candidates: List of (key, plaintext) tuples
            top_n: Number of top results to return
        
        Returns:
            List of (key, plaintext, score) tuples, sorted by score (descending)
        """
        # Score each candidate
        scored = []
        for key, plaintext in candidates:
            score = self.score(plaintext)
            scored.append((key, plaintext, score))
        
        # Sort by score (descending) and return top N
        scored.sort(key=lambda x: x[2], reverse=True)
        return scored[:top_n]
    
    def explain_score(self, text: str) -> Dict[str, float]:
        """
        Provide explainable scoring breakdown for a text.
        
        Returns scores from all methods for transparency and reproducibility.
        
        Args:
            text: The text to analyze
        
        Returns:
            Dictionary mapping scoring method names to their scores
        """
        return {
            'dictionary': self.scorer.dictionary_score(text),
            'bigram': self.scorer.bigram_score(text),
            'trigram': self.scorer.trigram_score(text),
            'frequency': self.scorer.frequency_score(text),
            'perplexity': self.scorer.perplexity_score(text),
            'hybrid': self.scorer.hybrid_score(text),
        }
    
    def rank_with_explanation(
        self,
        candidates: List[Tuple[int, str]],
        top_n: int = 5
    ) -> List[Dict]:
        """
        Rank candidates with full explanation of scores.
        
        Args:
            candidates: List of (key, plaintext) tuples
            top_n: Number of top results to return
        
        Returns:
            List of dictionaries containing key, plaintext, score, and explanation
        """
        # Score and explain each candidate
        results = []
        for key, plaintext in candidates:
            explanation = self.explain_score(plaintext)
            primary_score = explanation[self.scoring_method]
            results.append({
                'key': key,
                'plaintext': plaintext,
                'score': primary_score,
                'explanation': explanation,
            })
        
        # Sort by primary score (descending) and return top N
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_n]
