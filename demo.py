#!/usr/bin/env python3
"""
Demonstration script for the Cryptography System

This script demonstrates all features of the system:
- Caesar cipher encryption/decryption
- Transposition cipher encryption/decryption
- Brute-force attacks with AI recommender
- All four AI scoring methods
"""

from src.ciphers.caesar import CaesarCipher
from src.ciphers.transposition import TranspositionCipher
from src.attacks.caesar_bruteforce import CaesarBruteForce
from src.attacks.transposition_bruteforce import TranspositionBruteForce
from src.ai_recommender.recommender import AIRecommender


def demo_caesar_cipher():
    """Demonstrate Caesar cipher operations."""
    print("\n" + "="*70)
    print("DEMO 1: CAESAR CIPHER ENCRYPTION/DECRYPTION")
    print("="*70 + "\n")
    
    cipher = CaesarCipher()
    
    plaintext = "The Quick Brown Fox Jumps Over The Lazy Dog"
    key = 7
    
    print(f"Original plaintext: {plaintext}")
    print(f"Key: {key}")
    
    ciphertext = cipher.encrypt(plaintext, key)
    print(f"Encrypted: {ciphertext}")
    
    decrypted = cipher.decrypt(ciphertext, key)
    print(f"Decrypted: {decrypted}")
    
    print(f"\nVerification: Original == Decrypted? {plaintext == decrypted}")


def demo_caesar_attack():
    """Demonstrate Caesar cipher brute-force attack."""
    print("\n" + "="*70)
    print("DEMO 2: CAESAR CIPHER BRUTE-FORCE ATTACK WITH AI RECOMMENDER")
    print("="*70 + "\n")
    
    # Create an encrypted message
    cipher = CaesarCipher()
    secret_message = "Meet me at the park at midnight"
    secret_key = 13
    
    ciphertext = cipher.encrypt(secret_message, secret_key)
    print(f"Intercepted ciphertext: {ciphertext}")
    print(f"(Unknown to attacker: key={secret_key})")
    
    # Perform brute-force attack
    bruteforce = CaesarBruteForce()
    print("\nPerforming brute-force attack...")
    candidates = bruteforce.attack(ciphertext)
    
    # Use AI recommender with hybrid method
    recommender = AIRecommender()
    print("Analyzing candidates with AI Recommender (Hybrid Method)...")
    ranked = recommender.analyze_candidates(candidates, method='hybrid', top_n=3)
    recommender.print_analysis(ranked, method='hybrid')
    
    # Show the best result
    best_key, best_plaintext, best_score, _ = ranked[0]
    print(f"AI RECOMMENDATION:")
    print(f"Most likely key: {best_key}")
    print(f"Recovered message: {best_plaintext}")
    print(f"Confidence score: {best_score:.4f}")
    print(f"\nCorrect? {best_key == secret_key}")


def demo_all_ai_methods():
    """Demonstrate all four AI recommender methods."""
    print("\n" + "="*70)
    print("DEMO 3: COMPARING ALL AI RECOMMENDER METHODS")
    print("="*70 + "\n")
    
    cipher = CaesarCipher()
    message = "Attack at dawn"
    key = 5
    
    ciphertext = cipher.encrypt(message, key)
    print(f"Encrypted message: {ciphertext}")
    print(f"Actual key: {key}\n")
    
    bruteforce = CaesarBruteForce()
    candidates = bruteforce.attack(ciphertext)
    
    recommender = AIRecommender()
    
    methods = [
        ('dictionary', 'Method A: Dictionary/Word-Match'),
        ('ngram', 'Method B: N-gram (Quadgram)'),
        ('language_model', 'Method C: Language Model'),
        ('hybrid', 'Method D: Hybrid (Recommended)')
    ]
    
    for method_id, method_name in methods:
        print(f"\n{'-'*70}")
        print(f"{method_name}")
        print(f"{'-'*70}")
        
        ranked = recommender.analyze_candidates(candidates, method=method_id, top_n=1)
        best_key, best_plaintext, best_score, explanation = ranked[0]
        
        print(f"Top candidate: Key {best_key}")
        print(f"Plaintext: {best_plaintext}")
        print(f"Score: {best_score:.4f}")
        print(f"Correct? {best_key == key}")


