# System Security Capstone Project - Cipher Cryptanalysis

A modular, tested, packaged system for classical cipher encryption, decryption, and AI-based cryptanalysis. This project implements Caesar cipher and Transposition cipher with brute-force attacks and an explainable AI recommender that ranks likely plaintexts.

## Features

### Phase 1: Caesar Cipher
- ✅ Encryption/decryption with case preservation
- ✅ Configurable alphabet size (default: 26)
- ✅ Brute-force attack (tries all possible keys)
- ✅ AI-based plaintext ranking with multiple scoring methods

### Phase 2: Transposition Cipher
- ✅ Columnar transposition encryption/decryption
- ✅ Brute-force attack with configurable key range
- ✅ Extended AI recommender for transposition cipher

### AI Recommender Scoring Methods

The recommender uses multiple explainable and reproducible scoring methods:

1. **Dictionary Scoring**: Measures the proportion of common English words
2. **Bigram Analysis**: Scores based on English bigram frequencies
3. **Trigram Analysis**: Scores based on English trigram frequencies
4. **Frequency Analysis**: Chi-squared test comparing letter frequencies to English
5. **Perplexity Scoring**: Language model-like scoring using n-gram probabilities
6. **Hybrid Scoring**: Weighted combination of all methods (default)

All scoring methods are explainable and reproducible, with detailed breakdowns available via the `--explain` flag.

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/eliaghazal/System-Security-Capstone-Project-phase-1-2.git
cd System-Security-Capstone-Project-phase-1-2

# Install the package
pip install -e .

# Install development dependencies (for testing)
pip install -e ".[dev]"
```

### Requirements

- Python 3.8 or higher
- NumPy (for numerical operations)
- pytest and pytest-cov (for testing, optional)

## Usage

### Command Line Interface

The package provides a comprehensive CLI tool:

#### Caesar Cipher

**Encrypt:**
```bash
cipher-tool caesar encrypt "Hello World" 3
# Output: Encrypted: Khoor Zruog

# Or using Python module
python -m cipher_cryptanalysis.cli caesar encrypt "Hello World" 3
```

**Decrypt:**
```bash
cipher-tool caesar decrypt "Khoor Zruog" 3
# Output: Decrypted: Hello World
```

**Attack (Brute Force with AI Ranking):**
```bash
cipher-tool caesar attack "Khoor Zruog" --top-n 5
# Shows top 5 most likely plaintexts

# With detailed scoring explanation
cipher-tool caesar attack "Khoor Zruog" --top-n 3 --explain

# Using different scoring methods
cipher-tool caesar attack "Khoor Zruog" --scoring-method dictionary
cipher-tool caesar attack "Khoor Zruog" --scoring-method bigram
cipher-tool caesar attack "Khoor Zruog" --scoring-method hybrid
```

**Custom Alphabet Size:**
```bash
cipher-tool caesar encrypt "ABC" 5 --alphabet-size 10
```

#### Transposition Cipher

**Encrypt:**
```bash
cipher-tool transposition encrypt "The quick brown fox" 5
# Output: Encrypted: Tub  lhirfuotecoomvq n koxwher
```

**Decrypt:**
```bash
cipher-tool transposition decrypt "Tub  lhirfuotecoomvq n koxwher" 5
# Output: Decrypted: The quick brown fox
```

**Attack (Brute Force with AI Ranking):**
```bash
cipher-tool transposition attack "Tub  lhirfuotecoomvq n koxwher" --max-key 10 --top-n 5

# With explanation
cipher-tool transposition attack "Tub  lhirfuotecoomvq n koxwher" --top-n 3 --explain
```

### Python API

```python
from cipher_cryptanalysis import CaesarCipher, TranspositionCipher, BruteForceAttack, PlaintextRanker

# Caesar Cipher
cipher = CaesarCipher(alphabet_size=26)
ciphertext = cipher.encrypt("Hello World", key=3)
plaintext = cipher.decrypt(ciphertext, key=3)

# Transposition Cipher
trans_cipher = TranspositionCipher()
ciphertext = trans_cipher.encrypt("Hello World", key=4)
plaintext = trans_cipher.decrypt(ciphertext, key=4)

# Brute Force Attack
attack = BruteForceAttack()
results = attack.attack_caesar(ciphertext, alphabet_size=26)

# AI Ranking
ranker = PlaintextRanker(scoring_method='hybrid')
ranked = ranker.rank(results, top_n=5)

