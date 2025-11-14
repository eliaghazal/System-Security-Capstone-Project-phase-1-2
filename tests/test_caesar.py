"""
Unit tests for Caesar Cipher implementation
"""

import unittest
from src.ciphers.caesar import CaesarCipher


class TestCaesarCipher(unittest.TestCase):
    """Test cases for Caesar cipher."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cipher = CaesarCipher()
    
    def test_encrypt_basic(self):
        """Test basic encryption."""
        plaintext = "HELLO"
        key = 3
        expected = "KHOOR"
        result = self.cipher.encrypt(plaintext, key)
        self.assertEqual(result, expected)
    
    def test_encrypt_lowercase(self):
        """Test encryption with lowercase letters."""
        plaintext = "hello"
        key = 3
        expected = "khoor"
        result = self.cipher.encrypt(plaintext, key)
        self.assertEqual(result, expected)
    
    def test_encrypt_mixed_case(self):
        """Test encryption preserves case."""
        plaintext = "Hello World"
        key = 5
        expected = "Mjqqt Btwqi"
        result = self.cipher.encrypt(plaintext, key)
        self.assertEqual(result, expected)
    
    def test_encrypt_with_punctuation(self):
        """Test that punctuation is preserved."""
        plaintext = "Hello, World!"
        key = 3
        expected = "Khoor, Zruog!"
        result = self.cipher.encrypt(plaintext, key)
        self.assertEqual(result, expected)
    
    def test_encrypt_with_numbers(self):
        """Test that numbers are preserved."""
        plaintext = "Test123"
        key = 1
        expected = "Uftu123"
        result = self.cipher.encrypt(plaintext, key)
        self.assertEqual(result, expected)
    
    def test_encrypt_wraparound(self):
        """Test wraparound from Z to A."""
        plaintext = "XYZ"
        key = 3
        expected = "ABC"
        result = self.cipher.encrypt(plaintext, key)
        self.assertEqual(result, expected)
    
    def test_decrypt_basic(self):
        """Test basic decryption."""
        ciphertext = "KHOOR"
        key = 3
        expected = "HELLO"
        result = self.cipher.decrypt(ciphertext, key)
        self.assertEqual(result, expected)
    
    def test_encrypt_decrypt_roundtrip(self):
        """Test that encrypt then decrypt returns original."""
        plaintext = "The Quick Brown Fox Jumps Over The Lazy Dog!"
        key = 13
        ciphertext = self.cipher.encrypt(plaintext, key)
        decrypted = self.cipher.decrypt(ciphertext, key)
        self.assertEqual(decrypted, plaintext)
    
    def test_key_zero(self):
        """Test that key=0 returns original text."""
        plaintext = "Hello World"
        result = self.cipher.encrypt(plaintext, 0)
        self.assertEqual(result, plaintext)
    
    def test_key_26(self):
        """Test that key=26 is same as key=0."""
        plaintext = "Hello World"
        result = self.cipher.encrypt(plaintext, 26)
        self.assertEqual(result, plaintext)
    
    def test_negative_key(self):
        """Test encryption with negative key."""
        plaintext = "HELLO"
        result = self.cipher.encrypt(plaintext, -3)
        expected = self.cipher.decrypt(plaintext, 3)
        self.assertEqual(result, expected)
    
    def test_configurable_alphabet_size(self):
        """Test with different alphabet size."""
        cipher = CaesarCipher(alphabet_size=26)
        plaintext = "ABC"
        key = 1
        result = cipher.encrypt(plaintext, key)
        self.assertEqual(result, "BCD")


if __name__ == '__main__':
    unittest.main()
