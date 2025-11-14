# AI Recommender Methods - Technical Documentation

## Overview

This document provides detailed technical documentation for all four AI recommender methods implemented in this project. Each method is designed to be explainable and reproducible, avoiding black-box models.

---

## Method A: Dictionary/Word-Match Scoring

### Description
This method tokenizes the candidate plaintext into words and compares them against a curated English word frequency list. Words that match are weighted by their frequency in English text.

### Algorithm

1. **Tokenization**: Split text using regex `[a-zA-Z]+` to extract words
2. **Normalization**: Convert all words to lowercase
3. **Matching**: For each word, check if it exists in the frequency dictionary
4. **Scoring**: 
   ```
   score = match_rate × 0.7 + (avg_frequency / 100) × 0.3
   
   where:
   - match_rate = matched_words / total_words
   - avg_frequency = sum(word_frequencies) / total_words
   ```

### Implementation Location
- File: `src/ai_recommender/recommender.py`
- Method: `score_dictionary()`
- Lines: Marked with "METHOD A" comment

### Pros and Cons

**Advantages:**
- Simple and interpretable
- Fast computation (O(n) where n = number of words)
- Works well for texts with common English words
- Easy to explain to non-technical users

**Disadvantages:**
- Fails on short texts (few words to match)
- Poor performance with proper nouns
- Doesn't consider word context
- Requires comprehensive word list

### Example Output
```python
{
    'matched_words': ['hello', 'world', 'this', 'is', 'a', 'test'],
    'total_words': 6,
    'matched_count': 6,
    'match_rate': 1.0,
    'avg_frequency': 45.5,
}
```

---

## Method B: N-gram (Quadgram) Log-Likelihood Scoring

### Description
Uses precomputed English quadgram (4-character sequences) frequencies to calculate the log-likelihood that a text is English. This is a classical cryptanalysis technique.

### Algorithm

1. **Preprocessing**: Convert text to uppercase, remove spaces
2. **Quadgram Extraction**: Sliding window of size 4
3. **Scoring**: 
   ```
   log_prob = sum(log_frequency[quadgram]) for all quadgrams
   
   - Known quadgrams: use precomputed log frequency
   - Unknown quadgrams: apply penalty of -5.0
   ```
4. **Normalization**: `avg_log_prob = log_prob / (text_length - 3)`

### Implementation Location
- File: `src/ai_recommender/recommender.py`
- Method: `score_ngram()`
- Lines: Marked with "METHOD B" comment

### Quadgram Frequency Table
The implementation includes ~75 common English quadgrams with approximate log frequencies based on English corpus analysis:
- "TION": -2.0 (very common)
- "THE ": -2.5 (common with space)
- Unknown: -5.0 (penalty)

### Pros and Cons

**Advantages:**
- Excellent for short texts
- Language-independent approach (just need frequency table)
- Proven effective in classical cryptanalysis
- Works with noisy or incomplete text

**Disadvantages:**
- Requires precomputed frequency table
- Less intuitive than word matching
- Can be fooled by non-words with common letter patterns

### Example Output
```python
{
    'quadgram_count': 15,
    'log_likelihood': -48.5,
    'avg_log_prob': -3.23,
    'sample_quadgrams': [('TION', -2.0), ('THE ', -2.5), ...]
}
```

---

## Method C: Language Model Scoring

### Description
A lightweight language model using character and bigram frequency statistics to estimate how "English-like" a text appears. This is a simplified alternative to full neural language models while maintaining reproducibility.

### Algorithm

1. **Character Frequency Analysis**:
   ```
   char_score = sum(expected_frequency[char]) for all chars
   avg_char_score = char_score / char_count
   
   Expected frequencies based on English corpus:
   - 'e': 12.70%, 't': 9.06%, 'a': 8.17%, etc.
   - ' ': 15.0% (spaces)
   ```

2. **Bigram Frequency Analysis**:
   ```
   bigram_score = sum(expected_frequency[bigram]) for all bigrams
   avg_bigram_score = bigram_score / (text_length - 1)
   
   Common bigrams: 'th', 'he', 'in', 'er', 'an', etc.
   ```

3. **Final Score**:
   ```
   score = (avg_char_score / 10) × 0.5 + avg_bigram_score × 0.5
   ```

### Implementation Location
- File: `src/ai_recommender/recommender.py`
- Method: `score_language_model()`
- Lines: Marked with "METHOD C" comment

### Frequency Tables
- **Character frequencies**: 26 letters + space (~27 entries)
- **Bigram frequencies**: 25 most common English bigrams

### Pros and Cons

**Advantages:**
- No external dependencies
- Fully reproducible
- Good balance of performance and simplicity
- Works reasonably well on various text lengths

**Disadvantages:**
- Less sophisticated than full language models
- May not capture complex linguistic patterns
- Static frequency tables (no learning)

### Example Output
```python
{
    'char_score': 8.75,
    'bigram_score': 0.92,
    'char_count': 42,
    'bigram_count': 38
}
```

---

## Method D: Hybrid Heuristic (RECOMMENDED)