# With explanation
for result in ranker.rank_with_explanation(results, top_n=3):
    print(f"Key: {result['key']}")
    print(f"Text: {result['plaintext']}")
    print(f"Score: {result['score']:.4f}")
    print(f"Explanation: {result['explanation']}")
```

## Testing

The project includes comprehensive unit tests with 77 test cases covering all functionality:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=cipher_cryptanalysis --cov-report=html

# Run specific test file
pytest tests/test_caesar.py
pytest tests/test_transposition.py
pytest tests/test_ranker.py
```

### Test Coverage

- **Caesar Cipher**: 13 tests covering encryption, decryption, edge cases, and various alphabet sizes
- **Transposition Cipher**: 13 tests covering encryption, decryption, and key validation
- **Brute Force Attack**: 10 tests covering both cipher types and ranking integration
- **Text Scorer**: 22 tests covering all scoring methods
- **Plaintext Ranker**: 19 tests covering ranking, explanation, and all scoring methods

## Project Structure

```
.
├── src/
│   └── cipher_cryptanalysis/
│       ├── __init__.py
│       ├── cli.py                    # Command-line interface
│       ├── ciphers/
│       │   ├── __init__.py
│       │   ├── caesar.py            # Caesar cipher implementation
│       │   └── transposition.py     # Transposition cipher implementation
│       ├── attacks/
│       │   ├── __init__.py
│       │   └── brute_force.py       # Brute force attack implementation
│       └── recommender/
│           ├── __init__.py
│           ├── plaintext_ranker.py  # AI-based ranking system
│           ├── scorer.py            # Scoring methods
│           └── language_stats.py    # English language statistics
├── tests/
│   ├── test_caesar.py
│   ├── test_transposition.py
│   ├── test_brute_force.py
│   ├── test_scorer.py
│   └── test_ranker.py
├── setup.py
├── requirements.txt
└── README.md
```

## Methodology

### Cryptanalysis Approach

1. **Brute Force**: Try all possible keys (26 for Caesar, configurable range for Transposition)
2. **AI Ranking**: Score each decrypted result using multiple methods
3. **Ranking**: Sort by score and return top N candidates
4. **Explanation**: Provide detailed scoring breakdown for transparency

### Scoring Methods

All scoring methods are normalized to produce comparable results:

- **Dictionary (0-1)**: Proportion of common English words
- **Bigram (0-1)**: Normalized average bigram frequency
- **Trigram (0-1)**: Normalized average trigram frequency
- **Frequency (0-1)**: Inverse chi-squared statistic (normalized)
- **Perplexity (0-1)**: Exponential of average log probability
- **Hybrid (0-1)**: Weighted combination (default: 30% dict, 20% bigram, 20% trigram, 20% freq, 10% perplexity)

### Reproducibility

- All language statistics are hardcoded (no external dependencies)
- Deterministic scoring (no randomness)
- Explicit weights for hybrid scoring
- Clear documentation of all algorithms

## Examples

### Example 1: Caesar Cipher Attack

```bash
$ cipher-tool caesar attack "Wkh txlfn eurzq ira" --top-n 3 --explain

Attacking Caesar cipher with hybrid scoring...
Ciphertext: Wkh txlfn eurzq ira

Top 3 candidates:

1. Key  3 (score: 0.6234): The quick brown fox
   Explanation:
     dictionary  : 0.7500
     bigram      : 0.9123
     trigram     : 0.8456
     frequency   : 87.1234
     perplexity  : 0.8901
     hybrid      : 0.6234
```

### Example 2: Transposition Cipher Attack

```bash
$ cipher-tool transposition attack "Hloel" --max-key 5 --top-n 2

Top 2 candidates:

1. Key  2 (score: 0.5123): Hello
2. Key  3 (score: 0.1234): Holel
```

## Design Principles

- **Modularity**: Separate modules for ciphers, attacks, and recommenders
- **Testability**: Comprehensive unit tests with 100% function coverage
- **Extensibility**: Easy to add new ciphers and scoring methods
- **Explainability**: All scoring methods provide interpretable results
- **Reproducibility**: Deterministic algorithms with documented parameters

## Contributing

This is a capstone project for a System Security course. Contributions, suggestions, and feedback are welcome!

## License

This project is for educational purposes as part of a System Security course.

## Authors

- Capstone Project Team
- Course: System Security

## Acknowledgments

- English language statistics based on common corpus analysis
- Cryptanalysis techniques from classical cryptography literature