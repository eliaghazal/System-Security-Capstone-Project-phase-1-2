# Architecture Documentation

## System Overview

The Cipher Cryptanalysis System is designed with a modular architecture that separates concerns and promotes code reusability, testability, and extensibility.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     CLI Interface                            │
│                  (cipher_cryptanalysis.cli)                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
┌───────▼──────────┐         ┌────────▼─────────┐
│  Cipher Modules  │         │  Attack Module   │
│                  │         │                  │
│  - Caesar        │◄────────┤  - BruteForce    │
│  - Transposition │         │                  │
└──────────────────┘         └────────┬─────────┘
                                      │
                             ┌────────▼──────────┐
                             │  AI Recommender   │
                             │                   │
                             │  - PlaintextRanker│
                             │  - TextScorer     │
                             │  - Language Stats │
                             └───────────────────┘
```

## Module Structure

### 1. Cipher Modules (`src/cipher_cryptanalysis/ciphers/`)

**Purpose**: Implement encryption and decryption algorithms

**Components**:
- `caesar.py`: Caesar cipher with configurable alphabet
- `transposition.py`: Columnar transposition cipher

**Design Principles**:
- Each cipher is independent and self-contained
- Consistent interface (encrypt/decrypt methods)
- No dependencies on other modules
- Easy to add new ciphers

**Caesar Cipher Class**:
```python
class CaesarCipher:
    def __init__(self, alphabet_size: int = 26)
    def encrypt(self, plaintext: str, key: int) -> str
    def decrypt(self, ciphertext: str, key: int) -> str
    def get_all_keys(self) -> list[int]
```

**Transposition Cipher Class**:
```python
class TranspositionCipher:
    def __init__(self)
    def encrypt(self, plaintext: str, key: int) -> str
    def decrypt(self, ciphertext: str, key: int) -> str
    def get_possible_keys(self, ciphertext_length: int, max_key: int) -> list[int]
```

### 2. Attack Module (`src/cipher_cryptanalysis/attacks/`)

**Purpose**: Implement cryptanalysis techniques

**Components**:
- `brute_force.py`: Brute force attack for both ciphers

**Design Principles**:
- Generic attack interface that works with any cipher
- Integrates with AI recommender for intelligent ranking
- Returns structured results for easy processing

**BruteForceAttack Class**:
```python
class BruteForceAttack:
    def attack_caesar(self, ciphertext: str, alphabet_size: int) -> List[Tuple[int, str]]
    def attack_transposition(self, ciphertext: str, max_key: int) -> List[Tuple[int, str]]
    def attack_with_ranker(self, ciphertext: str, cipher_type: str, ranker: Callable, 
                          top_n: int, **kwargs) -> List[Tuple[int, str, float]]
```

### 3. AI Recommender (`src/cipher_cryptanalysis/recommender/`)

**Purpose**: Intelligent ranking of decryption candidates

**Components**:
- `plaintext_ranker.py`: Main ranking interface
- `scorer.py`: Individual scoring methods
- `language_stats.py`: English language statistics

**Design Principles**:
- Multiple scoring methods for robustness
- Explainable AI with detailed breakdowns
- Reproducible results (deterministic)
- Extensible for new scoring methods

**PlaintextRanker Class**:
```python
class PlaintextRanker:
    def __init__(self, scoring_method: str = 'hybrid')
    def score(self, text: str) -> float
    def rank(self, candidates: List[Tuple], top_n: int) -> List[Tuple]
    def explain_score(self, text: str) -> Dict[str, float]
    def rank_with_explanation(self, candidates: List[Tuple], top_n: int) -> List[Dict]
```

**TextScorer Class**:
```python
class TextScorer:
    def dictionary_score(self, text: str) -> float
    def bigram_score(self, text: str) -> float
    def trigram_score(self, text: str) -> float
    def frequency_score(self, text: str) -> float
    def perplexity_score(self, text: str) -> float
    def hybrid_score(self, text: str, weights: Dict = None) -> float
```

### 4. CLI Interface (`src/cipher_cryptanalysis/cli.py`)

**Purpose**: User-friendly command-line interface

**Design Principles**:
- Intuitive command structure
- Comprehensive help text
- Rich output formatting
- Error handling and validation

**Command Structure**:
```
cipher-tool
├── caesar
│   ├── encrypt <text> <key> [--alphabet-size]
│   ├── decrypt <text> <key> [--alphabet-size]
│   └── attack <text> [--scoring-method] [--top-n] [--explain]
└── transposition
    ├── encrypt <text> <key>
    ├── decrypt <text> <key>
    └── attack <text> [--max-key] [--scoring-method] [--top-n] [--explain]
```

## Data Flow

### Encryption Flow
```
User Input (plaintext + key)
    ↓
