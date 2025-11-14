"""Caesar cipher implementation with case preservation and configurable alphabet size."""
from typing import Optional


class CaesarCipher:
    """
    Caesar cipher encryption and decryption with case preservation.
    
    Supports configurable alphabet sizes (default is 26 for English alphabet).
    Preserves case of input characters and ignores non-alphabetic characters.
    """
    
    def __init__(self, alphabet_size: int = 26):
        """
        Initialize the Caesar cipher.
        
        Args:
            alphabet_size: Size of the alphabet (default 26 for English)
        
        Raises:
            ValueError: If alphabet_size is less than 1
        """
        if alphabet_size < 1:
            raise ValueError("Alphabet size must be at least 1")
        self.alphabet_size = alphabet_size
    
    def encrypt(self, plaintext: str, key: int) -> str:
        """
        Encrypt plaintext using Caesar cipher with the given key.
        
        Args:
            plaintext: The text to encrypt
            key: The shift value (can be positive or negative)
        
        Returns:
            The encrypted ciphertext
        """
        if not plaintext:
            return ""
        
        # Normalize key to be within alphabet size
        key = key % self.alphabet_size
        
        result = []
        for char in plaintext:
            if char.isalpha():
                # Determine if uppercase or lowercase
                is_upper = char.isupper()
                base = ord('A') if is_upper else ord('a')
                
                # Shift the character
                shifted = (ord(char) - base + key) % self.alphabet_size
                new_char = chr(base + shifted)
                result.append(new_char)
            else:
                # Non-alphabetic characters are not encrypted
                result.append(char)
        
        return ''.join(result)
    
    def decrypt(self, ciphertext: str, key: int) -> str:
        """
        Decrypt ciphertext using Caesar cipher with the given key.
        
        Args:
            ciphertext: The text to decrypt
            key: The shift value used for encryption
        
        Returns:
            The decrypted plaintext
        """
        # Decryption is just encryption with negative key
        return self.encrypt(ciphertext, -key)
    
    def get_all_keys(self) -> list[int]:
        """
        Get all possible keys for this cipher.
        
        Returns:
            List of all possible keys (0 to alphabet_size - 1)
        """
        return list(range(self.alphabet_size))
