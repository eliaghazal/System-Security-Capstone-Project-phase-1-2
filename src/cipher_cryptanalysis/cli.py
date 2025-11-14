"""Command-line interface for cipher cryptanalysis tool."""
import argparse
import sys
from typing import Optional
from cipher_cryptanalysis.ciphers import CaesarCipher, TranspositionCipher
from cipher_cryptanalysis.attacks import BruteForceAttack
from cipher_cryptanalysis.recommender import PlaintextRanker


def caesar_encrypt(args):
    """Encrypt text using Caesar cipher."""
    cipher = CaesarCipher(alphabet_size=args.alphabet_size)
    result = cipher.encrypt(args.text, args.key)
    print(f"Encrypted: {result}")


def caesar_decrypt(args):
    """Decrypt text using Caesar cipher."""
    cipher = CaesarCipher(alphabet_size=args.alphabet_size)
    result = cipher.decrypt(args.text, args.key)
    print(f"Decrypted: {result}")


def caesar_attack(args):
    """Perform brute force attack on Caesar cipher."""
    attack = BruteForceAttack()
    ranker = PlaintextRanker(scoring_method=args.scoring_method)
    
    print(f"Attacking Caesar cipher with {args.scoring_method} scoring...")
    print(f"Ciphertext: {args.text}\n")
    
    results = attack.attack_with_ranker(
        args.text,
        'caesar',
        ranker.score,
        top_n=args.top_n,
        alphabet_size=args.alphabet_size
    )
    
    print(f"Top {len(results)} candidates:\n")
    for i, (key, plaintext, score) in enumerate(results, 1):
        print(f"{i}. Key {key:2d} (score: {score:.4f}): {plaintext}")
        
        if args.explain:
            explanation = ranker.explain_score(plaintext)
            print(f"   Explanation:")
            for method, method_score in explanation.items():
                print(f"     {method:12s}: {method_score:.4f}")
            print()


def transposition_encrypt(args):
    """Encrypt text using Transposition cipher."""
    cipher = TranspositionCipher()
    result = cipher.encrypt(args.text, args.key)
    print(f"Encrypted: {result}")


def transposition_decrypt(args):
    """Decrypt text using Transposition cipher."""
    cipher = TranspositionCipher()
    result = cipher.decrypt(args.text, args.key)
    print(f"Decrypted: {result}")


def transposition_attack(args):
    """Perform brute force attack on Transposition cipher."""
    attack = BruteForceAttack()
    ranker = PlaintextRanker(scoring_method=args.scoring_method)
    
    print(f"Attacking Transposition cipher with {args.scoring_method} scoring...")
    print(f"Ciphertext: {args.text}\n")
    
    results = attack.attack_with_ranker(
        args.text,
        'transposition',
        ranker.score,
        top_n=args.top_n,
        max_key=args.max_key
    )
    
    print(f"Top {len(results)} candidates:\n")
    for i, (key, plaintext, score) in enumerate(results, 1):
        print(f"{i}. Key {key:2d} (score: {score:.4f}): {plaintext}")
        
        if args.explain:
            explanation = ranker.explain_score(plaintext)
            print(f"   Explanation:")
            for method, method_score in explanation.items():
                print(f"     {method:12s}: {method_score:.4f}")
            print()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Cipher Cryptanalysis Tool - Encrypt, decrypt, and attack ciphers with AI-based ranking'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Caesar cipher commands
    caesar_parser = subparsers.add_parser('caesar', help='Caesar cipher operations')
    caesar_subparsers = caesar_parser.add_subparsers(dest='operation', help='Caesar operations')
    
    # Caesar encrypt
    caesar_enc = caesar_subparsers.add_parser('encrypt', help='Encrypt text')
    caesar_enc.add_argument('text', help='Text to encrypt')
    caesar_enc.add_argument('key', type=int, help='Encryption key (shift value)')
    caesar_enc.add_argument('--alphabet-size', type=int, default=26, 
                           help='Alphabet size (default: 26)')
    caesar_enc.set_defaults(func=caesar_encrypt)
    
    # Caesar decrypt
    caesar_dec = caesar_subparsers.add_parser('decrypt', help='Decrypt text')
    caesar_dec.add_argument('text', help='Text to decrypt')
    caesar_dec.add_argument('key', type=int, help='Decryption key (shift value)')
    caesar_dec.add_argument('--alphabet-size', type=int, default=26,
                           help='Alphabet size (default: 26)')
    caesar_dec.set_defaults(func=caesar_decrypt)
    
    # Caesar attack
    caesar_atk = caesar_subparsers.add_parser('attack', help='Brute force attack')
    caesar_atk.add_argument('text', help='Ciphertext to attack')
    caesar_atk.add_argument('--alphabet-size', type=int, default=26,
                           help='Alphabet size (default: 26)')
    caesar_atk.add_argument('--scoring-method', 
                           choices=['dictionary', 'bigram', 'trigram', 'frequency', 
                                   'perplexity', 'hybrid'],
                           default='hybrid',
                           help='Scoring method for ranking (default: hybrid)')
    caesar_atk.add_argument('--top-n', type=int, default=5,
                           help='Number of top candidates to show (default: 5)')
    caesar_atk.add_argument('--explain', action='store_true',
                           help='Show detailed scoring explanation')
    caesar_atk.set_defaults(func=caesar_attack)
    
    # Transposition cipher commands
    trans_parser = subparsers.add_parser('transposition', help='Transposition cipher operations')
    trans_subparsers = trans_parser.add_subparsers(dest='operation', help='Transposition operations')
    
    # Transposition encrypt
    trans_enc = trans_subparsers.add_parser('encrypt', help='Encrypt text')
    trans_enc.add_argument('text', help='Text to encrypt')
    trans_enc.add_argument('key', type=int, help='Encryption key (number of columns)')
    trans_enc.set_defaults(func=transposition_encrypt)
    
    # Transposition decrypt
    trans_dec = trans_subparsers.add_parser('decrypt', help='Decrypt text')
    trans_dec.add_argument('text', help='Text to decrypt')
    trans_dec.add_argument('key', type=int, help='Decryption key (number of columns)')
    trans_dec.set_defaults(func=transposition_decrypt)
    
    # Transposition attack
    trans_atk = trans_subparsers.add_parser('attack', help='Brute force attack')
    trans_atk.add_argument('text', help='Ciphertext to attack')
    trans_atk.add_argument('--max-key', type=int, default=20,
                          help='Maximum key to try (default: 20)')
    trans_atk.add_argument('--scoring-method',
                          choices=['dictionary', 'bigram', 'trigram', 'frequency',
                                  'perplexity', 'hybrid'],
                          default='hybrid',
                          help='Scoring method for ranking (default: hybrid)')
    trans_atk.add_argument('--top-n', type=int, default=5,
                          help='Number of top candidates to show (default: 5)')
    trans_atk.add_argument('--explain', action='store_true',
                          help='Show detailed scoring explanation')
    trans_atk.set_defaults(func=transposition_attack)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    if hasattr(args, 'func'):
        args.func(args)
        return 0
    else:
        if args.command == 'caesar':
            caesar_parser.print_help()
        elif args.command == 'transposition':
            trans_parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
