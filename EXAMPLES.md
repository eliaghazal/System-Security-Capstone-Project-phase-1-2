# Example Usage Scenarios

This document provides example usage scenarios for the cryptography system.

## Scenario 1: Encrypting a Secret Message (Caesar Cipher)

```python
from src.ciphers.caesar import CaesarCipher

# Create cipher instance
cipher = CaesarCipher()

# Your secret message
message = "Attack at dawn"
key = 7

# Encrypt
ciphertext = cipher.encrypt(message, key)
print(f"Send this to your ally: {ciphertext}")
# Output: Haahjr ha khdv

# They decrypt using the same key
plaintext = cipher.decrypt(ciphertext, key)
print(f"Ally receives: {plaintext}")
# Output: Attack at dawn
```

## Scenario 2: Breaking an Enemy's Caesar Cipher

```python
from src.attacks.caesar_bruteforce import CaesarBruteForce
from src.ai_recommender.recommender import AIRecommender

# You intercepted this message
enemy_message = "Khoor Zruog"

# Try to break it
bruteforce = CaesarBruteForce()
candidates = bruteforce.attack(enemy_message)

# Use AI to find the most likely plaintext
recommender = AIRecommender()
ranked = recommender.analyze_candidates(candidates, method='hybrid', top_n=1)

# Get the best result
key, plaintext, score, explanation = ranked[0]
print(f"Enemy's message: {plaintext}")
print(f"They used key: {key}")
```

## Scenario 3: Using Transposition for Better Security

```python
from src.ciphers.transposition import TranspositionCipher

cipher = TranspositionCipher()

# Your message
message = "MEETATTHEBRIDGE"
key = "SECRET"

# Encrypt
ciphertext = cipher.encrypt(message, key)
print(f"Encrypted: {ciphertext}")

# Decrypt
plaintext = cipher.decrypt(ciphertext, key)
print(f"Decrypted: {plaintext}")
```

## Scenario 4: Comparing AI Methods for Analysis

```python
from src.attacks.caesar_bruteforce import CaesarBruteForce
from src.ai_recommender.recommender import AIRecommender

ciphertext = "Wkh txlfn eurzq ira"
bruteforce = CaesarBruteForce()
candidates = bruteforce.attack(ciphertext)

recommender = AIRecommender()

# Try each method
methods = ['dictionary', 'ngram', 'language_model', 'hybrid']
for method in methods:
    ranked = recommender.analyze_candidates(candidates, method=method, top_n=1)
    key, text, score, _ = ranked[0]
    print(f"{method:15s}: Key={key:2d}, Score={score:.3f}, Text={text}")

# Output will show which method works best for this particular text
```

## Scenario 5: Interactive Menu System

For the easiest experience, use the interactive menu:

```bash
python main.py
```

Then follow the on-screen prompts:
1. Choose Caesar or Transposition cipher
2. Select encrypt, decrypt, or attack operation
3. Enter your text and keys as prompted
4. For attacks, choose which AI method to use

## Scenario 6: Educational Analysis

Compare different encryption strengths:

```python
from src.ciphers.caesar import CaesarCipher
from src.attacks.caesar_bruteforce import CaesarBruteForce
from src.ai_recommender.recommender import AIRecommender

cipher = CaesarCipher()
recommender = AIRecommender()

# Test with different text lengths
texts = [
    "Hi",
    "Hello there",
    "The quick brown fox jumps over the lazy dog",
]

for text in texts:
    # Encrypt with random key
    ciphertext = cipher.encrypt(text, 13)
    
    # Attack
    bf = CaesarBruteForce()
    candidates = bf.attack(ciphertext)
    
    # Analyze
    ranked = recommender.analyze_candidates(candidates, method='hybrid', top_n=1)
    key, plaintext, score, _ = ranked[0]
    
    print(f"Text length: {len(text):2d}, AI confidence: {score:.3f}, Correct? {plaintext == text}")

# Shows that AI works better with longer texts
```

## Scenario 7: Custom Alphabet Size

```python
from src.ciphers.caesar import CaesarCipher

# Use 26-letter alphabet (default)
cipher26 = CaesarCipher(alphabet_size=26)
encrypted = cipher26.encrypt("HELLO", 5)
print(f"26-letter alphabet: {encrypted}")

# Could extend for different alphabets
# (though implementation currently uses English A-Z)
```

## Scenario 8: Secure Key Distribution

Remember: In real scenarios, you need to securely share the key with your recipient!

```python
from src.ciphers.transposition import TranspositionCipher

# Both parties agree on a key beforehand (in person or via secure channel)
shared_key = "TRUSTNOONE"

# Sender
cipher = TranspositionCipher()
message = "SECRETMISSION"
encrypted = cipher.encrypt(message, shared_key)
# Send encrypted message over insecure channel

# Receiver
decrypted = cipher.decrypt(encrypted, shared_key)
print(f"Received: {decrypted}")
```

## Tips for Best Results

1. **For Encryption:**
   - Use longer, more random keys for transposition
   - Remember: these are classical ciphers, NOT secure for real secrets!
   - Always use modern encryption (AES, RSA) for actual security

2. **For Cryptanalysis:**
   - Longer ciphertexts give better AI recommendations
   - Hybrid method is most reliable overall
   - Dictionary method works best for common English words
   - N-gram method works well for short or unusual texts

3. **For Learning:**
   - Run the demo.py to see all features
   - Try breaking your own encrypted messages
   - Compare different AI methods on the same ciphertext
   - Read the code comments to understand each algorithm

## Quick Reference

### Caesar Cipher
- **Encrypt:** `cipher.encrypt(text, key)`
- **Decrypt:** `cipher.decrypt(text, key)`
- **Attack:** `bruteforce.attack(ciphertext)`

### Transposition Cipher
- **Encrypt:** `cipher.encrypt(text, key_string)`
- **Decrypt:** `cipher.decrypt(text, key_string)`
- **Attack:** `bruteforce.attack(ciphertext, max_key_length)`

### AI Recommender
- **Methods:** 'dictionary', 'ngram', 'language_model', 'hybrid'
- **Analyze:** `recommender.analyze_candidates(candidates, method='hybrid', top_n=5)`
- **Print:** `recommender.print_analysis(ranked, method='hybrid')`
