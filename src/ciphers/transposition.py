"""
Columnar Transposition Cipher Implementation

This module implements columnar transposition cipher with support for:
- Encryption and decryption
- Key-based column ordering
- Handling of text padding
"""

import math


class TranspositionCipher:
    """
    Columnar Transposition Cipher implementation.
    
    The transposition cipher rearranges characters according to a key-based column order.
    """
    
    def __init__(self):
        """Initialize the Transposition cipher."""
        pass
    
    def _get_column_order(self, key):
        """
        Get the column ordering based on alphabetical sorting of the key.
        
        Args:
            key (str): The key string
            
        Returns:
            list: Column indices in the order they should be read
        """
        # Create list of (character, original_index) tuples
        indexed_key = [(char, idx) for idx, char in enumerate(key)]
        # Sort by character, keeping original indices
        sorted_key = sorted(indexed_key)
        # Return the original indices in sorted order
        return [idx for char, idx in sorted_key]
    
    def encrypt(self, plaintext, key):
        """
        Encrypt plaintext using columnar transposition.
        
        Args:
            plaintext (str): Text to encrypt
            key (str): Key for column ordering
            
        Returns:
            str: Encrypted ciphertext
        """
        if not key:
            return plaintext
        
        # Remove spaces from plaintext for classic transposition
        plaintext = plaintext.replace(' ', '')
        key_length = len(key)
        
        # Pad plaintext if needed
        padding_needed = (key_length - len(plaintext) % key_length) % key_length
        plaintext += 'X' * padding_needed
        
        # Create grid
        num_rows = math.ceil(len(plaintext) / key_length)
        grid = []
        
        for i in range(num_rows):
            row = []
            for j in range(key_length):
                idx = i * key_length + j
                if idx < len(plaintext):
                    row.append(plaintext[idx])
                else:
                    row.append('X')
            grid.append(row)
        
        # Get column order
        column_order = self._get_column_order(key)
        
        # Read columns in order
        ciphertext = []
        for col_idx in column_order:
            for row in grid:
                ciphertext.append(row[col_idx])
        
        return ''.join(ciphertext)
    
    def decrypt(self, ciphertext, key):
        """
        Decrypt ciphertext using columnar transposition.
        
        Args:
            ciphertext (str): Text to decrypt
            key (str): Key used for encryption
            
        Returns:
            str: Decrypted plaintext
        """
        if not key:
            return ciphertext
        
        key_length = len(key)
        num_rows = math.ceil(len(ciphertext) / key_length)
        
        # Get column order
        column_order = self._get_column_order(key)
        
        # Create empty grid
        grid = [[''] * key_length for _ in range(num_rows)]
        
        # Fill grid column by column in the order specified by key
        idx = 0
        for col_idx in column_order:
            for row in range(num_rows):
                if idx < len(ciphertext):
                    grid[row][col_idx] = ciphertext[idx]
                    idx += 1
        
        # Read grid row by row
        plaintext = []
        for row in grid:
            plaintext.extend(row)
        
        # Remove padding 'X' characters from end
        result = ''.join(plaintext).rstrip('X')
        
        return result