### Description
Combines all three methods (A, B, C) with configurable weights to leverage the strengths of each approach. This provides the most robust analysis across different text types and lengths.

### Algorithm

1. **Compute Individual Scores**:
   - Dictionary score (0-1 range)
   - N-gram score (normalized to 0-1)
   - Language model score (normalized to 0-1)

2. **Normalization**:
   ```
   ngram_normalized = max(0, min(1, (ngram_score + 10) / 8))
   lm_normalized = max(0, min(1, lm_score / 2))
   ```

3. **Weighted Combination**:
   ```
   final_score = α × dict_score + β × ngram_normalized + γ × lm_normalized
   
   Default weights:
   - α = 0.35 (dictionary)
   - β = 0.35 (n-gram)
   - γ = 0.30 (language model)
   ```

### Implementation Location
- File: `src/ai_recommender/recommender.py`
- Method: `score_hybrid()`
- Lines: Marked with "METHOD D" comment

### Weight Justification

The default weights (α=0.35, β=0.35, γ=0.30) were chosen based on:

1. **Equal emphasis on dictionary and n-gram** (0.35 each):
   - Dictionary excellent for common words
   - N-gram excellent for short/noisy text
   - Complementary strengths

2. **Slightly lower weight on language model** (0.30):
   - Simpler than full LMs
   - Still provides valuable signal
   - Prevents over-reliance on any single method

3. **Weights are configurable** via function parameters for experimentation

### Pros and Cons

**Advantages:**
- Most robust across different scenarios
- Leverages strengths of all methods
- Provides component-level explanations
- Configurable weights for tuning

**Disadvantages:**
- Slightly more complex to explain
- Computational overhead of running all methods
- Requires tuning weights for optimal performance

### Example Output
```python
{
    'final_score': 0.6234,
    'weights': {'alpha': 0.35, 'beta': 0.35, 'gamma': 0.30},
    'components': {
        'dictionary': {
            'score': 0.75,
            'details': {...}
        },
        'ngram': {
            'score': -3.2,
            'normalized': 0.85,
            'details': {...}
        },
        'language_model': {
            'score': 1.2,
            'normalized': 0.60,
            'details': {...}
        }
    }
}
```

---

## Usage Examples

### Using a Single Method
```python
from src.ai_recommender.recommender import AIRecommender

recommender = AIRecommender()
text = "hello world"

# Method A
score_a, explanation_a = recommender.score_dictionary(text)

# Method B
score_b, explanation_b = recommender.score_ngram(text)

# Method C
score_c, explanation_c = recommender.score_language_model(text)

# Method D
score_d, explanation_d = recommender.score_hybrid(text)
```

### Analyzing Candidates
```python
candidates = [(0, "abc"), (3, "hello world"), (5, "xyz")]

# Use hybrid method (recommended)
ranked = recommender.analyze_candidates(
    candidates, 
    method='hybrid',  # or 'dictionary', 'ngram', 'language_model'
    top_n=3
)

# Print detailed analysis
recommender.print_analysis(ranked, method='hybrid')
```

### Custom Hybrid Weights
```python
# Emphasize dictionary method
score, explanation = recommender.score_hybrid(
    text,
    alpha=0.7,  # 70% dictionary
    beta=0.2,   # 20% n-gram
    gamma=0.1   # 10% language model
)
```

---

## Performance Comparison

Based on testing with various ciphertexts:

| Method | Short Text (<10 words) | Medium Text (10-50 words) | Long Text (>50 words) |
|--------|----------------------|--------------------------|---------------------|
| Dictionary | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| N-gram | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Language Model | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Hybrid | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## Reproducibility

All methods are fully reproducible:

1. **No random elements**: Deterministic scoring
2. **No external API calls**: All computation local
3. **Fixed frequency tables**: Embedded in code
4. **Version controlled**: All parameters documented
5. **No model downloads**: Pure Python implementation

To reproduce results:
```python
# Same input always produces same output
text = "test message"
score1, _ = recommender.score_hybrid(text)
score2, _ = recommender.score_hybrid(text)
assert score1 == score2  # Always True
```

---

## Future Enhancements

Potential improvements while maintaining explainability:

1. **Expand frequency tables**: Include more quadgrams, trigrams
2. **Add language detection**: Auto-detect non-English text
3. **Context-aware scoring**: Consider sentence structure
4. **Adaptive weights**: Learn optimal weights from examples
5. **Domain-specific dictionaries**: Technical, medical, etc.

All enhancements must maintain:
- Explainability
- Reproducibility  
- No black-box models

---

## References

- **N-gram analysis**: Classical cryptanalysis techniques
- **Character/bigram frequencies**: English language corpus statistics
- **Hybrid methods**: Ensemble learning principles
- **Cryptanalysis**: Historical codebreaking methods (Enigma, etc.)

---

## Testing

See `tests/test_ai_recommender.py` for comprehensive unit tests covering:
- Each method individually
- Edge cases (empty text, gibberish, etc.)
- Candidate ranking
- Custom weights
- All method variations
