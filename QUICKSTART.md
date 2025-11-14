# Quick Start Guide

Get started with the System Security Capstone Project in 5 minutes!

## Installation

1. Clone the repository:
```bash
git clone https://github.com/eliaghazal/System-Security-Capstone-Project-phase-1-2.git
cd System-Security-Capstone-Project-phase-1-2
```

2. That's it! No dependencies to install (uses only Python standard library).

## Running the System

### Option 1: Interactive Menu (Recommended for Beginners)

```bash
python main.py
```

Follow the on-screen prompts to:
- Encrypt/decrypt messages
- Perform cryptanalysis attacks
- Test AI recommender methods

### Option 2: Demo Script (See All Features)

```bash
python demo.py
```

This runs 6 comprehensive demonstrations showing all system capabilities.

### Option 3: Programmatic Use (For Developers)

```python
from src.ciphers.caesar import CaesarCipher
from src.attacks.caesar_bruteforce import CaesarBruteForce
from src.ai_recommender.recommender import AIRecommender

# Encrypt a message
cipher = CaesarCipher()
ciphertext = cipher.encrypt("Hello World", 3)
print(f"Encrypted: {ciphertext}")  # Khoor Zruog

# Break the cipher
bruteforce = CaesarBruteForce()
candidates = bruteforce.attack(ciphertext)

# Use AI to find the answer
recommender = AIRecommender()
ranked = recommender.analyze_candidates(candidates, method='hybrid', top_n=1)
key, plaintext, score, _ = ranked[0]
print(f"Decrypted: {plaintext}, Key: {key}")  # Hello World, Key: 3
```

## Quick Examples

### Encrypt with Caesar Cipher
```python
from src.ciphers.caesar import CaesarCipher

cipher = CaesarCipher()
encrypted = cipher.encrypt("Attack at dawn", 5)
print(encrypted)  # Fyyfhp fy ifbs
```

### Break a Caesar Cipher
```python
from src.attacks.caesar_bruteforce import CaesarBruteForce
from src.ai_recommender.recommender import AIRecommender

ciphertext = "Khoor Zruog"

# Attack
bruteforce = CaesarBruteForce()
candidates = bruteforce.attack(ciphertext)

# Analyze with AI
recommender = AIRecommender()
ranked = recommender.analyze_candidates(candidates, method='hybrid', top_n=1)

# Get result
key, plaintext, score, _ = ranked[0]
print(f"{plaintext} (key={key})")  # Hello World (key=3)
```

### Encrypt with Transposition Cipher
```python
from src.ciphers.transposition import TranspositionCipher

cipher = TranspositionCipher()
encrypted = cipher.encrypt("MEETATMIDNIGHT", "SECRET")
print(encrypted)
```

## Running Tests

```bash
# Run all tests
python -m unittest discover tests/ -v

# Run specific test file
python -m unittest tests/test_caesar.py
```

All 30 tests should pass!

## Next Steps

1. **Read the documentation:**
   - `README.md` - Complete project overview
   - `EXAMPLES.md` - Usage scenarios
   - `AI_METHODS.md` - Technical details of AI methods

2. **Try the demos:**
   - Run `python demo.py` to see all features
   - Experiment with different texts and keys

3. **Explore the code:**
   - `src/ciphers/` - Cipher implementations
   - `src/attacks/` - Brute-force attacks
   - `src/ai_recommender/` - AI scoring methods

4. **Learn about the AI methods:**
   - Method A: Dictionary matching
   - Method B: N-gram analysis
   - Method C: Language model
   - Method D: Hybrid (recommended)

## Common Tasks

### Encrypt a Secret Message
```bash
python main.py
# Select: 1 (Caesar Cipher)
# Select: 1 (Encrypt)
# Enter your message and key
```

### Break an Encrypted Message
```bash
python main.py
# Select: 1 (Caesar Cipher)
# Select: 3 (Brute-force attack)
# Enter the ciphertext
# Choose AI method (4 for Hybrid recommended)
```

### Compare AI Methods
See `EXAMPLES.md` Scenario 4 for comparing all AI methods on the same ciphertext.

## Troubleshooting

**Q: Python not found?**
A: Install Python 3.7+ from python.org

**Q: Import errors?**
A: Make sure you're in the project root directory when running commands

**Q: Tests failing?**
A: This shouldn't happen! All tests pass in the verified release. Check your Python version.

## Support

- **Documentation**: See README.md, EXAMPLES.md, AI_METHODS.md
- **Code Examples**: Run demo.py
- **Tests**: Check tests/ directory for examples

## Project Structure at a Glance

```
.
├── main.py              # Interactive CLI
├── demo.py              # Demonstration script
├── README.md            # Full documentation
├── EXAMPLES.md          # Usage scenarios
├── AI_METHODS.md        # AI technical docs
├── QUICKSTART.md        # This file
├── src/
│   ├── ciphers/         # Cipher implementations
│   ├── attacks/         # Brute-force attacks
│   └── ai_recommender/  # AI scoring methods
└── tests/               # Unit tests (30 tests)
```

## What Makes This Special?

✅ **Complete implementation** of Phase 1 & 2 requirements
✅ **Four AI methods** (all documented and explainable)
✅ **Interactive menu** (no command-line arguments needed)
✅ **Comprehensive testing** (30 unit tests, all passing)
✅ **No dependencies** (pure Python standard library)
✅ **Well documented** (4 documentation files + code comments)
✅ **Educational** (perfect for learning cryptography)

## Ready to Start?

Run this now:
```bash
python demo.py
```

Then explore with:
```bash
python main.py
```

Happy encrypting! 🔐
