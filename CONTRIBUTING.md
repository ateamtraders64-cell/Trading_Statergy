# Contributing Guidelines

Thank you for your interest in contributing to the Trading Strategy project! This guide helps you understand how to contribute effectively.

## Getting Started

1. **Fork the Repository**
   ```bash
   git clone https://github.com/yourusername/Trading_Statergy.git
   cd Trading_Statergy
   ```

2. **Set Up Development Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

3. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### 1. Code Style
- Follow PEP 8 conventions
- Use type hints for all functions
- Maximum line length: 100 characters
- Use meaningful variable names

### 2. Writing Code

```python
def calculate_signal_strength(price_data: Dict, period: int) -> float:
    """
    Calculate signal strength from price data.
    
    Args:
        price_data: Dictionary with price information
        period: Calculation period in days
        
    Returns:
        Float value between 0 and 1
        
    Raises:
        ValueError: If period is invalid
    """
    if period <= 0:
        raise ValueError("Period must be positive")
    
    # Implementation here
    return strength
```

### 3. Testing

Write tests for all new functionality:

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=.

# Run specific test file
pytest tests/test_strategies.py -v
```

### 4. Documentation

- Update docstrings for all functions
- Add comments for complex logic
- Update relevant markdown files in docs/
- Include examples for new features

### 5. Committing Changes

```bash
# Stage changes
git add .

# Commit with clear message
git commit -m "feat: add moving average crossover detection"

# Commit message format:
# feat: new feature
# fix: bug fix
# docs: documentation updates
# test: test additions
# refactor: code refactoring
# perf: performance improvements
```

## Pull Request Process

1. **Before Submitting**
   - Ensure all tests pass: `pytest tests/`
   - Check code quality: `black . && flake8`
   - Update documentation
   - Rebase on latest main branch

2. **Submit PR**
   - Provide clear title and description
   - Reference any related issues
   - Include test results
   - Request review from maintainers

3. **PR Review**
   - Address reviewer comments
   - Make requested changes
   - Push updates to same branch
   - Request re-review

## Code Review Criteria

- Code follows style guidelines
- Tests cover new functionality
- Documentation is comprehensive
- No regression in existing tests
- Performance impact is acceptable
- Security best practices followed

## Adding New Strategies

### 1. Create Strategy Class

```python
# strategies/my_strategy.py
from strategies.base import Strategy, Signal

class MyStrategy(Strategy):
    def __init__(self, parameters: Dict):
        super().__init__('MyStrategy', parameters)
    
    def validate_parameters(self) -> bool:
        required = ['param1', 'param2']
        return all(p in self.parameters for p in required)
    
    def calculate_signals(self, data: Dict) -> List[Signal]:
        signals = []
        # Implementation
        return signals
```

### 2. Register Strategy

```python
# In strategies/base.py
StrategyFactory.register_strategy('my_strategy', MyStrategy)
```

### 3. Add Tests

```python
# tests/test_my_strategy.py
def test_my_strategy_signals():
    params = {'param1': 10, 'param2': 20}
    strategy = MyStrategy(params)
    signals = strategy.calculate_signals(test_data)
    assert len(signals) > 0
```

### 4. Add Configuration

```json
// config/strategy_config.json
"my_strategy_v1": {
  "name": "My Strategy v1",
  "parameters": {
    "param1": 10,
    "param2": 20
  }
}
```

## Reporting Issues

Use GitHub Issues to report bugs or suggest features:

1. **Bug Reports**
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Python version and OS

2. **Feature Requests**
   - Clear use case
   - Proposed implementation (optional)
   - Examples or mockups

## Communication

- Use GitHub Issues for discussions
- Tag maintainers for urgent matters
- Be respectful and constructive
- Follow community code of conduct

## Useful Resources

- [Strategy Guide](docs/01_STRATEGY_GUIDE.md)
- [Architecture Overview](docs/02_ARCHITECTURE.md)
- [Implementation Details](docs/03_IMPLEMENTATION.md)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)

## Questions?

Feel free to reach out:
- **Arun**: arun@example.com (Architecture)
- **Surendar**: surendar@example.com (Implementation)

---

**Thank you for contributing!**
