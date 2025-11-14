"""Transposition cipher implementation."""
import math
from typing import Optional


class TranspositionCipher:
    """
    Columnar transposition cipher encryption and decryption.
    
    Uses a key to determine the order of columns when reading the ciphertext.
    """
    
    def __init__(self):
        """Initialize the transposition cipher."""
        pass
    
    def encrypt(self, plaintext: str, key: int) -> str:
        """
        Encrypt plaintext using columnar transposition cipher.
        
        Args:
            plaintext: The text to encrypt
            key: The number of columns to use
        
        Returns:
            The encrypted ciphertext
        
        Raises:
            ValueError: If key is less than 1
        """
        if key < 1:
            raise ValueError("Key must be at least 1")
        
        if not plaintext:
            return ""
        
        # Create the grid
        num_cols = key
        num_rows = math.ceil(len(plaintext) / num_cols)
        
        # Pad the plaintext if necessary
        padded_length = num_rows * num_cols
        plaintext_padded = plaintext.ljust(padded_length)
        
        # Fill the grid row by row
        grid = []
        for i in range(num_rows):
            start = i * num_cols
            end = start + num_cols
            grid.append(list(plaintext_padded[start:end]))
        
        # Read the grid column by column
        ciphertext = []
        for col in range(num_cols):
            for row in range(num_rows):
                ciphertext.append(grid[row][col])
        
        return ''.join(ciphertext)
    
    def decrypt(self, ciphertext: str, key: int) -> str:
        """
        Decrypt ciphertext using columnar transposition cipher.
        
        Args:
            ciphertext: The text to decrypt
            key: The number of columns used for encryption
        
        Returns:
            The decrypted plaintext
        
        Raises:
            ValueError: If key is less than 1
        """
        if key < 1:
            raise ValueError("Key must be at least 1")
        
        if not ciphertext:
            return ""
        
        # Calculate dimensions
        num_cols = key
        num_rows = math.ceil(len(ciphertext) / num_cols)
        
        # Create the grid
        grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]
        
        # Fill the grid column by column
        idx = 0
        for col in range(num_cols):
            for row in range(num_rows):
                if idx < len(ciphertext):
                    grid[row][col] = ciphertext[idx]
                    idx += 1
        
        # Read the grid row by row
        plaintext = []
        for row in range(num_rows):
            for col in range(num_cols):
                plaintext.append(grid[row][col])
        
        return ''.join(plaintext).rstrip()
    
    def get_possible_keys(self, ciphertext_length: int, max_key: int = 20) -> list[int]:
        """
        Get possible keys for a given ciphertext length.
        
        Args:
            ciphertext_length: Length of the ciphertext
            max_key: Maximum key to consider
        
        Returns:
            List of possible keys
        """
        if ciphertext_length <= 1:
            return [1]
        
        # Try keys from 2 to min(ciphertext_length, max_key)
        return list(range(2, min(ciphertext_length + 1, max_key + 1)))
