# Contributing to Voice Cloner

Thank you for your interest in contributing to Voice Cloner! We welcome contributions from everyone.

## 📝 Code of Conduct

This project follows a simple code of conduct: **Be kind, be respectful, be inclusive.**

- Treat everyone with respect
- Be welcoming to newcomers
- Give constructive feedback
- Accept that differences of opinion are normal

## 🎯 Ways to Contribute

### 1. Reporting Bugs

If you find a bug, please:

1. Check if it's already been reported in the [Issues](https://github.com/your-username/voice-cloner/issues)
2. Create a new issue with:
   - Clear title describing the problem
   - Steps to reproduce
   - Expected vs. actual behavior
   - Your environment (OS, Python version, etc.)
   - Error messages (full traceback)
   - Sample files (if applicable and not private)

### 2. Suggesting Features

Have an idea for a new feature?

1. Check existing [feature requests](https://github.com/your-username/voice-cloner/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)
2. Open a new issue with the `[enhancement]` label
3. Describe:
   - What the feature should do
   - Why it would be useful
   - Any implementation ideas

### 3. Contributing Code

We welcome pull requests! Here's how to contribute:

#### Fork the Repository

```bash
git fork https://github.com/your-username/voice-cloner.git
cd voice-cloner
git checkout -b feature/your-feature-name
```

#### Make Your Changes

- Follow [Code Style](#-code-style) guidelines
- Add tests for new functionality
- Update documentation as needed
- Keep commits atomic and well-described

#### Submit a Pull Request

1. Push your changes:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Open a Pull Request to the `main` branch
3. Fill out the PR template
4. Wait for review and address any feedback

### 4. Improving Documentation

Good documentation is crucial! You can help by:

- Fixing typos and grammatical errors
- Adding missing information
- Creating examples and tutorials
- Improving existing docs for clarity

### 5. Testing

Help improve the test suite by:

- Adding tests for untested functionality
- Reporting test failures
- Improving test coverage

## 🚀 Getting Started with Development

### Prerequisites

- Python 3.8+
- Git
- FFmpeg
- pip

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/your-username/voice-cloner.git
cd voice-cloner

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install in development mode
pip install -e .
```

### requirements-dev.txt

Additional packages for development:

```
pytest
pytest-cov
black
flake8
mypy
isort
Sphinx
```

### Run Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_extraction.py

# Run with verbose output
pytest -v tests/
```

## 📛 Code Style

This project follows PEP 8 style guidelines with the following conventions:

### Python

- **Indentation**: 4 spaces (no tabs)
- **Line Length**: 88 characters maximum
- **Naming**:
  - Variables and functions: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`
  - Private: `_leading_underscore`
- **Imports**: Group by standard library, third-party, local (with blank lines between)
- **Type Hints**: Use type hints for function signatures and variables
- **Docstrings**: Use Google-style docstrings

### Example Code Style

```python
"""Module docstring."""

from typing import Optional, List
import os
import sys


class VoiceCloner:
    """Main voice cloning class.
    
    Attributes:
        sample_rate: The audio sample rate in Hz.
        method: The cloning method to use.
    """
    
    def __init__(self, sample_rate: int = 44100, method: str = "rvc"):
        """Initialize the voice cloner.
        
        Args:
            sample_rate: Audio sample rate in Hz.
            method: Cloning method ('rvc' or 'simple').
        """
        self.sample_rate = sample_rate
        self.method = method
    
    def clone_voice(self, input_path: str, output_path: str) -> str:
        """Clone a voice from input to output.
        
        Args:
            input_path: Path to input audio file.
            output_path: Path to save cloned voice.
            
        Returns:
            Path to the output file.
            
        Raises:
            FileNotFoundError: If input file doesn't exist.
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Implementation here
        return output_path
```

### Formatting Tools

We use the following tools to maintain code quality:

- **Black**: Auto-formatter (line length: 88)
- **isort**: Import sorter
- **flake8**: Linter (PEP 8 compliance)
- **mypy**: Static type checker

Run formatting:

```bash
# Format all Python files
black src/ tests/

# Sort imports
isort src/ tests/

# Check PEP 8 compliance
flake8 src/ tests/

# Type checking
mypy src/
```

## 📜 Commit Message Guidelines

Use clear, descriptive commit messages following this format:

```
type(scope): description

[optional body]

[optional footer]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

### Examples

```bash
# Good commit messages
feat(audio): add support for FLAC input files
fix(isolation): handle edge case with silent audio
refactor(cloning): simplify voice model training loop
docs: update README with installation instructions
style: format code with black

# Bad commit messages (avoid these)
fix bug
update code
wip
changes
```

## ✅ Pull Request Guidelines

### PR Template

Every PR should include:

1. **Title**: Clear, descriptive title prefixed with type (e.g., `[feat] Add video support`)
2. **Description**: What does this PR do?
3. **Related Issues**: Link to any related issues
4. **Changes Made**: List of changes
5. **Testing**: How you tested your changes
6. **Checklist**:
   - [ ] Code follows style guidelines
   - [ ] All tests pass
   - [ ] Documentation updated
   - [ ] New tests added for new functionality

### Review Process

1. At least one maintainer must review and approve
2. All CI checks must pass
3. Code must follow style guidelines
4. Tests must pass with good coverage
5. Documentation must be updated if needed

## 🎓 Good First Issues

New to open source? Here are some good starting points:

1. **Documentation**: Improve existing docs, add examples
2. **Tests**: Add tests for untested code paths
3. **Code Cleanup**: Fix linting issues, improve code style
4. **Simple Features**: Add support for new audio formats
5. **Bug Fixes**: Fix reported issues

Look for issues with the `[good first issue]` label.

## 🏆 Recognition

All contributors will be recognized in:

- The [CONTRIBUTORS.md](CONTRIBUTORS.md) file
- Release notes for significant contributions
- GitHub contribution graph

## 📞 Need Help?

If you have questions about contributing:

1. Check this document first
2. Look at existing PRs and issues for examples
3. Ask in the [Discussions](https://github.com/your-username/voice-cloner/discussions)
4. Open an issue with your question

---

Thank you for contributing to Voice Cloner! Your help makes this project better for everyone.
