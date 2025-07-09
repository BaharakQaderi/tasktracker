# Contributing to TaskTracker

Thank you for your interest in contributing to TaskTracker! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Bugs

1. **Check existing issues** to see if the bug has already been reported
2. **Create a new issue** with:
   - Clear, descriptive title
   - Detailed description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, Docker version)
   - Error messages or logs

### Suggesting Enhancements

1. **Check existing issues** for similar suggestions
2. **Create a new issue** with:
   - Clear, descriptive title
   - Detailed description of the enhancement
   - Use cases and benefits
   - Possible implementation approach

### Submitting Code Changes

1. **Fork the repository**
2. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following our coding standards
4. **Test your changes** thoroughly
5. **Commit your changes** with clear commit messages
6. **Push to your fork** and submit a pull request

## 🛠️ Development Setup

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Git

### Local Development

1. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/tasktracker.git
   cd tasktracker
   ```

2. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your local settings
   ```

3. **Start development environment**:
   ```bash
   docker-compose up -d
   ```

4. **Install development dependencies** (for local testing):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install pytest pytest-cov black flake8 mypy
   ```

## 📝 Coding Standards

### Python Code Style

- **Follow PEP 8** for Python code style
- **Use Black** for code formatting:
  ```bash
  black app/ tests/
  ```
- **Use meaningful variable and function names**
- **Add type hints** for function parameters and return types
- **Write docstrings** for all classes and functions

### Code Structure

- **Keep functions small** and focused on a single responsibility
- **Use proper error handling** with appropriate exceptions
- **Add logging** for important operations
- **Follow the existing project structure**

### Documentation

- **Update README.md** if adding new features
- **Add docstrings** to new functions and classes
- **Update API documentation** if changing endpoints
- **Add comments** for complex business logic

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_crud.py

# Run tests with verbose output
pytest -v
```

### Writing Tests

- **Write tests** for all new features
- **Test error conditions** and edge cases
- **Use descriptive test names**
- **Follow the existing test structure**
- **Mock external dependencies**

### Test Structure

```
tests/
├── unit/           # Unit tests for individual components
├── integration/    # Integration tests for API endpoints
└── conftest.py     # Shared test fixtures
```

## 📋 Pull Request Guidelines

### Before Submitting

- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No merge conflicts with main branch

### Pull Request Template

1. **Description**: Clear description of changes
2. **Type of Change**:
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
3. **Testing**: How the changes were tested
4. **Checklist**: Confirm all requirements are met

### Review Process

1. **Automated checks** must pass (tests, linting)
2. **Code review** by maintainers
3. **Address feedback** if requested
4. **Merge** after approval

## 🎯 Areas for Contribution

### High Priority

- [ ] Comprehensive test suite
- [ ] User authentication and authorization
- [ ] Task categories/tags
- [ ] Due dates and reminders
- [ ] Search and filtering improvements

### Medium Priority

- [ ] Export functionality (JSON, CSV)
- [ ] Task templates
- [ ] Bulk operations
- [ ] API rate limiting
- [ ] Performance optimizations

### Documentation

- [ ] API examples in multiple languages
- [ ] Deployment guides
- [ ] Architecture deep-dive
- [ ] Video tutorials

## 🚀 Release Process

1. **Feature freeze** for upcoming release
2. **Testing** and bug fixes
3. **Documentation** updates
4. **Version bump** and changelog
5. **Release** with notes

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Code Review**: For feedback on your contributions

## 🙏 Recognition

Contributors are recognized in:
- GitHub contributors list
- Release notes
- Project documentation

Thank you for helping make TaskTracker better! 🚀
