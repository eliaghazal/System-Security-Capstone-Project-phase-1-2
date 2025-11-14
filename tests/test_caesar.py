"""Tests for Caesar cipher implementation."""
import pytest
from cipher_cryptanalysis.ciphers import CaesarCipher


class TestCaesarCipher:
    """Test cases for Caesar cipher."""
    
    def test_initialization(self):
        """Test cipher initialization."""
        cipher = CaesarCipher()
        assert cipher.alphabet_size == 26
        
        cipher = CaesarCipher(alphabet_size=10)
        assert cipher.alphabet_size == 10
    
    def test_initialization_invalid(self):
        """Test initialization with invalid alphabet size."""
        with pytest.raises(ValueError):
            CaesarCipher(alphabet_size=0)
        
        with pytest.raises(ValueError):
            CaesarCipher(alphabet_size=-5)
    
    def test_encrypt_basic(self):
        """Test basic encryption."""
        cipher = CaesarCipher()
        
        # Simple encryption
        assert cipher.encrypt("ABC", 1) == "BCD"
        assert cipher.encrypt("XYZ", 3) == "ABC"
        assert cipher.encrypt("HELLO", 3) == "KHOOR"
    
    def test_encrypt_case_preservation(self):
        """Test that encryption preserves case."""
        cipher = CaesarCipher()
        
        assert cipher.encrypt("Hello", 1) == "Ifmmp"
        assert cipher.encrypt("HeLLo WoRLd", 5) == "MjQQt BtWQi"
    
    def test_encrypt_non_alphabetic(self):
        """Test that non-alphabetic characters are not encrypted."""
        cipher = CaesarCipher()
        
        assert cipher.encrypt("Hello, World!", 3) == "Khoor, Zruog!"
        assert cipher.encrypt("123 ABC", 1) == "123 BCD"
        assert cipher.encrypt("Test-123", 2) == "Vguv-123"
    
    def test_encrypt_empty_string(self):
        """Test encryption of empty string."""
        cipher = CaesarCipher()
        assert cipher.encrypt("", 5) == ""
    
    def test_encrypt_wraparound(self):
        """Test that encryption wraps around alphabet."""
        cipher = CaesarCipher()
        
        assert cipher.encrypt("Z", 1) == "A"
        assert cipher.encrypt("z", 1) == "a"
        assert cipher.encrypt("XYZ", 5) == "CDE"
    
    def test_encrypt_negative_key(self):
        """Test encryption with negative key."""
        cipher = CaesarCipher()
        
        assert cipher.encrypt("BCD", -1) == "ABC"
        assert cipher.encrypt("ABC", -3) == "XYZ"
    
    def test_encrypt_large_key(self):
        """Test encryption with key larger than alphabet size."""
        cipher = CaesarCipher()
        
        # Key 27 should be same as key 1 (27 % 26 = 1)
        assert cipher.encrypt("ABC", 27) == cipher.encrypt("ABC", 1)
        assert cipher.encrypt("HELLO", 52) == cipher.encrypt("HELLO", 0)
    
    def test_decrypt_basic(self):
        """Test basic decryption."""
        cipher = CaesarCipher()
        
        assert cipher.decrypt("BCD", 1) == "ABC"
        assert cipher.decrypt("ABC", 3) == "XYZ"
        assert cipher.decrypt("KHOOR", 3) == "HELLO"
    
    def test_encrypt_decrypt_roundtrip(self):
        """Test that encryption followed by decryption returns original."""
        cipher = CaesarCipher()
        
        original = "Hello, World! 123"
        key = 7
        
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        
        assert decrypted == original
    
    def test_encrypt_decrypt_all_keys(self):
        """Test roundtrip for all possible keys."""
        cipher = CaesarCipher()
        original = "The Quick Brown Fox"
        
        for key in range(26):
            encrypted = cipher.encrypt(original, key)
            decrypted = cipher.decrypt(encrypted, key)
            assert decrypted == original
    
    def test_get_all_keys(self):
        """Test getting all possible keys."""
        cipher = CaesarCipher()
        keys = cipher.get_all_keys()
        
        assert len(keys) == 26
        assert keys == list(range(26))
        
        cipher = CaesarCipher(alphabet_size=10)
        keys = cipher.get_all_keys()
        assert len(keys) == 10
    
    def test_custom_alphabet_size(self):
        """Test cipher with custom alphabet size."""
        cipher = CaesarCipher(alphabet_size=10)
        
        # With alphabet_size=10, 'A' shifts to 'K', 'B' to 'L', etc.
        # But this wraps: A(0) + 5 = E(4), K(10) wraps around
        # Actually this doesn't make practical sense but tests the modulo logic
        original = "ABCDE"
        key = 3
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        
        assert decrypted == original