def demo_transposition_cipher():
    """Demonstrate Transposition cipher operations."""
    print("\n" + "="*70)
    print("DEMO 4: TRANSPOSITION CIPHER ENCRYPTION/DECRYPTION")
    print("="*70 + "\n")
    
    cipher = TranspositionCipher()
    
    plaintext = "DEFENDTHEEASTWALLOFTHECASTLE"
    key = "ZEBRAS"
    
    print(f"Original plaintext: {plaintext}")
    print(f"Key: {key}")
    
    ciphertext = cipher.encrypt(plaintext, key)
    print(f"Encrypted: {ciphertext}")
    
    decrypted = cipher.decrypt(ciphertext, key)
    print(f"Decrypted: {decrypted}")
    
    print(f"\nVerification: Original == Decrypted? {plaintext == decrypted}")


def demo_transposition_attack():
    """Demonstrate Transposition cipher attack."""
    print("\n" + "="*70)
    print("DEMO 5: TRANSPOSITION CIPHER ATTACK")
    print("="*70 + "\n")
    
    cipher = TranspositionCipher()
    secret_message = "THISISASECRETMESSAGE"
    secret_key = "CAT"
    
    ciphertext = cipher.encrypt(secret_message, secret_key)
    print(f"Intercepted ciphertext: {ciphertext}")
    print(f"(Unknown to attacker: key='{secret_key}')")
    
    # Perform attack
    bruteforce = TranspositionBruteForce(max_key_length=5)
    print("\nPerforming heuristic attack (trying key lengths 2-5)...")
    candidates = bruteforce.attack(ciphertext, max_keys_per_length=6)
    
    if candidates:
        # Use AI recommender
        recommender = AIRecommender()
        print("\nAnalyzing candidates with AI Recommender...")
        ranked = recommender.analyze_candidates(candidates, method='hybrid', top_n=3)
        recommender.print_analysis(ranked, method='hybrid')
        
        best_key, best_plaintext, best_score, _ = ranked[0]
        print(f"AI RECOMMENDATION:")
        print(f"Most likely key: {best_key}")
        print(f"Recovered message: {best_plaintext}")


def demo_edge_cases():
    """Demonstrate edge cases and special features."""
    print("\n" + "="*70)
    print("DEMO 6: SPECIAL FEATURES AND EDGE CASES")
    print("="*70 + "\n")
    
    cipher = CaesarCipher()
    
    # Test with numbers and punctuation
    print("1. Mixed content (letters, numbers, punctuation):")
    text = "Password123! is my secret."
    encrypted = cipher.encrypt(text, 10)
    print(f"   Original:  {text}")
    print(f"   Encrypted: {encrypted}")
    print(f"   Note: Only letters are encrypted, numbers/punctuation preserved\n")
    
    # Test case preservation
    print("2. Case preservation:")
    text = "HeLLo WoRLd"
    encrypted = cipher.encrypt(text, 5)
    print(f"   Original:  {text}")
    print(f"   Encrypted: {encrypted}")
    print(f"   Note: Original case is maintained\n")
    
    # Test wraparound
    print("3. Alphabet wraparound:")
    text = "XYZ"
    encrypted = cipher.encrypt(text, 5)
    print(f"   Original:  {text}")
    print(f"   Encrypted: {encrypted}")
    print(f"   Note: Z+5 wraps around to C\n")
    
    # Test key normalization
    print("4. Key normalization:")
    text = "HELLO"
    e1 = cipher.encrypt(text, 3)
    e2 = cipher.encrypt(text, 29)  # 29 % 26 = 3
    print(f"   Original:  {text}")
    print(f"   Key 3:     {e1}")
    print(f"   Key 29:    {e2}")
    print(f"   Note: Key 29 is equivalent to key 3 (29 mod 26 = 3)\n")


def main():
    """Run all demonstrations."""
    print("\n" + "="*70)
    print(" "*15 + "CRYPTOGRAPHY SYSTEM DEMONSTRATION")
    print(" "*20 + "Complete Feature Showcase")
    print("="*70)
    
    demo_caesar_cipher()
    demo_caesar_attack()
    demo_all_ai_methods()
    demo_transposition_cipher()
    demo_transposition_attack()
    demo_edge_cases()
    
    print("\n" + "="*70)
    print("DEMONSTRATION COMPLETE")
    print("="*70)
    print("\nTo use the interactive menu system, run:")
    print("  python main.py")
    print("\nFor more information, see README.md")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
