"""
Brute-Force Attack for Caesar Cipher

This module implements brute-force cryptanalysis by trying all possible keys.
"""

from src.ciphers.caesar import CaesarCipher


class CaesarBruteForce:
    """
    Brute-force attack implementation for Caesar cipher.
    
    Tries all possible keys and returns candidate plaintexts.
    """
    
    def __init__(self, alphabet_size=26):
        """
        Initialize the brute-force attack.
        
        Args:
            alphabet_size (int): Size of the alphabet (default: 26)
        """
        self.cipher = CaesarCipher(alphabet_size)
        self.alphabet_size = alphabet_size
    
    def attack(self, ciphertext):
        """
        Perform brute-force attack on ciphertext.
        
        Args:
            ciphertext (str): Encrypted text to attack
            
        Returns:
            list: List of tuples (key, plaintext) for all possible keys
        """
        candidates = []
        
        print(f"\n{'='*70}")
        print("BRUTE-FORCE ATTACK RESULTS")
        print(f"{'='*70}")
        print(f"Trying all {self.alphabet_size} possible keys...\n")
        
        for key in range(self.alphabet_size):
            plaintext = self.cipher.decrypt(ciphertext, key)
            candidates.append((key, plaintext))
            print(f"Key {key:2d}: {plaintext}")
        
        print(f"{'='*70}\n")
        
        return candidates
