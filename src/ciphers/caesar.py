"""
Caesar Cipher Implementation

This module implements the Caesar cipher with support for:
- Encryption and decryption
- Configurable alphabet size (default 26 for English)
- Case preservation
- Handling of non-alphabetic characters
"""


class CaesarCipher:
    """
    Caesar Cipher implementation with configurable alphabet size.
    
    The Caesar cipher is a substitution cipher that shifts letters by a fixed key.
    """
    
    def __init__(self, alphabet_size=26):
        """
        Initialize the Caesar cipher.
        
        Args:
            alphabet_size (int): Size of the alphabet (default: 26 for English)
        """
        self.alphabet_size = alphabet_size
    
    def encrypt(self, plaintext, key):
        """
        Encrypt plaintext using Caesar cipher.
        
        Args:
            plaintext (str): Text to encrypt
            key (int): Shift amount (0 to alphabet_size-1)
            
        Returns:
            str: Encrypted ciphertext
        """
        key = key % self.alphabet_size  # Normalize key
        result = []
        
        for char in plaintext:
            if char.isupper():
                # Encrypt uppercase letters
                shifted = (ord(char) - ord('A') + key) % self.alphabet_size
                result.append(chr(shifted + ord('A')))
            elif char.islower():
                # Encrypt lowercase letters
                shifted = (ord(char) - ord('a') + key) % self.alphabet_size
                result.append(chr(shifted + ord('a')))
            else:
                # Keep non-alphabetic characters unchanged
                result.append(char)
        
        return ''.join(result)
    
    def decrypt(self, ciphertext, key):
        """
        Decrypt ciphertext using Caesar cipher.
        
        Args:
            ciphertext (str): Text to decrypt
            key (int): Shift amount used for encryption
            
        Returns:
            str: Decrypted plaintext
        """
        # Decryption is encryption with negative key
        return self.encrypt(ciphertext, -key)
