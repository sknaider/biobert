# Contributing to BioBERT

Thank you for your interest in contributing to BioBERT! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Style](#code-style)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in all interactions.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/biobert.git
   cd biobert
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/dmis-lab/biobert.git
   ```

## Development Setup

### Using Docker (Recommended)

```bash
# Build and run development container
docker-compose up -d biobert-dev

# Enter the container
docker exec -it biobert-dev bash
```

### Local Setup

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```

## Making Changes

### Branch Naming

- Feature: `feature/description-of-feature`
- Bug fix: `fix/description-of-bug`
- Documentation: `docs/description-of-change`
- Refactoring: `refactor/description-of-change`

### Creating a Branch

```bash
git checkout -b feature/your-feature-name
```

### Development Workflow

1. **Make your changes** following our [code style guidelines](#code-style)

2. **Run linters and formatters:**
   ```bash
   # Format code
   black .
   isort .

   # Check linting
   flake8 .
   pylint *.py

   # Type checking
   mypy .
   ```

3. **Run tests:**
   ```bash
   pytest
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Descriptive commit message"
   ```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest modeling_test.py

# Run tests in parallel
pytest -n auto
```

### Writing Tests

- Place test files next to the code they test with `_test.py` suffix
- Use descriptive test names: `test_<function_name>_<scenario>`
- Include docstrings explaining what the test validates
- Aim for >80% code coverage

Example:
```python
def test_tokenize_basic_text():
    """Test that basic text tokenization works correctly."""
    tokenizer = BasicTokenizer()
    tokens = tokenizer.tokenize("Hello, World!")
    assert tokens == ["hello", ",", "world", "!"]
```

## Code Style

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with the following specifications:

- **Line length:** 100 characters maximum
- **Indentation:** 4 spaces (no tabs)
- **Imports:** Sorted with `isort`, grouped by standard library, third-party, local
- **Formatting:** Automated with `black`
- **Type hints:** Required for all new functions and methods
- **Docstrings:** Google style for all public functions, classes, and modules

### Example Function

```python
from typing import List, Dict, Optional

def process_tokens(
    tokens: List[str],
    vocab: Dict[str, int],
    max_length: Optional[int] = None
) -> List[int]:
    """Convert tokens to IDs using the vocabulary.

    Args:
        tokens: List of string tokens to convert
        vocab: Dictionary mapping tokens to integer IDs
        max_length: Optional maximum sequence length

    Returns:
        List of integer token IDs

    Raises:
        ValueError: If max_length is negative
    """
    if max_length is not None and max_length < 0:
        raise ValueError("max_length must be non-negative")

    ids = [vocab.get(token, vocab["[UNK]"]) for token in tokens]

    if max_length:
        ids = ids[:max_length]

    return ids
```

### Pre-commit Hooks

Pre-commit hooks automatically run on every commit to ensure code quality:

- **Black:** Code formatting
- **isort:** Import sorting
- **flake8:** Linting
- **mypy:** Type checking
- **bandit:** Security scanning
- **trailing-whitespace:** Remove trailing whitespace
- **end-of-file-fixer:** Ensure files end with newline

To run manually:
```bash
pre-commit run --all-files
```

## Submitting Changes

### Pull Request Process

1. **Update your fork:**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request** on GitHub with:
   - Clear title describing the change
   - Detailed description of what and why
   - Reference to any related issues
   - Screenshots/logs if applicable

### Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] All tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated (if applicable)
- [ ] Type hints added to new functions
- [ ] Commit messages are clear and descriptive
- [ ] No merge conflicts with main branch
- [ ] Pre-commit hooks pass
- [ ] Security scan passes (bandit, safety)

### Commit Message Guidelines

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Example:**
```
feat(tokenizer): add support for custom vocabulary

Implement custom vocabulary loading to support domain-specific
tokenization. This allows users to provide their own vocab.txt
files for specialized biomedical terms.

Closes #123
```

## Reporting Issues

### Bug Reports

Include:
- Clear, descriptive title
- Steps to reproduce
- Expected vs actual behavior
- Environment details (Python version, OS, TensorFlow version)
- Error messages and stack traces
- Minimal code example

### Feature Requests

Include:
- Clear description of the feature
- Use case and motivation
- Proposed implementation (if applicable)
- Alternatives considered

## Security Vulnerabilities

**DO NOT** create public issues for security vulnerabilities. Instead, email the maintainers directly at dmis.korea@gmail.com.

## Questions?

- Check existing issues and discussions
- Review documentation
- Ask in GitHub Discussions

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

---

Thank you for contributing to BioBERT! 🧬🤖