Cipher Module (encrypt method)
    ↓
Ciphertext Output
```

### Attack Flow
```
Ciphertext Input
    ↓
BruteForceAttack (try all keys)
    ↓
List of (key, plaintext) candidates
    ↓
PlaintextRanker (score each candidate)
    ↓
TextScorer (apply scoring methods)
    ↓
Sorted list of (key, plaintext, score)
    ↓
Top N results returned to user
```

### Explainable AI Flow
```
Plaintext candidate
    ↓
TextScorer (calculate all scores)
    ├── Dictionary Score
    ├── Bigram Score
    ├── Trigram Score
    ├── Frequency Score
    └── Perplexity Score
    ↓
PlaintextRanker (combine with weights)
    ↓
Final score + detailed breakdown
```

## Design Patterns

### 1. Strategy Pattern
- Different scoring methods implement the same interface
- Scoring method can be selected at runtime
- Easy to add new scoring strategies

### 2. Factory Pattern (implicit)
- BruteForceAttack creates appropriate cipher instances
- Cipher type determines which attack method is used

### 3. Composition
- PlaintextRanker uses TextScorer
- TextScorer uses language statistics
- Loose coupling between components

## Extension Points

### Adding a New Cipher

1. Create new file in `src/cipher_cryptanalysis/ciphers/`
2. Implement `encrypt()` and `decrypt()` methods
3. Add method to get possible keys
4. Update `BruteForceAttack` to support new cipher
5. Add tests in `tests/`

Example:
```python
class NewCipher:
    def encrypt(self, plaintext: str, key: Any) -> str:
        # Implementation
        pass
    
    def decrypt(self, ciphertext: str, key: Any) -> str:
        # Implementation
        pass
```

### Adding a New Scoring Method

1. Add method to `TextScorer` class
2. Update `PlaintextRanker` to recognize new method
3. Add to `explain_score()` method
4. Update hybrid scoring if needed
5. Add tests in `tests/test_scorer.py`

Example:
```python
def new_score_method(self, text: str) -> float:
    """Description of scoring method."""
    # Calculate score
    return score
```

### Adding a New Attack Method

1. Add method to `BruteForceAttack` class
2. Document expected parameters
3. Return results in standard format
4. Add tests in `tests/test_brute_force.py`

## Testing Strategy

### Unit Tests
- Test each module independently
- Mock external dependencies
- Test edge cases and error conditions
- Aim for >95% code coverage

### Integration Tests
- Test module interactions
- Verify data flow between components
- Test complete attack workflows

### End-to-End Tests
- Test full user workflows
- Verify CLI functionality
- Test with realistic scenarios

## Performance Considerations

### Time Complexity
- **Caesar brute force**: O(26 × n) where n is text length
- **Transposition brute force**: O(k × n) where k is max_key
- **Scoring**: O(n) for each method
- **Overall attack**: O(k × n × m) where m is number of scoring operations

### Space Complexity
- **Caesar**: O(26 × n) for storing all candidates
- **Transposition**: O(k × n) for storing all candidates
- **Ranking**: O(k) for top-N heap (if optimized)

### Optimization Opportunities
1. Parallel processing of candidates
2. Early termination based on score threshold
3. Caching of language statistics
4. Lazy evaluation of scores

## Security Considerations

### Educational Use Only
- This system is for educational purposes
- Classical ciphers are not secure for real-world use
- Demonstrates cryptanalysis techniques

### Code Security
- No external API calls
- No file system access beyond Python imports
- No network access
- Deterministic behavior (no random seeds)

## Dependencies

### Core Dependencies
- Python 3.8+
- NumPy (for numerical operations)

### Development Dependencies
- pytest (testing framework)
- pytest-cov (coverage reporting)

### Design Decision: Minimal Dependencies
- All language statistics are hardcoded
- No heavy ML frameworks required
- Fast installation and deployment
- Easy to audit and understand

## Future Enhancements

### Potential Additions
1. **More Ciphers**: Vigenère, Playfair, Hill cipher
2. **Advanced Attacks**: Frequency analysis, Kasiski examination
3. **Better Language Models**: Larger n-grams, neural language models
4. **Performance**: Parallel processing, GPU acceleration
5. **UI**: Web interface, visualization tools
6. **Analysis Tools**: Frequency charts, pattern detection

### Maintaining Modularity
- Keep ciphers independent
- Maintain consistent interfaces
- Extend, don't modify (Open/Closed Principle)
- Document all public APIs

## Conclusion

The system architecture prioritizes:
- **Modularity**: Independent, reusable components
- **Testability**: Comprehensive test coverage
- **Extensibility**: Easy to add new features
- **Maintainability**: Clear code structure and documentation
- **Usability**: Intuitive CLI and Python API
- **Explainability**: Transparent AI scoring
