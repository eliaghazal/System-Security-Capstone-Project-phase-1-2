# System Security Capstone Project - Phase 1 & 2

A comprehensive cryptography system implementing classical ciphers with AI-powered cryptanalysis.

## Project Overview

This project implements a complete, well-documented software system for cryptographic operations and analysis, designed for educational purposes in system security.

### Features

#### Phase 1: Caesar Cipher
- **Encryption/Decryption**: Full implementation with configurable alphabet size
- **Case Preservation**: Maintains original letter casing
- **Brute-Force Attack**: Tries all possible keys (0-25)
- **AI Recommender**: Intelligent analysis of plaintext candidates using multiple methods

#### Phase 2: Transposition Cipher
- **Columnar Transposition**: Key-based column reordering
- **Encryption/Decryption**: Complete implementation with padding
- **Brute-Force Attack**: Heuristic-based key discovery
- **AI Recommender**: Extended support for transposition analysis

### AI Recommender Methods

The AI recommender implements **all four methods** as required, combining them for robust cryptanalysis:

#### Method A: Dictionary/Word-Match Scoring
- Tokenizes candidate plaintext into words
- Compares against English word frequency list
- Scores based on matched words and their frequencies
- **Pros**: Simple, interpretable, fast
- **Cons**: May fail on short texts or proper nouns

#### Method B: N-gram (Quadgram) Log-Likelihood Scoring
- Uses precomputed English quadgram frequencies
- Calculates log probability for each candidate
- Ranks by likelihood of being English text
- **Pros**: Strong for short or noisy texts
- **Cons**: Requires frequency table

#### Method C: Language Model Scoring
- Character and bigram frequency analysis
- Lightweight perplexity-based scoring
- Reproducible without external model downloads
- **Pros**: Good performance, no dependencies
- **Cons**: Less sophisticated than full LMs

#### Method D: Hybrid Heuristic (RECOMMENDED)
- Combines all three methods with configurable weights
- Default: α=0.35 (dictionary), β=0.35 (n-gram), γ=0.30 (LM)
- Provides component-level explanations
- **Best overall accuracy and robustness**

All methods are fully documented in the code with comments explaining which method is used.

## Installation

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses Python standard library only)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/eliaghazal/System-Security-Capstone-Project-phase-1-2.git
cd System-Security-Capstone-Project-phase-1-2
```

2. The project uses only Python standard library, so no pip installation needed!

## Usage

### Interactive CLI Menu

Run the interactive menu system:

```bash
python main.py
```

The menu allows you to:
- Encrypt/decrypt text with Caesar cipher
- Encrypt/decrypt text with Transposition cipher
- Perform brute-force attacks with AI-powered analysis
- Choose different AI recommender methods

### Example Session

```
==================================================
         SYSTEM SECURITY CAPSTONE PROJECT
              Cryptography System v1.0
==================================================

MAIN MENU
--------------------------------------------------
1. Caesar Cipher Operations
2. Transposition Cipher Operations
3. Exit
--------------------------------------------------

Enter your choice (1-3): 1

CAESAR CIPHER MENU
--------------------------------------------------
1. Encrypt text
2. Decrypt text
3. Brute-force attack (with AI recommender)
4. Back to main menu
--------------------------------------------------

Enter your choice (1-4): 3

Enter ciphertext to attack: Khoor Zruog

AI Recommender Methods:
1. Dictionary/word-match scoring (Method A)
2. N-gram (quadgram) scoring (Method B)
3. Language model scoring (Method C)
4. Hybrid (ALL methods combined) (Method D) - RECOMMENDED

Select AI method (1-4, default=4): 4

[System performs brute-force attack and displays ranked results]
```

### Programmatic Usage

You can also use the components programmatically:

```python
from src.ciphers.caesar import CaesarCipher
from src.attacks.caesar_bruteforce import CaesarBruteForce
from src.ai_recommender.recommender import AIRecommender

