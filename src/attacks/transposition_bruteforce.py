"""
Brute-Force and Heuristic Attack for Transposition Cipher

This module implements cryptanalysis for columnar transposition cipher.
"""

from src.ciphers.transposition import TranspositionCipher
import itertools


class TranspositionBruteForce:
    """
    Brute-force and heuristic attack for transposition cipher.
    
    Tries different key lengths and column orderings.
    """
    
    def __init__(self, max_key_length=10):
        """
        Initialize the attack.
        
        Args:
            max_key_length (int): Maximum key length to try
        """
        self.cipher = TranspositionCipher()
        self.max_key_length = max_key_length
    
    def attack(self, ciphertext, max_keys_per_length=10):
        """
        Perform brute-force attack with heuristics.
        
        Args:
            ciphertext (str): Encrypted text to attack
            max_keys_per_length (int): Maximum number of key permutations to try per length
            
        Returns:
            list: List of tuples (key, plaintext, score)
        """
        candidates = []
        
        print(f"\n{'='*70}")
        print("TRANSPOSITION BRUTE-FORCE ATTACK")
        print(f"{'='*70}")
        
        # Try different key lengths
        for key_length in range(2, min(self.max_key_length + 1, len(ciphertext) + 1)):
            print(f"\nTrying key length {key_length}...")
            
            # Generate sample keys (limited to avoid explosion)
            # Use alphabetic keys like "ABC", "BAC", etc.
            base_key = ''.join([chr(ord('A') + i) for i in range(key_length)])
            
            # Try a subset of permutations
            count = 0
            for perm in itertools.permutations(base_key):
                if count >= max_keys_per_length:
                    break
                
                key = ''.join(perm)
                try:
                    plaintext = self.cipher.decrypt(ciphertext, key)
                    candidates.append((key, plaintext))
                    print(f"  Key '{key}': {plaintext[:50]}...")
                    count += 1
                except Exception as e:
                    continue
        
        print(f"{'='*70}\n")
        
        return candidates
