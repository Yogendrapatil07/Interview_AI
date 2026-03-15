# Contributing to InterviewAI

Thank you for your interest in contributing to InterviewAI! This document provides guidelines and information for contributors.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Feature Requests](#feature-requests)

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.9+
- MongoDB 5.0+
- Docker & Docker Compose
- Git

### Setting Up the Development Environment

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/InterviewAI.git
   cd InterviewAI
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   cp .env.example .env
   # Edit .env with your backend URL
   ```

4. **Start MongoDB**
   ```bash
   # Using Docker
   docker run -d -p 27017:27017 --name mongodb mongo:latest
   
   # Or install locally
   mongod
   ```

5. **Run the application**
   ```bash
   # Backend (in terminal 1)
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

   # Frontend (in terminal 2)
   cd frontend
   npm start
   ```

## Code Style

### Backend (Python)

- Follow PEP 8 style guidelines
- Use type hints for function signatures
- Write docstrings for all functions and classes
- Use meaningful variable and function names
- Keep functions small and focused

```python
# Good example
from typing import List
from pydantic import BaseModel

class UserResponse(BaseModel):
    """Response model for user data."""
    id: str
    email: str
    name: str

async def get_user_by_id(user_id: str) -> UserResponse:
    """Get user by ID from database."""
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    return UserResponse(**user)
```

### Frontend (JavaScript/React)

- Use ES6+ features
- Follow Airbnb JavaScript Style Guide
- Use functional components with hooks
- Use meaningful component and variable names
- Keep components small and focused

```javascript
// Good example
import React, { useState, useEffect } from 'react';
import { apiService } from '../services/apiService';

const UserProfile = ({ userId }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const userData = await apiService.get(`/users/${userId}`);
        setUser(userData);
      } catch (error) {
        console.error('Error fetching user:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, [userId]);

  if (loading) return <div>Loading...</div>;
  return <div>{user.name}</div>;
};

export default UserProfile;
```

## Pull Request Process

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the code style guidelines
   - Add tests for new features
   - Update documentation if needed

3. **Test your changes**
   ```bash
   # Run backend tests
   cd backend
   pytest

   # Run frontend tests
   cd frontend
   npm test
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Provide a clear title and description
   - Link any relevant issues
   - Include screenshots if applicable

### Pull Request Template

```markdown
## Description
Brief description of the changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Backend tests pass
- [ ] Frontend tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## Issue Reporting

### Bug Reports

When reporting a bug, please include:

1. **Environment Information**
   - OS version
   - Browser version
   - Application version

2. **Steps to Reproduce**
   - Clear steps to reproduce the issue
   - Expected behavior
   - Actual behavior

3. **Additional Context**
   - Screenshots
   - Error messages
   - Logs

### Bug Report Template

```markdown
## Bug Description
Clear and concise description of the bug.

## Environment
- OS: [e.g. Windows 10, macOS 12.0]
- Browser: [e.g. Chrome 96, Firefox 95]
- Version: [e.g. v1.0.0]

## Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Screenshots
If applicable, add screenshots.

## Additional Context
Any other context about the problem.
```

## Feature Requests

When requesting a new feature:

1. **Use a clear title**
2. **Provide a detailed description**
3. **Explain the use case**
4. **Suggest implementation ideas** (optional)

### Feature Request Template

```markdown
## Feature Description
Clear and concise description of the feature.

## Use Case
Explain why this feature would be useful.

## Proposed Solution
How you envision the feature working.

## Alternatives Considered
Any alternative solutions you've thought about.

## Additional Context
Any other context or screenshots.
```

## Development Guidelines

### Backend Development

- **API Design**: Follow RESTful principles
- **Database**: Use proper indexing and validation
- **Security**: Validate all inputs and use proper authentication
- **Error Handling**: Provide meaningful error messages
- **Testing**: Write unit tests for all API endpoints

### Frontend Development

- **Components**: Keep components reusable and focused
- **State Management**: Use appropriate state management patterns
- **Performance**: Optimize for performance and user experience
- **Accessibility**: Follow WCAG guidelines
- **Testing**: Write tests for critical components

### Database Management

- **Migrations**: Use proper migration scripts
- **Indexes**: Create appropriate indexes for performance
- **Validation**: Use database-level validation
- **Backups**: Regular backup strategy

## Security Guidelines

- Never commit API keys or secrets
- Use environment variables for sensitive data
- Validate all user inputs
- Implement proper authentication and authorization
- Keep dependencies updated

## Performance Guidelines

- Monitor application performance
- Optimize database queries
- Use caching where appropriate
- Minimize bundle size for frontend
- Implement lazy loading for large datasets

## Documentation

- Keep documentation up to date
- Use clear and concise language
- Include code examples
- Document API endpoints
- Provide setup instructions

## Code Review Process

1. **Self-Review**: Review your own code first
2. **Peer Review**: Another developer reviews the code
3. **Testing**: Ensure all tests pass
4. **Documentation**: Update relevant documentation
5. **Merge**: Merge after approval

## Release Process

1. **Version Bumping**: Update version numbers
2. **Changelog**: Update CHANGELOG.md
3. **Testing**: Full regression testing
4. **Deployment**: Deploy to staging first
5. **Release**: Deploy to production

## Community Guidelines

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Help

- **Documentation**: Check the README and docs
- **Issues**: Search existing issues before creating new ones
- **Discussions**: Use GitHub Discussions for questions
- **Discord**: Join our Discord community (link in README)

## License

By contributing to InterviewAI, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to InterviewAI! 🎉
