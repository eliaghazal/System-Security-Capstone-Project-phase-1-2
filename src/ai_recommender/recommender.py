"""
AI Recommender System for Cryptanalysis

This module implements multiple scoring methods to identify the most likely plaintext
from brute-force attack candidates:

Method A: Dictionary/word-match scoring
Method B: N-gram (quadgram) log-likelihood scoring  
Method C: Language model scoring
Method D: Hybrid heuristic combining all methods

All methods are documented and explainable (no black-box models).
"""

import re
import math
from collections import defaultdict


class AIRecommender:
    """
    AI-powered recommender system for ranking plaintext candidates.
    
    Combines multiple scoring methods for robust cryptanalysis.
    """
    
    def __init__(self):
        """Initialize the AI recommender system."""
        self.word_freq = self._load_word_frequencies()
        self.quadgrams = self._load_quadgrams()
        
    def _load_word_frequencies(self):
        """
        Load English word frequency list.
        
        METHOD A: Dictionary/word-match scoring
        Uses a list of common English words with their frequencies.
        
        Returns:
            dict: Word frequencies (word -> frequency score)
        """
        # Common English words with approximate frequency scores
        # Higher score = more common word
        common_words = {
            'the': 100, 'be': 90, 'to': 89, 'of': 88, 'and': 87, 'a': 86, 'in': 85,
            'that': 84, 'have': 83, 'i': 82, 'it': 81, 'for': 80, 'not': 79, 'on': 78,
            'with': 77, 'he': 76, 'as': 75, 'you': 74, 'do': 73, 'at': 72, 'this': 71,
            'but': 70, 'his': 69, 'by': 68, 'from': 67, 'they': 66, 'we': 65, 'say': 64,
            'her': 63, 'she': 62, 'or': 61, 'an': 60, 'will': 59, 'my': 58, 'one': 57,
            'all': 56, 'would': 55, 'there': 54, 'their': 53, 'what': 52, 'so': 51,
            'up': 50, 'out': 49, 'if': 48, 'about': 47, 'who': 46, 'get': 45, 'which': 44,
            'go': 43, 'me': 42, 'when': 41, 'make': 40, 'can': 39, 'like': 38, 'time': 37,
            'no': 36, 'just': 35, 'him': 34, 'know': 33, 'take': 32, 'people': 31,
            'into': 30, 'year': 29, 'your': 28, 'good': 27, 'some': 26, 'could': 25,
            'them': 24, 'see': 23, 'other': 22, 'than': 21, 'then': 20, 'now': 19,
            'look': 18, 'only': 17, 'come': 16, 'its': 15, 'over': 14, 'think': 13,
            'also': 12, 'back': 11, 'after': 10, 'use': 9, 'two': 8, 'how': 7, 'our': 6,
            'work': 5, 'first': 4, 'well': 3, 'way': 2, 'even': 1, 'new': 1, 'want': 1,
            'because': 1, 'any': 1, 'these': 1, 'give': 1, 'day': 1, 'most': 1, 'us': 1,
            'is': 85, 'was': 75, 'are': 70, 'been': 65, 'has': 60, 'had': 55, 'were': 50,
            'said': 45, 'did': 40, 'am': 35, 'being': 30, 'very': 25, 'never': 20,
            'may': 15, 'might': 10, 'must': 10, 'should': 10, 'hello': 50, 'world': 50,
            # Add more common words for better segmentation
            'quick': 25, 'brown': 25, 'fox': 25, 'dog': 25, 'cat': 25, 'man': 25,
            'woman': 25, 'child': 25, 'boy': 25, 'girl': 25, 'sir': 25, 'yes': 25,
            'where': 30, 'why': 30, 'here': 30, 'there': 30, 'every': 20,
            'everyone': 20, 'everything': 20, 'somewhere': 20, 'anywhere': 20,
            'someone': 20, 'something': 20, 'nothing': 20, 'nobody': 20,
            # Common action words
            'attack': 30, 'defend': 25, 'meet': 30, 'send': 25, 'receive': 20,
            'dawn': 25, 'dusk': 20, 'midnight': 25, 'noon': 20, 'morning': 25,
            'night': 30, 'today': 25, 'tomorrow': 25, 'yesterday': 20,
        }
        return common_words
    
    def _load_quadgrams(self):
        """
        Load English quadgram (4-letter sequence) frequencies.
        
        METHOD B: N-gram log-likelihood scoring
        Quadgrams are 4-character sequences with their frequencies in English text.
        Used for classical cryptanalysis.
        
        Returns:
            dict: Quadgram log probabilities
        """
        # Common English quadgrams with log frequencies
        # These are approximate values based on English language corpus analysis
        quadgrams = {
            'TION': -2.0, 'NTHE': -2.5, 'THER': -2.3, 'THAT': -2.4, 'OFTH': -2.8,
            'FTHE': -2.6, 'THES': -2.7, 'WITH': -2.9, 'INTH': -2.8, 'ANDX': -3.0,
            'HERE': -3.1, 'OULD': -3.2, 'OUGH': -3.3, 'HAVE': -3.0, 'HICH': -3.1,
            'WHIC': -3.2, 'THIS': -3.0, 'THIN': -3.1, 'THEY': -3.2, 'ATIO': -3.0,
            'EVER': -3.3, 'FROM': -3.1, 'OUGH': -3.3, 'WERE': -3.2, 'BEEN': -3.2,
            'HAVE': -3.0, 'THEI': -3.1, 'THEX': -3.5, 'INGX': -3.0, 'IONS': -3.0,
            'TTHE': -3.5, 'FORX': -3.2, 'TIONX': -3.0, 'EDXO': -3.5, 'TISXX': -4.0,
            'EREX': -3.5, 'SEXO': -4.0, 'MENTX': -3.2, 'ONTH': -3.3, 'STHE': -3.0,
            'THE ': -2.5, ' THE': -2.5, 'ING ': -3.0, ' AND': -2.8, 'AND ': -2.8,
            'TION': -2.0, 'HER ': -3.2, ' HER': -3.2, 'FOR ': -3.1, ' FOR': -3.1,
            'ENT ': -3.2, ' WAS': -3.0, 'WAS ': -3.0, 'TER ': -3.3, ' WIT': -3.1,
            'VER ': -3.4, 'ALL ': -3.2, ' ALL': -3.2, 'HIS ': -3.1, ' HIS': -3.1,
        }
        
        # Calculate total for normalization
        return quadgrams
    
    def _tokenize(self, text):
        """
        Tokenize text into words.
        
        Args:
            text (str): Text to tokenize
            
        Returns:
            list: List of words (lowercase)
        """
        # Remove punctuation and split on whitespace
        words = re.findall(r'[a-zA-Z]+', text.lower())
        return words
    
    def _segment_text(self, text):
        """
        Segment concatenated text into words using dynamic programming.
        
        This uses a word segmentation algorithm that finds the best way to split
        concatenated text into dictionary words. Useful for text without spaces.
        
        Args:
            text (str): Concatenated text without spaces
            
        Returns:
            list: List of segmented words
        """
        text = text.lower()
        text = re.sub(r'[^a-z]', '', text)  # Keep only letters
        
        if not text:
            return []
        
        n = len(text)
        # dp[i] = (score, word_list) for best segmentation of text[0:i]
        dp = [(0.0, [])] + [(float('-inf'), [])] * n
        
        for i in range(1, n + 1):
            # Try all possible last words ending at position i
            for j in range(max(0, i - 20), i):  # Limit word length to 20 chars
                word = text[j:i]
                word_len = len(word)
                
                # Score this word
                if word in self.word_freq:
                    # Prefer known words, with bonus for longer words
                    word_score = math.log(self.word_freq[word] + 1) + word_len * 0.5
                else:
                    # Heavy penalty for unknown words, especially short ones
                    if word_len == 1:
                        word_score = -15  # Very bad
                    elif word_len == 2:
                        word_score = -10  # Bad
                    else:
                        word_score = -5 / word_len  # Less penalty for longer unknown words
                
                # Calculate total score for this segmentation
                total_score = dp[j][0] + word_score
                
                if total_score > dp[i][0]:
                    dp[i] = (total_score, dp[j][1] + [word])
        
        return dp[n][1]
    
    def score_dictionary(self, text):
        """
        METHOD A: Dictionary/word-match scoring
        
        Tokenize the text and count how many words match our dictionary.
        Score is weighted by word frequency. If text has no spaces, attempts
        to segment it into words automatically.
        
        Args:
            text (str): Candidate plaintext
            
        Returns:
            tuple: (score, explanation_dict)
        """
        words = self._tokenize(text)
        
        # If we got only one long word, try word segmentation
        if len(words) == 1 and len(words[0]) > 5:
            segmented = self._segment_text(words[0])
            if len(segmented) > 1:  # Segmentation found multiple words
                words = segmented
        
        if not words:
            return 0.0, {'matched_words': [], 'total_words': 0, 'match_rate': 0.0, 'segmented': False}
        
        matched_words = []
        total_score = 0
        
        for word in words:
            if word in self.word_freq:
                matched_words.append(word)
                total_score += self.word_freq[word]
        
        # Normalize by number of words
        match_rate = len(matched_words) / len(words) if words else 0
        avg_score = total_score / len(words) if words else 0
        
        # Combine match rate and average frequency score
        final_score = match_rate * 0.7 + (avg_score / 100) * 0.3
        
        explanation = {
            'matched_words': matched_words[:10],  # Top 10 for display
            'total_words': len(words),
            'matched_count': len(matched_words),
            'match_rate': match_rate,
            'avg_frequency': avg_score,
            'segmented': len(words) > 1 and ' ' not in text,
        }
        
        return final_score, explanation
    
    def score_ngram(self, text):
        """
        METHOD B: N-gram (quadgram) log-likelihood scoring
        
        Calculate log probability based on quadgram frequencies.
        Higher score = more likely to be English text.
        Handles both spaced and non-spaced text.
        
        Args:
            text (str): Candidate plaintext
            
        Returns:
            tuple: (score, explanation_dict)
        """
        text_upper = text.upper()
        
        if len(text_upper) < 4:
            return -100.0, {'quadgram_count': 0, 'log_likelihood': -100.0}
        
        log_prob = 0.0
        quadgram_count = 0
        found_quadgrams = []
        
        # Calculate log probability for each quadgram
        for i in range(len(text_upper) - 3):
            quadgram = text_upper[i:i+4]
            
            if quadgram in self.quadgrams:
                prob = self.quadgrams[quadgram]
                log_prob += prob
                found_quadgrams.append((quadgram, prob))
                quadgram_count += 1
            else:
                # Penalty for unknown quadgrams
                log_prob += -5.0
        
        # Normalize by text length
        avg_log_prob = log_prob / (len(text_upper) - 3) if len(text_upper) > 3 else -100
        
        explanation = {
            'quadgram_count': quadgram_count,
            'log_likelihood': log_prob,
            'avg_log_prob': avg_log_prob,
            'sample_quadgrams': found_quadgrams[:5],
        }
        
        return avg_log_prob, explanation
    
    def score_language_model(self, text):
        """
        METHOD C: Language model scoring (simplified)
        
        Uses character-level statistics and bigram frequencies to estimate
        how "English-like" the text is. This is a lightweight alternative to
        full language models that maintains reproducibility.
        
        Args:
            text (str): Candidate plaintext
            
        Returns:
            tuple: (score, explanation_dict)
        """
        if not text:
            return -100.0, {'char_score': 0, 'bigram_score': 0}
        
        text_clean = text.lower()
        
        # Character frequency scoring
        # Expected frequencies in English (approximate)
        char_freq = {
            'e': 12.70, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97, 'n': 6.75,
            's': 6.33, 'h': 6.09, 'r': 5.99, 'd': 4.25, 'l': 4.03, 'c': 2.78,
            'u': 2.76, 'm': 2.41, 'w': 2.36, 'f': 2.23, 'g': 2.02, 'y': 1.97,
            'p': 1.93, 'b': 1.29, 'v': 0.98, 'k': 0.77, 'j': 0.15, 'x': 0.15,
            'q': 0.10, 'z': 0.07, ' ': 15.0,
        }
        
        char_score = 0.0
        char_count = 0
        
        for char in text_clean:
            if char in char_freq:
                char_score += char_freq[char]
                char_count += 1
        
        avg_char_score = char_score / char_count if char_count > 0 else 0
        
        # Bigram scoring
        common_bigrams = {
            'th': 3.56, 'he': 3.07, 'in': 2.43, 'er': 2.05, 'an': 1.99,
            're': 1.85, 'on': 1.76, 'at': 1.49, 'en': 1.45, 'nd': 1.35,
            'ti': 1.34, 'es': 1.34, 'or': 1.28, 'te': 1.20, 'of': 1.17,
            'ed': 1.17, 'is': 1.13, 'it': 1.12, 'al': 1.09, 'ar': 1.07,
            'st': 1.05, 'to': 1.04, 'nt': 1.04, 'ng': 0.95, 've': 0.93,
        }
        
        bigram_score = 0.0
        bigram_count = 0
        
        for i in range(len(text_clean) - 1):
            bigram = text_clean[i:i+2]
            if bigram in common_bigrams:
                bigram_score += common_bigrams[bigram]
                bigram_count += 1
        
        avg_bigram_score = bigram_score / (len(text_clean) - 1) if len(text_clean) > 1 else 0
        
        # Combine scores
        final_score = (avg_char_score / 10) * 0.5 + avg_bigram_score * 0.5
        
        explanation = {
            'char_score': avg_char_score,
            'bigram_score': avg_bigram_score,
            'char_count': char_count,
            'bigram_count': bigram_count,
        }
        
        return final_score, explanation
    
    def score_hybrid(self, text, alpha=0.35, beta=0.35, gamma=0.30):
        """
        METHOD D: Hybrid heuristic scoring
        
        Combines all three methods with configurable weights.
        This provides the most robust analysis.
        
        Args:
            text (str): Candidate plaintext
            alpha (float): Weight for dictionary score (default: 0.35)
            beta (float): Weight for n-gram score (default: 0.35)
            gamma (float): Weight for language model score (default: 0.30)
            
        Returns:
            tuple: (score, explanation_dict)
        """
        # Get individual scores
        dict_score, dict_explain = self.score_dictionary(text)
        ngram_score, ngram_explain = self.score_ngram(text)
        lm_score, lm_explain = self.score_language_model(text)
        
        # Normalize ngram score (it's in log space, typically negative)
        # Map -10 to 0, -2 to 1
        ngram_normalized = max(0, min(1, (ngram_score + 10) / 8))
        
        # Normalize LM score (typically 0-2 range)
        lm_normalized = max(0, min(1, lm_score / 2))
        
        # Calculate weighted combination
        final_score = (alpha * dict_score + 
                      beta * ngram_normalized + 
                      gamma * lm_normalized)
        
        explanation = {
            'final_score': final_score,
            'weights': {'alpha': alpha, 'beta': beta, 'gamma': gamma},
            'components': {
                'dictionary': {'score': dict_score, 'details': dict_explain},
                'ngram': {'score': ngram_score, 'normalized': ngram_normalized, 'details': ngram_explain},
                'language_model': {'score': lm_score, 'normalized': lm_normalized, 'details': lm_explain},
            }
        }
        
        return final_score, explanation
    
    def analyze_candidates(self, candidates, method='hybrid', top_n=5):
        """
        Analyze and rank plaintext candidates.
        
        Args:
            candidates (list): List of (key, plaintext) tuples
            method (str): Scoring method ('dictionary', 'ngram', 'language_model', 'hybrid')
            top_n (int): Number of top candidates to return
            
        Returns:
            list: Ranked list of (key, plaintext, score, explanation) tuples
        """
        scored_candidates = []
        
        for key, plaintext in candidates:
            if method == 'dictionary':
                score, explanation = self.score_dictionary(plaintext)
            elif method == 'ngram':
                score, explanation = self.score_ngram(plaintext)
            elif method == 'language_model':
                score, explanation = self.score_language_model(plaintext)
            else:  # hybrid (default)
                score, explanation = self.score_hybrid(plaintext)
            
            scored_candidates.append((key, plaintext, score, explanation))
        
        # Sort by score (descending)
        scored_candidates.sort(key=lambda x: x[2], reverse=True)
        
        return scored_candidates[:top_n]
    
    def print_analysis(self, ranked_candidates, method='hybrid'):
        """
        Print detailed analysis of top candidates.
        
        Args:
            ranked_candidates (list): Ranked candidates from analyze_candidates()
            method (str): Method used for scoring
        """
        print(f"\n{'='*70}")
        print(f"AI RECOMMENDER ANALYSIS (Method: {method.upper()})")
        print(f"{'='*70}\n")
        
        for rank, (key, plaintext, score, explanation) in enumerate(ranked_candidates, 1):
            print(f"Rank {rank}: Key {key}")
            print(f"Score: {score:.4f}")
            print(f"Text: {plaintext}")
            
            if method == 'dictionary' or method == 'hybrid':
                if 'components' in explanation and 'dictionary' in explanation['components']:
                    dict_details = explanation['components']['dictionary']['details']
                else:
                    dict_details = explanation
                
                if 'matched_words' in dict_details:
                    print(f"  - Matched words: {dict_details.get('matched_count', 0)}/{dict_details.get('total_words', 0)}")
                    if dict_details.get('matched_words'):
                        print(f"  - Sample matches: {', '.join(dict_details['matched_words'][:5])}")
            
            if method == 'ngram' or method == 'hybrid':
                if 'components' in explanation and 'ngram' in explanation['components']:
                    ngram_details = explanation['components']['ngram']['details']
                else:
                    ngram_details = explanation
                
                if 'log_likelihood' in ngram_details:
                    print(f"  - Quadgram log-likelihood: {ngram_details['log_likelihood']:.2f}")
            
            if method == 'language_model' or method == 'hybrid':
                if 'components' in explanation and 'language_model' in explanation['components']:
                    lm_details = explanation['components']['language_model']['details']
                else:
                    lm_details = explanation
                
                if 'char_score' in lm_details:
                    print(f"  - Character freq score: {lm_details['char_score']:.2f}")
                    print(f"  - Bigram score: {lm_details['bigram_score']:.2f}")
            
            print()
        
        print(f"{'='*70}\n")
