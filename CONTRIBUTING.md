# Contributing to Chemical Equipment Visualizer

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Maintain professional communication

## Getting Started

1. **Fork the repository**
   - Click the "Fork" button on GitHub
   - Clone your fork locally

2. **Set up development environment**
   - Follow [INSTALLATION.md](./INSTALLATION.md) for setup
   - Ensure all tests pass before making changes

3. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines

### Code Style

#### Python (Backend & Desktop)
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Maximum line length: 100 characters

```python
def calculate_average(values: List[float]) -> float:
    """
    Calculate the average of a list of values.
    
    Args:
        values: List of numeric values.
        
    Returns:
        Average value as float.
    """
    return sum(values) / len(values) if values else 0.0
```

#### JavaScript/React (Frontend)
- Use ES6+ features
- Follow Airbnb JavaScript Style Guide
- Use functional components with hooks
- Use meaningful variable names

```javascript
// Good
const fetchUserData = async (userId) => {
  const response = await api.get(`/users/${userId}`);
  return response.data;
};

// Avoid
const f = async (id) => {
  const r = await api.get(`/users/${id}`);
  return r.data;
};
```

### Project Structure

- **Backend**: Django apps should be self-contained with models, views, serializers, and services
- **Frontend**: Components should be reusable and follow single responsibility principle
- **Desktop**: UI widgets should match web components for consistency

### Commit Messages

Use conventional commit format:

```
type(scope): subject

body (optional)

footer (optional)
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(backend): add equipment filtering by type

fix(frontend): resolve CORS issue on upload

docs(readme): update installation instructions

refactor(desktop): improve API client error handling
```

### Testing

#### Backend Tests
```bash
cd backend
pytest
```

Write tests for:
- API endpoints
- Business logic in services
- Data validation
- Authentication flows

#### Frontend Tests
```bash
cd frontend
npm test
```

Write tests for:
- Component rendering
- User interactions
- API integration
- Custom hooks

### Pull Request Process

1. **Update your branch**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests**
   - Ensure all tests pass
   - Add tests for new features
   - Verify no regressions

3. **Update documentation**
   - Update README if needed
   - Add/update docstrings
   - Update API documentation

4. **Create pull request**
   - Use descriptive title
   - Reference related issues
   - Describe changes clearly
   - Add screenshots for UI changes

5. **Code review**
   - Address reviewer feedback
   - Keep discussions professional
   - Update PR as needed

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots for UI changes

## Related Issues
Closes #123
```

## Areas for Contribution

### High Priority
- [ ] Add unit tests for backend services
- [ ] Add integration tests for API endpoints
- [ ] Improve error handling and user feedback
- [ ] Add data export formats (Excel, JSON)
- [ ] Implement user preferences/settings

### Features
- [ ] Advanced filtering and search
- [ ] Data comparison between datasets
- [ ] Custom chart types
- [ ] Email notifications
- [ ] Batch file upload
- [ ] API rate limiting
- [ ] Caching layer

### Documentation
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Video tutorials
- [ ] Architecture diagrams
- [ ] Deployment guides for other platforms

### Desktop Application
- [ ] Offline mode support
- [ ] Local database caching
- [ ] Keyboard shortcuts
- [ ] Dark/light theme toggle
- [ ] Export to multiple formats

## Bug Reports

When reporting bugs, include:

1. **Description**: Clear description of the issue
2. **Steps to reproduce**: Detailed steps
3. **Expected behavior**: What should happen
4. **Actual behavior**: What actually happens
5. **Environment**:
   - OS and version
   - Python/Node.js version
   - Browser (for frontend issues)
6. **Screenshots**: If applicable
7. **Logs**: Relevant error messages

**Template:**
```markdown
**Bug Description**
Brief description

**Steps to Reproduce**
1. Go to...
2. Click on...
3. See error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: macOS 13.0
- Python: 3.11
- Browser: Chrome 120

**Screenshots**
[Add screenshots]

**Additional Context**
Any other relevant information
```

## Feature Requests

When requesting features, include:

1. **Problem**: What problem does this solve?
2. **Solution**: Proposed solution
3. **Alternatives**: Alternative solutions considered
4. **Use case**: Real-world use case
5. **Priority**: How important is this?

## Development Setup Tips

### Backend Development
```bash
# Run with auto-reload
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Run specific tests
pytest backend/apps/equipment/tests/test_views.py

# Check code style
flake8 backend/
```

### Frontend Development
```bash
# Run with hot reload
npm run dev

# Build for production
npm run build

# Lint code
npm run lint

# Preview production build
npm run preview
```

### Desktop Development
```bash
# Run application
python main.py

# Check for PyQt5 issues
python -c "from PyQt5 import QtWidgets; print('PyQt5 OK')"
```

## Questions?

- Open an issue for questions
- Check existing issues and PRs
- Review documentation first

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing! 🎉
