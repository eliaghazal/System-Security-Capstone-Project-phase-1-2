#!/usr/bin/env python3
"""
System Security Capstone Project - Interactive CLI
Main entry point for the cryptography system

This interactive menu allows users to:
- Encrypt/decrypt with Caesar cipher
- Encrypt/decrypt with Transposition cipher
- Perform brute-force attacks
- Use AI recommender to find best plaintext candidates
"""

import sys
from src.ciphers.caesar import CaesarCipher
from src.ciphers.transposition import TranspositionCipher
from src.attacks.caesar_bruteforce import CaesarBruteForce
from src.attacks.transposition_bruteforce import TranspositionBruteForce
from src.ai_recommender.recommender import AIRecommender


class CryptoSystem:
    """Main interactive cryptography system."""
    
    def __init__(self):
        """Initialize the crypto system."""
        self.caesar = CaesarCipher()
        self.transposition = TranspositionCipher()
        self.recommender = AIRecommender()
    
    def print_banner(self):
        """Print welcome banner."""
        print("\n" + "="*70)
        print(" " * 15 + "SYSTEM SECURITY CAPSTONE PROJECT")
        print(" " * 20 + "Cryptography System v1.0")
        print("="*70 + "\n")
    
    def main_menu(self):
        """Display main menu and get user choice."""
        print("\n" + "-"*70)
        print("MAIN MENU")
        print("-"*70)
        print("1. Caesar Cipher Operations")
        print("2. Transposition Cipher Operations")
        print("3. Exit")
        print("-"*70)
        
        while True:
            choice = input("\nEnter your choice (1-3): ").strip()
            if choice in ['1', '2', '3']:
                return choice
            print("Invalid choice. Please enter 1, 2, or 3.")
    
    def caesar_menu(self):
        """Display Caesar cipher menu."""
        print("\n" + "-"*70)
        print("CAESAR CIPHER MENU")
        print("-"*70)
        print("1. Encrypt text")
        print("2. Decrypt text")
        print("3. Brute-force attack (with AI recommender)")
        print("4. Back to main menu")
        print("-"*70)
        
        while True:
            choice = input("\nEnter your choice (1-4): ").strip()
            if choice in ['1', '2', '3', '4']:
                return choice
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
    
    def transposition_menu(self):
        """Display Transposition cipher menu."""
        print("\n" + "-"*70)
        print("TRANSPOSITION CIPHER MENU")
        print("-"*70)
        print("1. Encrypt text")
        print("2. Decrypt text")
        print("3. Brute-force attack (with AI recommender)")
        print("4. Back to main menu")
        print("-"*70)
        
        while True:
            choice = input("\nEnter your choice (1-4): ").strip()
            if choice in ['1', '2', '3', '4']:
                return choice
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
    
    def caesar_encrypt(self):
        """Handle Caesar cipher encryption."""
        print("\n" + "="*70)
        print("CAESAR CIPHER - ENCRYPTION")
        print("="*70)
        
        plaintext = input("\nEnter plaintext to encrypt: ").strip()
        
        while True:
            try:
                key = int(input("Enter shift key (0-25): ").strip())
                if 0 <= key <= 25:
                    break
                print("Key must be between 0 and 25.")
            except ValueError:
                print("Please enter a valid number.")
        
        ciphertext = self.caesar.encrypt(plaintext, key)
        
        print(f"\nPlaintext:  {plaintext}")
        print(f"Key:        {key}")
        print(f"Ciphertext: {ciphertext}")
        print("="*70)
    
    def caesar_decrypt(self):
        """Handle Caesar cipher decryption."""
        print("\n" + "="*70)
        print("CAESAR CIPHER - DECRYPTION")
        print("="*70)
        
        ciphertext = input("\nEnter ciphertext to decrypt: ").strip()
        
        while True:
            try:
                key = int(input("Enter shift key (0-25): ").strip())
                if 0 <= key <= 25:
                    break
                print("Key must be between 0 and 25.")
            except ValueError:
                print("Please enter a valid number.")
        
        plaintext = self.caesar.decrypt(ciphertext, key)
        
        print(f"\nCiphertext: {ciphertext}")
        print(f"Key:        {key}")
        print(f"Plaintext:  {plaintext}")
        print("="*70)
    
    def caesar_attack(self):
        """Handle Caesar cipher brute-force attack with AI recommender."""
        print("\n" + "="*70)
        print("CAESAR CIPHER - BRUTE-FORCE ATTACK")
        print("="*70)
        
        ciphertext = input("\nEnter ciphertext to attack: ").strip()
        
        # Perform brute-force attack
        bruteforce = CaesarBruteForce()
        candidates = bruteforce.attack(ciphertext)
        
        # Get AI recommender method choice
        print("\nAI Recommender Methods:")
        print("1. Dictionary/word-match scoring (Method A)")
        print("2. N-gram (quadgram) scoring (Method B)")
        print("3. Language model scoring (Method C)")
        print("4. Hybrid (ALL methods combined) (Method D) - RECOMMENDED")
        
        while True:
            method_choice = input("\nSelect AI method (1-4, default=4): ").strip()
            if not method_choice:
                method_choice = '4'
            if method_choice in ['1', '2', '3', '4']:
                break
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
        
        method_map = {
            '1': 'dictionary',
            '2': 'ngram',
            '3': 'language_model',
            '4': 'hybrid'
        }
        method = method_map[method_choice]
        
        # Analyze with AI recommender
        ranked = self.recommender.analyze_candidates(candidates, method=method, top_n=5)
        self.recommender.print_analysis(ranked, method=method)
        
        if ranked:
            best_key, best_plaintext, best_score, _ = ranked[0]
            print(f"BEST CANDIDATE: Key={best_key}, Score={best_score:.4f}")
            print(f"Plaintext: {best_plaintext}")
            print("="*70)
    
    def transposition_encrypt(self):
        """Handle Transposition cipher encryption."""
        print("\n" + "="*70)
        print("TRANSPOSITION CIPHER - ENCRYPTION")
        print("="*70)
        
        plaintext = input("\nEnter plaintext to encrypt: ").strip()
        key = input("Enter key (e.g., 'CRYPTO'): ").strip()
        
        if not key:
            print("Key cannot be empty!")
            return
        
        ciphertext = self.transposition.encrypt(plaintext, key)
        
        print(f"\nPlaintext:  {plaintext}")
        print(f"Key:        {key}")
        print(f"Ciphertext: {ciphertext}")
        print("="*70)
    
    def transposition_decrypt(self):
        """Handle Transposition cipher decryption."""
        print("\n" + "="*70)
        print("TRANSPOSITION CIPHER - DECRYPTION")
        print("="*70)
        
        ciphertext = input("\nEnter ciphertext to decrypt: ").strip()
        key = input("Enter key used for encryption: ").strip()
        
        if not key:
            print("Key cannot be empty!")
            return
        
        plaintext = self.transposition.decrypt(ciphertext, key)
        
        print(f"\nCiphertext: {ciphertext}")
        print(f"Key:        {key}")
        print(f"Plaintext:  {plaintext}")
        print("="*70)
    
    def transposition_attack(self):
        """Handle Transposition cipher attack with AI recommender."""
        print("\n" + "="*70)
        print("TRANSPOSITION CIPHER - BRUTE-FORCE ATTACK")
        print("="*70)
        
        ciphertext = input("\nEnter ciphertext to attack: ").strip()
        
        print("\nNote: This attack tries different key lengths and permutations.")
        print("For long keys, this can be computationally expensive.\n")
        
        while True:
            try:
                max_length = int(input("Maximum key length to try (2-8 recommended): ").strip())
                if 2 <= max_length <= 10:
                    break
                print("Please enter a value between 2 and 10.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Perform brute-force attack
        bruteforce = TranspositionBruteForce(max_key_length=max_length)
        candidates = bruteforce.attack(ciphertext, max_keys_per_length=10)
        
        if not candidates:
            print("\nNo candidates found. Try a different key length range.")
            return
        
        # Get AI recommender method
        print("\nAI Recommender Methods:")
        print("1. Dictionary/word-match scoring")
        print("2. N-gram (quadgram) scoring")
        print("3. Language model scoring")
        print("4. Hybrid (ALL methods combined) - RECOMMENDED")
        
        while True:
            method_choice = input("\nSelect AI method (1-4, default=4): ").strip()
            if not method_choice:
                method_choice = '4'
            if method_choice in ['1', '2', '3', '4']:
                break
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
        
        method_map = {
            '1': 'dictionary',
            '2': 'ngram',
            '3': 'language_model',
            '4': 'hybrid'
        }
        method = method_map[method_choice]
        
        # Analyze with AI recommender
        ranked = self.recommender.analyze_candidates(candidates, method=method, top_n=5)
        self.recommender.print_analysis(ranked, method=method)
        
        if ranked:
            best_key, best_plaintext, best_score, _ = ranked[0]
            print(f"BEST CANDIDATE: Key={best_key}, Score={best_score:.4f}")
            print(f"Plaintext: {best_plaintext}")
            print("="*70)
    
    def run(self):
        """Run the main interactive loop."""
        self.print_banner()
        
        while True:
            main_choice = self.main_menu()
            
            if main_choice == '1':
                # Caesar cipher operations
                while True:
                    caesar_choice = self.caesar_menu()
                    
                    if caesar_choice == '1':
                        self.caesar_encrypt()
                    elif caesar_choice == '2':
                        self.caesar_decrypt()
                    elif caesar_choice == '3':
                        self.caesar_attack()
                    elif caesar_choice == '4':
                        break
            
            elif main_choice == '2':
                # Transposition cipher operations
                while True:
                    trans_choice = self.transposition_menu()
                    
                    if trans_choice == '1':
                        self.transposition_encrypt()
                    elif trans_choice == '2':
                        self.transposition_decrypt()
                    elif trans_choice == '3':
                        self.transposition_attack()
                    elif trans_choice == '4':
                        break
            
            elif main_choice == '3':
                print("\n" + "="*70)
                print("Thank you for using the Cryptography System!")
                print("="*70 + "\n")
                sys.exit(0)


def main():
    """Main entry point."""
    try:
        system = CryptoSystem()
        system.run()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
