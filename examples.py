#!/usr/bin/env python
"""
Example demonstrations of the cipher cryptanalysis system.

This script shows various use cases of the cipher cryptanalysis package.
"""

from cipher_cryptanalysis import (
    CaesarCipher,
    TranspositionCipher,
    BruteForceAttack,
    PlaintextRanker
)


def demo_caesar_basic():
    """Demonstrate basic Caesar cipher usage."""
    print("=" * 60)
    print("DEMO 1: Caesar Cipher - Basic Usage")
    print("=" * 60)
    
    cipher = CaesarCipher()
    plaintext = "The quick brown fox jumps over the lazy dog"
    key = 7
    
    print(f"Original: {plaintext}")
    print(f"Key: {key}")
    
    ciphertext = cipher.encrypt(plaintext, key)
    print(f"Encrypted: {ciphertext}")
    
    decrypted = cipher.decrypt(ciphertext, key)
    print(f"Decrypted: {decrypted}")
    print()


def demo_caesar_attack():
    """Demonstrate Caesar cipher brute force attack with AI ranking."""
    print("=" * 60)
    print("DEMO 2: Caesar Cipher - Brute Force Attack with AI Ranking")
    print("=" * 60)
    
    # Create a ciphertext
    cipher = CaesarCipher()
    original_text = "Attack at dawn"
    secret_key = 13
    ciphertext = cipher.encrypt(original_text, secret_key)
    
    print(f"Ciphertext to attack: {ciphertext}")
    print(f"(Original was: '{original_text}' with key {secret_key})")
    print()
    
    # Perform attack
    attack = BruteForceAttack()
    ranker = PlaintextRanker(scoring_method='hybrid')
    
    results = attack.attack_with_ranker(
        ciphertext,
        'caesar',
        ranker.score,
        top_n=5,
        alphabet_size=26
    )
    
    print("Top 5 candidates:")
    for i, (key, plaintext, score) in enumerate(results, 1):
        marker = " ← CORRECT!" if key == secret_key else ""
        print(f"{i}. Key {key:2d} (score: {score:.4f}): {plaintext}{marker}")
    print()


def demo_caesar_scoring_methods():
    """Demonstrate different scoring methods."""
    print("=" * 60)
    print("DEMO 3: Caesar Cipher - Different Scoring Methods")
    print("=" * 60)
    
    cipher = CaesarCipher()
    plaintext = "Hello World"
    key = 3
    ciphertext = cipher.encrypt(plaintext, key)
    
    print(f"Ciphertext: {ciphertext}")
    print()
    
    attack = BruteForceAttack()
    methods = ['dictionary', 'bigram', 'trigram', 'frequency', 'hybrid']
    
    for method in methods:
        ranker = PlaintextRanker(scoring_method=method)
        results = attack.attack_with_ranker(
            ciphertext,
            'caesar',
            ranker.score,
            top_n=1,
            alphabet_size=26
        )
        
        best_key, best_text, best_score = results[0]
        correct = "✓" if best_key == key else "✗"
        print(f"{method:12s}: Key {best_key:2d} (score: {best_score:.4f}) {correct}")
    print()


def demo_transposition_basic():
    """Demonstrate basic Transposition cipher usage."""
    print("=" * 60)
    print("DEMO 4: Transposition Cipher - Basic Usage")
    print("=" * 60)
    
    cipher = TranspositionCipher()
    plaintext = "Meet me at the park"
    key = 4
    
    print(f"Original: {plaintext}")
    print(f"Key: {key}")
    
    ciphertext = cipher.encrypt(plaintext, key)
    print(f"Encrypted: {ciphertext}")
    
    decrypted = cipher.decrypt(ciphertext, key)
    print(f"Decrypted: {decrypted.strip()}")
    print()


def demo_transposition_attack():
    """Demonstrate Transposition cipher attack."""
    print("=" * 60)
    print("DEMO 5: Transposition Cipher - Brute Force Attack")
    print("=" * 60)
    
    # Create a ciphertext
    cipher = TranspositionCipher()
    original_text = "The secret message is hidden here"
    secret_key = 6
    ciphertext = cipher.encrypt(original_text, secret_key)
    
    print(f"Ciphertext to attack: {ciphertext}")
    print(f"(Original was: '{original_text}' with key {secret_key})")
    print()
    
    # Perform attack
    attack = BruteForceAttack()
    ranker = PlaintextRanker(scoring_method='hybrid')
    
    results = attack.attack_with_ranker(
        ciphertext,
        'transposition',
        ranker.score,
        top_n=5,
        max_key=10
    )
    
    print("Top 5 candidates:")
    for i, (key, plaintext, score) in enumerate(results, 1):
        marker = " ← CORRECT!" if key == secret_key else ""
        print(f"{i}. Key {key:2d} (score: {score:.4f}): {plaintext.strip()}{marker}")
    print()


def demo_explainable_ranking():
    """Demonstrate explainable AI ranking."""
    print("=" * 60)
    print("DEMO 6: Explainable AI Ranking")
    print("=" * 60)
    
    cipher = CaesarCipher()
    plaintext = "This is a test"
    key = 5
    ciphertext = cipher.encrypt(plaintext, key)
    
    print(f"Ciphertext: {ciphertext}")
    print()
    
    # Get candidates
    attack = BruteForceAttack()
    candidates = attack.attack_caesar(ciphertext)
    
    # Rank with explanation
    ranker = PlaintextRanker(scoring_method='hybrid')
    results = ranker.rank_with_explanation(candidates, top_n=3)
    
    print("Top 3 candidates with detailed explanations:")
    print()
    
    for i, result in enumerate(results, 1):
        print(f"{i}. Key {result['key']:2d}: {result['plaintext']}")
        print(f"   Overall Score: {result['score']:.4f}")
        print(f"   Breakdown:")
        for method, score in result['explanation'].items():
            print(f"     - {method:12s}: {score:.4f}")
        print()


def main():
    """Run all demonstrations."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  Cipher Cryptanalysis System - Demonstrations".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    demos = [
        demo_caesar_basic,
        demo_caesar_attack,
        demo_caesar_scoring_methods,
        demo_transposition_basic,
        demo_transposition_attack,
        demo_explainable_ranking,
    ]
    
    for demo in demos:
        demo()
        input("Press Enter to continue to next demo...")
        print("\n")
    
    print("=" * 60)
    print("All demonstrations completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
