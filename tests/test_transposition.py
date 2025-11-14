"""Tests for Transposition cipher implementation."""
import pytest
from cipher_cryptanalysis.ciphers import TranspositionCipher


class TestTranspositionCipher:
    """Test cases for Transposition cipher."""
    
    def test_initialization(self):
        """Test cipher initialization."""
        cipher = TranspositionCipher()
        assert cipher is not None
    
    def test_encrypt_basic(self):
        """Test basic encryption."""
        cipher = TranspositionCipher()
        
        # "HELLO" with key 2 -> "HLOEL " (with padding space)
        # Grid: H E
        #       L L
        #       O (padding space)
        # Read column-wise: H L O E L (space)
        result = cipher.encrypt("HELLO", 2)
        assert result == "HLOEL " or result.rstrip() == "HLOEL"
    
    def test_encrypt_exact_fit(self):
        """Test encryption when text fits exactly in grid."""
        cipher = TranspositionCipher()
        
        # "ABCD" with key 2 -> "ACBD"
        # Grid: A B
        #       C D
        # Read column-wise: A C B D
        result = cipher.encrypt("ABCD", 2)
        assert result == "ACBD"
    
    def test_encrypt_with_padding(self):
        """Test encryption with padding."""
        cipher = TranspositionCipher()
        
        # "HELLO WORLD" with key 4
        result = cipher.encrypt("HELLO WORLD", 4)
        # Grid: H E L L
        #       O   W O
        #       R L D (padding spaces)
        # Read column-wise: HOR E L LLWD O
        assert len(result) == 12  # 3 rows * 4 cols
    
    def test_encrypt_key_one(self):
        """Test encryption with key 1 (no transposition)."""
        cipher = TranspositionCipher()
        
        text = "HELLO"
        result = cipher.encrypt(text, 1)
        assert result == text
    
    def test_encrypt_invalid_key(self):
        """Test encryption with invalid key."""
        cipher = TranspositionCipher()
        
        with pytest.raises(ValueError):
            cipher.encrypt("HELLO", 0)
        
        with pytest.raises(ValueError):
            cipher.encrypt("HELLO", -1)
    
    def test_encrypt_empty_string(self):
        """Test encryption of empty string."""
        cipher = TranspositionCipher()
        assert cipher.encrypt("", 5) == ""
    
    def test_decrypt_basic(self):
        """Test basic decryption."""
        cipher = TranspositionCipher()
        
        # Decrypt "HLOEL" with key 2 -> "HELLO"
        result = cipher.decrypt("HLOEL", 2)
        assert result.strip() == "HELLO"
    
    def test_encrypt_decrypt_roundtrip(self):
        """Test that encryption followed by decryption returns original."""
        cipher = TranspositionCipher()
        
        original = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        key = 6
        
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        
        assert decrypted.strip() == original
    
    def test_encrypt_decrypt_various_keys(self):
        """Test roundtrip for various keys."""
        cipher = TranspositionCipher()
        original = "This is a test message"
        
        for key in range(2, 10):
            encrypted = cipher.encrypt(original, key)
            decrypted = cipher.decrypt(encrypted, key)
            assert decrypted.strip() == original
    
    def test_get_possible_keys(self):
        """Test getting possible keys."""
        cipher = TranspositionCipher()
        
        # For short text
        keys = cipher.get_possible_keys(5, max_key=20)
        assert 2 in keys
        assert 1 not in keys  # Key 1 is trivial
        
        # For longer text
        keys = cipher.get_possible_keys(100, max_key=10)
        assert len(keys) == 9  # 2 to 10
        assert min(keys) == 2
        assert max(keys) == 10
    
    def test_get_possible_keys_small_text(self):
        """Test getting possible keys for very small text."""
        cipher = TranspositionCipher()
        
        keys = cipher.get_possible_keys(1, max_key=20)
        assert keys == [1]
        
        keys = cipher.get_possible_keys(0, max_key=20)
        assert keys == [1]
    
    def test_decrypt_invalid_key(self):
        """Test decryption with invalid key."""
        cipher = TranspositionCipher()
        
        with pytest.raises(ValueError):
            cipher.decrypt("HELLO", 0)
        
        with pytest.raises(ValueError):
            cipher.decrypt("HELLO", -1)
    
    def test_decrypt_empty_string(self):
        """Test decryption of empty string."""
        cipher = TranspositionCipher()
        assert cipher.decrypt("", 5) == ""