# Encrypt
cipher = CaesarCipher()
ciphertext = cipher.encrypt("Hello World", 3)
print(f"Encrypted: {ciphertext}")

# Brute-force attack
bruteforce = CaesarBruteForce()
candidates = bruteforce.attack(ciphertext)

# AI analysis
recommender = AIRecommender()
ranked = recommender.analyze_candidates(candidates, method='hybrid', top_n=5)
recommender.print_analysis(ranked, method='hybrid')
```

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m pytest tests/ -v

# Or using unittest
python -m unittest discover tests/

# Run specific test file
python -m unittest tests/test_caesar.py
```

### Test Coverage

- **Caesar Cipher Tests**: Encryption, decryption, case preservation, wraparound, special characters
- **Transposition Cipher Tests**: Encryption, decryption, padding, different key lengths
- **AI Recommender Tests**: All four scoring methods, candidate ranking, hybrid weighting

## Project Structure

```
.
├── main.py                          # Interactive CLI entry point
├── README.md                        # This file
├── src/
│   ├── __init__.py
│   ├── ciphers/
│   │   ├── __init__.py
│   │   ├── caesar.py                # Caesar cipher implementation
│   │   └── transposition.py        # Transposition cipher implementation
│   ├── attacks/
│   │   ├── __init__.py
│   │   ├── caesar_bruteforce.py    # Caesar brute-force attack
│   │   └── transposition_bruteforce.py  # Transposition attack
│   └── ai_recommender/
│       ├── __init__.py
│       └── recommender.py           # AI recommender (all 4 methods)
└── tests/
    ├── __init__.py
    ├── test_caesar.py               # Caesar cipher tests
    ├── test_transposition.py        # Transposition cipher tests
    └── test_ai_recommender.py       # AI recommender tests
```

## Implementation Details

### Caesar Cipher Algorithm

The Caesar cipher shifts each letter by a fixed number of positions:
- Encryption: `E(x) = (x + k) mod 26`
- Decryption: `D(x) = (x - k) mod 26`

Special handling:
- Uppercase letters: Shifted within A-Z
- Lowercase letters: Shifted within a-z
- Non-alphabetic: Preserved unchanged
- Configurable alphabet size (default: 26)

### Transposition Cipher Algorithm

Columnar transposition rearranges text based on key:
1. Write plaintext in rows under the key
2. Sort columns alphabetically by key letters
3. Read columns in sorted order

Example with key "CRYPTO":
```
Key:    C R Y P T O  →  Sorted: C O P R T Y
Text:   H E L L O W         H W L E O L
        O R L D X X         O X D R X L
```

### AI Recommender Scoring

Each method produces a normalized score (0-1 range for comparison):

1. **Dictionary**: `score = match_rate * 0.7 + avg_frequency * 0.3`
2. **N-gram**: Normalized log-likelihood of quadgrams
3. **Language Model**: Character + bigram frequency scores
4. **Hybrid**: `α * dict + β * ngram + γ * lm`

## Security Considerations

⚠️ **Educational Use Only**: These classical ciphers are NOT secure for real-world use. They are easily broken and should only be used for learning purposes.

Modern encryption standards (AES, RSA, etc.) should be used for actual security needs.

## Documentation

All methods include comprehensive documentation:
- Docstrings for all classes and functions
- Inline comments explaining complex logic
- Method identification comments (A, B, C, D) in AI recommender
- Type hints for better code clarity

## Contributing

This is a capstone project. For educational purposes, feel free to:
- Study the implementation
- Run experiments with different texts
- Analyze the AI recommender performance
- Compare different scoring methods

## License

This project is created for educational purposes as part of a System Security course.

## Authors

Elia Ghazal, George Khayat, and Elia Hourany

## Acknowledgments

- Classical cryptography algorithms
- English language frequency analysis
- Cryptanalysis techniques from historical codebreaking
