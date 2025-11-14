# Usage Guide - Cipher Cryptanalysis System

This guide provides detailed instructions on how to use the cipher cryptanalysis system.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Caesar Cipher](#caesar-cipher)
4. [Transposition Cipher](#transposition-cipher)
5. [AI Recommender](#ai-recommender)
6. [Python API](#python-api)
7. [Advanced Examples](#advanced-examples)

## Installation

### From Source

```bash
git clone https://github.com/eliaghazal/System-Security-Capstone-Project-phase-1-2.git
cd System-Security-Capstone-Project-phase-1-2
pip install -e .
```

### Verify Installation

```bash
cipher-tool --help
python -m pytest tests/  # Run tests
```

## Quick Start

### Encrypt a Message

```bash
# Caesar cipher
cipher-tool caesar encrypt "Hello World" 3

# Transposition cipher
cipher-tool transposition encrypt "Hello World" 4
```

### Attack a Ciphertext

```bash
# Caesar cipher attack
cipher-tool caesar attack "Khoor Zruog"

# Transposition cipher attack
cipher-tool transposition attack "Hlel Wlrodo"
```

## Caesar Cipher

### Encryption

**Basic usage:**
```bash
cipher-tool caesar encrypt "Attack at dawn" 13
# Output: Nggnpx ng qnja
```

**With custom alphabet size:**
```bash
cipher-tool caesar encrypt "ABC" 5 --alphabet-size 10
```

**Case preservation:**
```bash
cipher-tool caesar encrypt "Hello World!" 7
# Output: Olssv Dvysk! (case and punctuation preserved)
```

### Decryption

```bash
cipher-tool caesar decrypt "Nggnpx ng qnja" 13
# Output: Attack at dawn
```

### Brute Force Attack

**Basic attack (top 5 candidates):**
```bash
cipher-tool caesar attack "Nggnpx ng qnja"
```

**Show more candidates:**
```bash
cipher-tool caesar attack "Nggnpx ng qnja" --top-n 10
```

**With detailed explanation:**
```bash
cipher-tool caesar attack "Nggnpx ng qnja" --explain
```

**Example output with explanation:**
```
Attacking Caesar cipher with hybrid scoring...
Ciphertext: Nggnpx ng qnja

Top 3 candidates:

1. Key 13 (score: 0.2437): Attack at dawn
   Explanation:
     dictionary  : 0.6667
     bigram      : 0.9234
     trigram     : 0.8123
     frequency   : 78.4321
     perplexity  : 0.8456
     hybrid      : 0.2437

2. Key  2 (score: 0.1226): Leelnv le olhy
   ...
```

**Using different scoring methods:**
```bash
# Dictionary-based scoring
cipher-tool caesar attack "Nggnpx ng qnja" --scoring-method dictionary

# Bigram frequency analysis
cipher-tool caesar attack "Nggnpx ng qnja" --scoring-method bigram

# Hybrid (default - combines all methods)
cipher-tool caesar attack "Nggnpx ng qnja" --scoring-method hybrid
```

### Available Scoring Methods

1. **dictionary** - Measures proportion of common English words
2. **bigram** - Analyzes bigram (2-letter) frequencies
3. **trigram** - Analyzes trigram (3-letter) frequencies
4. **frequency** - Chi-squared test on letter frequencies
5. **perplexity** - Language model-like scoring
6. **hybrid** - Weighted combination of all methods (recommended)

## Transposition Cipher

### Encryption

**Basic usage:**
```bash
cipher-tool transposition encrypt "The quick brown fox" 5
# Output: Tub  lhirfuotecoomvq n koxwher
```

**With longer messages:**
```bash
cipher-tool transposition encrypt "Meet me at the park at midnight" 6
```

### Decryption

```bash
cipher-tool transposition decrypt "Tub  lhirfuotecoomvq n koxwher" 5
# Output: The quick brown fox
```

### Brute Force Attack

**Basic attack:**
```bash
cipher-tool transposition attack "Tub  lhirfuotecoomvq n koxwher"
```

**Increase maximum key to try:**
```bash
cipher-tool transposition attack "ciphertext" --max-key 20
```

**With explanation:**
```bash
cipher-tool transposition attack "ciphertext" --explain --top-n 3
```

## AI Recommender

The AI recommender uses multiple scoring methods to rank potential plaintexts. All methods are:
- **Explainable**: Each score can be broken down and understood
- **Reproducible**: Same input always produces same output
- **Configurable**: Weights can be adjusted for hybrid scoring

### Understanding Scores

Scores range from 0 to 1, with higher scores indicating more likely plaintexts:

- **Dictionary Score (0-1)**: Proportion of recognized English words
  - 1.0 = All words are common English words
  - 0.0 = No recognized words

- **Bigram/Trigram Score (normalized to 0-1)**: Average frequency of n-grams
  - Higher = More common letter combinations
  - Based on English text corpus statistics

- **Frequency Score (normalized to 0-1)**: How well letter distribution matches English
  - Higher = Better match to expected English letter frequencies
  - Uses chi-squared statistical test

- **Perplexity Score (0-1)**: Language model probability
  - Higher = More likely to be valid English
  - Lower perplexity indicates better text

- **Hybrid Score (0-1)**: Weighted combination
  - Default weights: 30% dictionary, 20% bigram, 20% trigram, 20% frequency, 10% perplexity
  - Provides balanced evaluation

## Python API

### Basic Usage

```python
from cipher_cryptanalysis import CaesarCipher, TranspositionCipher

# Caesar cipher
cipher = CaesarCipher()
ciphertext = cipher.encrypt("Hello", 3)
plaintext = cipher.decrypt(ciphertext, 3)

# Transposition cipher
trans = TranspositionCipher()
ciphertext = trans.encrypt("Hello", 4)
plaintext = trans.decrypt(ciphertext, 4)
```

### Attack with Ranking

```python
from cipher_cryptanalysis import BruteForceAttack, PlaintextRanker

# Setup
attack = BruteForceAttack()
ranker = PlaintextRanker(scoring_method='hybrid')

# Attack Caesar cipher
results = attack.attack_with_ranker(
    ciphertext="Khoor",
    cipher_type='caesar',
    ranker=ranker.score,
    top_n=5,
    alphabet_size=26
)

# Results: [(key, plaintext, score), ...]
for key, plaintext, score in results:
    print(f"Key {key}: {plaintext} (score: {score:.4f})")
```

### Explainable Ranking

```python
from cipher_cryptanalysis import PlaintextRanker

ranker = PlaintextRanker(scoring_method='hybrid')

# Get detailed explanation
explanation = ranker.explain_score("Hello World")
print(explanation)
# Output: {'dictionary': 0.0, 'bigram': 0.48, ...}

# Rank with explanation
candidates = [(1, "text1"), (2, "text2"), ...]
results = ranker.rank_with_explanation(candidates, top_n=3)

for result in results:
    print(f"Key: {result['key']}")
    print(f"Text: {result['plaintext']}")
    print(f"Score: {result['score']:.4f}")
    print(f"Breakdown: {result['explanation']}")
```

### Custom Scoring Weights

```python
from cipher_cryptanalysis.recommender import TextScorer

scorer = TextScorer()

# Custom hybrid weights
weights = {
    'dictionary': 0.5,  # 50% weight
    'bigram': 0.3,      # 30% weight
    'trigram': 0.2,     # 20% weight
    'frequency': 0.0,   # 0% weight
    'perplexity': 0.0,  # 0% weight
}

score = scorer.hybrid_score("Hello World", weights=weights)
```

## Advanced Examples

### Example 1: Batch Processing

```python
from cipher_cryptanalysis import CaesarCipher, BruteForceAttack, PlaintextRanker

# Multiple ciphertexts
ciphertexts = [
    "Khoor Zruog",
    "Nggnpx ng qnja",
    "Wkh txlfn eurzq ira"
]

attack = BruteForceAttack()
ranker = PlaintextRanker(scoring_method='hybrid')

for i, ct in enumerate(ciphertexts, 1):
    results = attack.attack_with_ranker(ct, 'caesar', ranker.score, top_n=1)
    key, plaintext, score = results[0]
    print(f"{i}. Best guess: '{plaintext}' (key {key}, score {score:.4f})")
```

### Example 2: Custom Scoring Function

```python
from cipher_cryptanalysis import BruteForceAttack

def custom_scorer(text):
    """Custom scoring: prefer texts with 'secret' word."""
    score = 0.0
    if 'secret' in text.lower():
        score += 1.0
    # Add length penalty for very short/long texts
    if 10 <= len(text) <= 100:
        score += 0.5
    return score

attack = BruteForceAttack()
results = attack.attack_with_ranker(
    "ciphertext",
    'caesar',
    custom_scorer,
    top_n=5
)
```

### Example 3: Testing Different Alphabet Sizes

```python
from cipher_cryptanalysis import CaesarCipher

# Standard 26-letter alphabet
cipher26 = CaesarCipher(alphabet_size=26)
ct1 = cipher26.encrypt("Test", 5)

# Custom alphabet size
cipher10 = CaesarCipher(alphabet_size=10)
ct2 = cipher10.encrypt("Test", 5)

print(f"26-letter: {ct1}")
print(f"10-letter: {ct2}")
```

### Example 4: Comparing Scoring Methods

```python
from cipher_cryptanalysis import PlaintextRanker

text = "The quick brown fox jumps over the lazy dog"
methods = ['dictionary', 'bigram', 'trigram', 'frequency', 'perplexity', 'hybrid']

print("Scoring method comparison:")
for method in methods:
    ranker = PlaintextRanker(scoring_method=method)
    score = ranker.score(text)
    print(f"{method:12s}: {score:.4f}")
```

## Tips and Best Practices

1. **Use hybrid scoring for general cases**: It combines multiple methods for robust results

2. **Use dictionary scoring for short messages**: Dictionary-based works well for short, word-based texts

3. **Use frequency/bigram for longer texts**: Statistical methods work better with more data

4. **Adjust max_key for transposition**: Longer texts may need larger max_key values

5. **Check multiple top candidates**: The best score isn't always correct; review top 3-5 results

6. **Use --explain for learning**: The detailed breakdown helps understand how scoring works

7. **Validate results**: Always verify that decrypted text makes sense in context

## Troubleshooting

### Issue: Attack doesn't find correct key

**Solution**: Try different scoring methods or increase top_n to see more candidates

```bash
cipher-tool caesar attack "text" --scoring-method dictionary --top-n 10
```

### Issue: Scores are all very low

**Cause**: Ciphertext might not be English or uses different encoding

**Solution**: Verify the ciphertext and ensure it's from a supported cipher

### Issue: Transposition attack is slow

**Cause**: Large max_key value creates many candidates

**Solution**: Reduce max_key or use faster scoring method

```bash
cipher-tool transposition attack "text" --max-key 10 --scoring-method bigram
```

## Further Reading

- See `examples.py` for interactive demonstrations
- Check `tests/` directory for usage examples
- Review source code documentation for API details
- Consult README.md for project overview

## Getting Help

For issues or questions:
1. Check the examples in this guide
2. Run the test suite: `pytest tests/`
3. Review the example demonstrations: `python examples.py`
4. Check the source code documentation
