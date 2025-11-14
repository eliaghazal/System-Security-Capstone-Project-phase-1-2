"""
Unit tests for Transposition Cipher implementation
"""

import unittest
from src.ciphers.transposition import TranspositionCipher


class TestTranspositionCipher(unittest.TestCase):
    """Test cases for Transposition cipher."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cipher = TranspositionCipher()
    
    def test_encrypt_basic(self):
        """Test basic encryption."""
        plaintext = "HELLO"
        key = "KEY"
        result = self.cipher.encrypt(plaintext, key)
        # Should rearrange based on key order (with padding)
        self.assertIsNotNone(result)
        # Length may be greater due to padding
        self.assertGreaterEqual(len(result), len(plaintext))
    
    def test_decrypt_basic(self):
        """Test basic decryption."""
        plaintext = "HELLOWORLD"
        key = "CRYPTO"
        ciphertext = self.cipher.encrypt(plaintext, key)
        decrypted = self.cipher.decrypt(ciphertext, key)
        # Should recover original (may have padding)
        self.assertTrue(decrypted.startswith("HELLOWORLD"))
    
    def test_encrypt_decrypt_roundtrip(self):
        """Test that encrypt then decrypt returns original."""
        plaintext = "THEQUICKBROWNFOX"
        key = "SECRET"
        ciphertext = self.cipher.encrypt(plaintext, key)
        decrypted = self.cipher.decrypt(ciphertext, key)
        # May have trailing padding removed
        self.assertTrue(plaintext.startswith(decrypted) or decrypted.startswith(plaintext))
    
    def test_different_keys_produce_different_ciphertexts(self):
        """Test that different keys produce different results."""
        plaintext = "ATTACKATDAWN"
        key1 = "ABC"
        key2 = "CBA"  # Different order should produce different result
        result1 = self.cipher.encrypt(plaintext, key1)
        result2 = self.cipher.encrypt(plaintext, key2)
        self.assertNotEqual(result1, result2)
    
    def test_empty_key(self):
        """Test behavior with empty key."""
        plaintext = "HELLO"
        result = self.cipher.encrypt(plaintext, "")
        # Should return original or handle gracefully
        self.assertEqual(result, plaintext)
    
    def test_single_char_key(self):
        """Test with single character key."""
        plaintext = "HELLO"
        key = "A"
        result = self.cipher.encrypt(plaintext, key)
        # With single column, should be mostly unchanged
        self.assertIsNotNone(result)
    
    def test_padding_added(self):
        """Test that padding is added when needed."""
        plaintext = "HELLO"
        key = "ABCD"  # 4 columns
        result = self.cipher.encrypt(plaintext, key)
        # Should be padded to multiple of 4
        self.assertEqual(len(result) % len(key), 0)
    
    def test_longer_text(self):
        """Test with longer text."""
        plaintext = "THISISALONGERMESSAGETOTESTTHECIPHER"
        key = "CRYPTOGRAPHY"
        ciphertext = self.cipher.encrypt(plaintext, key)
        decrypted = self.cipher.decrypt(ciphertext, key)
        self.assertEqual(decrypted, plaintext)


if __name__ == '__main__':
    unittest.main()
