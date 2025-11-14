"""Tests for brute force attack implementation."""
import pytest
from cipher_cryptanalysis.attacks import BruteForceAttack
from cipher_cryptanalysis.ciphers import CaesarCipher, TranspositionCipher


class TestBruteForceAttack:
    """Test cases for brute force attack."""
    
    def test_initialization(self):
        """Test attack initialization."""
        attack = BruteForceAttack()
        assert attack is not None
    
    def test_attack_caesar_basic(self):
        """Test basic Caesar cipher attack."""
        attack = BruteForceAttack()
        
        # Encrypt a known plaintext
        cipher = CaesarCipher()
        plaintext = "HELLO"
        key = 3
        ciphertext = cipher.encrypt(plaintext, key)
        
        # Attack
        results = attack.attack_caesar(ciphertext)
        
        # Check that we get 26 results
        assert len(results) == 26
        
        # Check that the correct key is in the results
        assert (key, plaintext) in results
    
    def test_attack_caesar_all_keys(self):
        """Test that Caesar attack tries all keys."""
        attack = BruteForceAttack()
        
        ciphertext = "ABC"
        results = attack.attack_caesar(ciphertext, alphabet_size=26)
        
        # Should have one result for each key (0-25)
        assert len(results) == 26
        
        # Check keys are sequential
        keys = [k for k, _ in results]
        assert keys == list(range(26))
    
    def test_attack_caesar_custom_alphabet(self):
        """Test Caesar attack with custom alphabet size."""
        attack = BruteForceAttack()
        
        ciphertext = "ABC"
        results = attack.attack_caesar(ciphertext, alphabet_size=10)
        
        # Should have one result for each key (0-9)
        assert len(results) == 10
    
    def test_attack_transposition_basic(self):
        """Test basic Transposition cipher attack."""
        attack = BruteForceAttack()
        
        # Encrypt a known plaintext
        cipher = TranspositionCipher()
        plaintext = "HELLO WORLD"
        key = 3
        ciphertext = cipher.encrypt(plaintext, key)
        
        # Attack
        results = attack.attack_transposition(ciphertext, max_key=10)
        
        # Check that results are returned
        assert len(results) > 0
        
        # Check that the correct key produces the right result
        result_dict = {k: v for k, v in results}
        assert key in result_dict
        assert result_dict[key].strip() == plaintext
    
    def test_attack_transposition_max_key(self):
        """Test Transposition attack respects max_key."""
        attack = BruteForceAttack()
        
        ciphertext = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        max_key = 5
        results = attack.attack_transposition(ciphertext, max_key=max_key)
        
        # Should have at most max_key-1 results (keys 2 to max_key)
        assert len(results) <= max_key - 1
        
        # Check no key exceeds max_key
        keys = [k for k, _ in results]
        assert all(k <= max_key for k in keys)
    
    def test_attack_with_ranker_caesar(self):
        """Test Caesar attack with ranking function."""
        attack = BruteForceAttack()
        
        # Create a simple ranker that prefers lowercase 'hello'
        def simple_ranker(text):
            return 1.0 if "hello" in text.lower() else 0.0
        
        # Encrypt "HELLO"
        cipher = CaesarCipher()
        ciphertext = cipher.encrypt("HELLO", 3)
        
        # Attack with ranker
        results = attack.attack_with_ranker(
            ciphertext,
            'caesar',
            simple_ranker,
            top_n=5,
            alphabet_size=26
        )
        
        # Check that we get results
        assert len(results) <= 5
        
        # Check that results are tuples of (key, plaintext, score)
        assert all(len(r) == 3 for r in results)
        
        # The correct decryption should have the highest score
        best_key, best_text, best_score = results[0]
        assert "hello" in best_text.lower()
        assert best_score == 1.0
    
    def test_attack_with_ranker_transposition(self):
        """Test Transposition attack with ranking function."""
        attack = BruteForceAttack()
        
        # Create a simple ranker
        def simple_ranker(text):
            # Prefer text with more spaces (indicates word boundaries)
            return text.count(' ')
        
        # Encrypt a phrase
        cipher = TranspositionCipher()
        plaintext = "HELLO WORLD TEST"
        key = 4
        ciphertext = cipher.encrypt(plaintext, key)
        
        # Attack with ranker
        results = attack.attack_with_ranker(
            ciphertext,
            'transposition',
            simple_ranker,
            top_n=3,
            max_key=10
        )
        
        # Check that we get results
        assert len(results) <= 3
        assert len(results) > 0
        
        # Check format
        assert all(len(r) == 3 for r in results)
    
    def test_attack_with_ranker_invalid_cipher(self):
        """Test attack with invalid cipher type."""
        attack = BruteForceAttack()
        
        def dummy_ranker(text):
            return 0.0
        
        with pytest.raises(ValueError):
            attack.attack_with_ranker(
                "ABC",
                'invalid_cipher',
                dummy_ranker,
                top_n=5
            )
    
    def test_attack_with_ranker_sorting(self):
        """Test that results are sorted by score."""
        attack = BruteForceAttack()
        
        # Create a ranker that gives predictable scores
        def predictable_ranker(text):
            # Score based on first character
            if text and text[0].isalpha():
                return ord(text[0].upper()) - ord('A')
            return 0.0
        
        ciphertext = "TEST"
        results = attack.attack_with_ranker(
            ciphertext,
            'caesar',
            predictable_ranker,
            top_n=10,
            alphabet_size=26
        )
        
        # Check that scores are in descending order
        scores = [score for _, _, score in results]
        assert scores == sorted(scores, reverse=True)
