"""Brute force attack implementation for ciphers."""
from typing import List, Tuple, Callable
from ..ciphers.caesar import CaesarCipher
from ..ciphers.transposition import TranspositionCipher


class BruteForceAttack:
    """
    Brute force attack implementation that tries all possible keys.
    
    Works with both Caesar and Transposition ciphers.
    """
    
    def __init__(self):
        """Initialize the brute force attack."""
        pass
    
    def attack_caesar(
        self,
        ciphertext: str,
        alphabet_size: int = 26
    ) -> List[Tuple[int, str]]:
        """
        Perform brute force attack on Caesar cipher.
        
        Tries all possible keys and returns all decryption results.
        
        Args:
            ciphertext: The encrypted text to attack
            alphabet_size: Size of the alphabet used in encryption
        
        Returns:
            List of tuples (key, decrypted_text) for all possible keys
        """
        cipher = CaesarCipher(alphabet_size=alphabet_size)
        results = []
        
        for key in cipher.get_all_keys():
            decrypted = cipher.decrypt(ciphertext, key)
            results.append((key, decrypted))
        
        return results
    
    def attack_transposition(
        self,
        ciphertext: str,
        max_key: int = 20
    ) -> List[Tuple[int, str]]:
        """
        Perform brute force attack on Transposition cipher.
        
        Tries possible keys up to max_key and returns all decryption results.
        
        Args:
            ciphertext: The encrypted text to attack
            max_key: Maximum key value to try
        
        Returns:
            List of tuples (key, decrypted_text) for all attempted keys
        """
        cipher = TranspositionCipher()
        results = []
        
        possible_keys = cipher.get_possible_keys(len(ciphertext), max_key)
        
        for key in possible_keys:
            try:
                decrypted = cipher.decrypt(ciphertext, key)
                results.append((key, decrypted))
            except Exception:
                # Skip invalid keys
                continue
        
        return results
    
    def attack_with_ranker(
        self,
        ciphertext: str,
        cipher_type: str,
        ranker: Callable,
        top_n: int = 5,
        **kwargs
    ) -> List[Tuple[int, str, float]]:
        """
        Perform brute force attack and rank results using a plaintext ranker.
        
        Args:
            ciphertext: The encrypted text to attack
            cipher_type: Type of cipher ('caesar' or 'transposition')
            ranker: A callable that scores plaintext (higher is better)
            top_n: Number of top results to return
            **kwargs: Additional arguments for the attack (alphabet_size, max_key, etc.)
        
        Returns:
            List of tuples (key, decrypted_text, score) for top N results
        """
        # Perform brute force attack
        if cipher_type.lower() == 'caesar':
            alphabet_size = kwargs.get('alphabet_size', 26)
            results = self.attack_caesar(ciphertext, alphabet_size)
        elif cipher_type.lower() == 'transposition':
            max_key = kwargs.get('max_key', 20)
            results = self.attack_transposition(ciphertext, max_key)
        else:
            raise ValueError(f"Unknown cipher type: {cipher_type}")
        
        # Score each result
        scored_results = []
        for key, plaintext in results:
            score = ranker(plaintext)
            scored_results.append((key, plaintext, score))
        
        # Sort by score (descending) and return top N
        scored_results.sort(key=lambda x: x[2], reverse=True)
        return scored_results[:top_n]
