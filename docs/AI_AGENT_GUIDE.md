# 🤖 AI AGENT CODING GUIDE FOR CERTEUS

> **Comprehensive coding guide for AI agents (GitHub Copilot, Claude, ChatGPT, etc.)**  
> Version: 1.0 Enterprise  
> Status: MANDATORY for all AI assistance

## 🎯 **Purpose**

This document provides specific guidelines for AI agents working on CERTEUS projects. All AI agents MUST follow these standards to ensure code quality, consistency, and enterprise compliance.

---

## 📋 **TABLE OF CONTENTS**

1. [🏗️ File Headers (ForgeHeader v3)](#file-headers)
2. [🎨 Code Structure & Style](#code-structure)
3. [🔍 Quality Requirements](#quality-requirements)
4. [🧪 Testing Standards](#testing-standards)
5. [🔒 Security Guidelines](#security-guidelines)
6. [📚 Documentation Standards](#documentation-standards)
7. [🔄 Git & CI/CD Integration](#git-cicd)
8. [✅ Quality Checklist](#quality-checklist)

---

## 🏗️ **File Headers (ForgeHeader v3)** {#file-headers}

### **MANDATORY for ALL files**

Every file MUST contain the standardized CERTEUS header:

#### **Python (.py)**
```python
# +=====================================================================+
# |                          CERTEUS                                    |
# +=====================================================================+
# | FILE: services/api_gateway/main.py                                  |
# | ROLE: FastAPI main application entry point                          |
# | PLIK: services/api_gateway/main.py                                  |
# | ROLA: Główny punkt wejścia aplikacji FastAPI                        |
# +=====================================================================+

\"\"\"
PL: Główna aplikacja FastAPI z routerami i middleware.
    Obsługuje autentyfikację, CORS i telemetrię OpenTelemetry.

EN: Main FastAPI application with routers and middleware.
    Handles authentication, CORS and OpenTelemetry telemetry.
\"\"\"
```

#### **TypeScript/JavaScript (.ts/.js)**
```typescript
// +=====================================================================+
// |                          CERTEUS                                    |
// +=====================================================================+
// | FILE: src/components/Dashboard.tsx                                  |
// | ROLE: Main dashboard component with real-time data                  |
// | PLIK: src/components/Dashboard.tsx                                  |
// | ROLA: Główny komponent dashboard z danymi w czasie rzeczywistym     |
// +=====================================================================+

/**
 * PL: Komponent dashboard z real-time danymi i interaktywnymi wykresami.
 *     Wykorzystuje WebSocket dla aktualizacji na żywo.
 *
 * EN: Dashboard component with real-time data and interactive charts.
 *     Uses WebSocket for live updates.
 */
```

#### **YAML (.yml/.yaml)**
```yaml
# +=====================================================================+
# |                          CERTEUS                                    |
# +=====================================================================+
# | FILE: .github/workflows/ci.yml                                      |
# | ROLE: Continuous Integration workflow                               |
# | PLIK: .github/workflows/ci.yml                                      |
# | ROLA: Workflow ciągłej integracji                                   |
# +=====================================================================+

# PL: GitHub Actions workflow dla CI/CD z testami i deployment
# EN: GitHub Actions workflow for CI/CD with tests and deployment

name: ci
```

---

## 🎨 **Code Structure & Style** {#code-structure}

### **Python Standards**

#### **Section-based organization:**
```python
# === IMPORTY / IMPORTS ===
from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# === KONFIGURACJA / CONFIGURATION ===
logger = logging.getLogger(__name__)

# === MODELE / MODELS ===
class UserRequest(BaseModel):
    name: str
    email: str

# === LOGIKA / LOGIC ===
def process_user(request: UserRequest) -> Dict[str, Any]:
    \"\"\"Process user request with validation.\"\"\"
    return {\"status\": \"success\", \"user_id\": 123}
```

#### **Type hints (MANDATORY):**
```python
# ✅ CORRECT - Full type annotations
def calculate_metrics(
    data: List[Dict[str, Any]], 
    threshold: float = 0.5
) -> Tuple[float, bool]:
    \"\"\"Calculate metrics with threshold validation.\"\"\"
    pass

# ❌ INCORRECT - Missing type hints
def calculate_metrics(data, threshold=0.5):
    pass
```

#### **Error handling:**
```python
# ✅ CORRECT - Specific exception handling
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f\"Invalid value: {e}\")
    raise HTTPException(status_code=400, detail=str(e))
except Exception as e:
    logger.error(f\"Unexpected error: {e}\")
    raise HTTPException(status_code=500, detail=\"Internal error\")

# ❌ INCORRECT - Bare except
try:
    result = risky_operation()
except:
    pass
```

### **TypeScript/JavaScript Standards**

#### **Interface definitions:**
```typescript
// ✅ CORRECT - Proper interface with documentation
interface UserProfile {
  /** Unique user identifier */
  id: string;
  /** User display name */
  name: string;
  /** User email address */
  email: string;
  /** Account creation timestamp */
  createdAt: Date;
}

// ✅ CORRECT - Function with proper types
async function fetchUserProfile(userId: string): Promise<UserProfile> {
  const response = await fetch(`/api/users/${userId}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch user: ${response.status}`);
  }
  return response.json();
}
```

---

## 🔍 **Quality Requirements** {#quality-requirements}

### **Code Quality Standards**

1. **Zero warnings/errors in linting**
2. **100% type annotation coverage (Python)**
3. **Comprehensive error handling**
4. **No hardcoded values (use configuration)**
5. **Logging at appropriate levels**
6. **Performance considerations**

### **Performance Guidelines**

```python
# ✅ CORRECT - Efficient operations
def process_large_dataset(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    \"\"\"Process large dataset efficiently with generator.\"\"\"
    return [
        {\"id\": item[\"id\"], \"processed\": True}
        for item in data
        if item.get(\"active\", False)
    ]

# ❌ INCORRECT - Inefficient nested loops
def process_large_dataset(data):
    results = []
    for item in data:
        for key in item:
            if key == \"active\" and item[key]:
                results.append({\"id\": item[\"id\"], \"processed\": True})
    return results
```

---

## 🧪 **Testing Standards** {#testing-standards}

### **Test Coverage Requirements**

- **Unit Tests**: 95%+ coverage
- **Integration Tests**: All API endpoints
- **Property-based Tests**: For complex algorithms
- **Performance Tests**: For critical paths

### **Test Structure**

```python
# test_user_service.py
import pytest
from unittest.mock import Mock, patch

from services.user_service import UserService, UserNotFoundError


class TestUserService:
    \"\"\"Test suite for UserService.\"\"\"
    
    @pytest.fixture
    def user_service(self):
        \"\"\"Create UserService instance for testing.\"\"\"
        return UserService(db_url=\"sqlite:///:memory:\")
    
    def test_get_user_success(self, user_service):
        \"\"\"Test successful user retrieval.\"\"\"
        # Given
        user_id = \"123\"
        expected_user = {\"id\": user_id, \"name\": \"Test User\"}
        
        # When
        with patch.object(user_service, '_fetch_from_db', return_value=expected_user):
            result = user_service.get_user(user_id)
        
        # Then
        assert result == expected_user
    
    def test_get_user_not_found(self, user_service):
        \"\"\"Test user not found scenario.\"\"\"
        # Given
        user_id = \"nonexistent\"
        
        # When/Then
        with patch.object(user_service, '_fetch_from_db', return_value=None):
            with pytest.raises(UserNotFoundError):
                user_service.get_user(user_id)
```

---

## 🔒 **Security Guidelines** {#security-guidelines}

### **Security Checklist**

1. **No hardcoded secrets/passwords**
2. **Input validation and sanitization**
3. **Proper authentication/authorization**
4. **SQL injection prevention**
5. **XSS prevention**
6. **HTTPS/TLS enforcement**

### **Security Code Examples**

```python
# ✅ CORRECT - Secure password handling
import hashlib
import secrets
from typing import Tuple

def hash_password(password: str) -> Tuple[str, str]:
    \"\"\"Hash password with secure salt.\"\"\"
    salt = secrets.token_hex(32)
    password_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return password_hash.hex(), salt

# ✅ CORRECT - Input validation
from pydantic import BaseModel, validator

class UserInput(BaseModel):
    email: str
    age: int
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower().strip()
    
    @validator('age')
    def validate_age(cls, v):
        if v < 0 or v > 150:
            raise ValueError('Age must be between 0 and 150')
        return v
```

---

## 📚 **Documentation Standards** {#documentation-standards}

### **Docstring Requirements**

```python
def complex_calculation(
    data: List[float],
    algorithm: str = \"standard\",
    threshold: Optional[float] = None
) -> Dict[str, Any]:
    \"\"\"
    Perform complex calculation on numerical data.
    
    Args:
        data: List of numerical values to process
        algorithm: Algorithm to use ('standard', 'advanced', 'experimental')
        threshold: Optional threshold for filtering results
        
    Returns:
        Dict containing:
            - result: Calculated value
            - algorithm_used: Algorithm that was applied
            - filtered_count: Number of values after threshold filtering
            
    Raises:
        ValueError: If data is empty or algorithm is unsupported
        TypeError: If data contains non-numerical values
        
    Example:
        >>> data = [1.0, 2.5, 3.2, 4.1]
        >>> result = complex_calculation(data, algorithm=\"advanced\")
        >>> print(result['result'])
        2.7
    \"\"\"
    pass
```

### **README.md Structure**

```markdown
# Project Name

Brief description of what the project does.

## 🚀 Quick Start

\`\`\`bash
# Installation steps
npm install
npm start
\`\`\`

## 📖 Documentation

- [API Documentation](docs/api.md)
- [Configuration Guide](docs/config.md)
- [Deployment Guide](docs/deployment.md)

## 🧪 Testing

\`\`\`bash
# Run tests
npm test

# Run with coverage
npm run test:coverage
\`\`\`

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
```

---

## 🔄 **Git & CI/CD Integration** {#git-cicd}

### **Commit Message Format**

```
🚀 feat: add user authentication system

✅ Features:
- JWT token-based authentication
- Role-based access control
- Password reset functionality

🧪 Tests:
- Unit tests for auth service
- Integration tests for login flow
- Security tests for token validation

🔒 Security:
- Secure password hashing
- Rate limiting for login attempts
- Session management
```

### **Branch Strategy**

- `main` - Production-ready code
- `work/*` - Feature development (recommended)
- `feature/*` - Feature branches
- `hotfix/*` - Critical fixes
- `release/*` - Release preparation

### **Pull Request Template**

```markdown
## 🎯 Description

Brief description of changes and motivation.

## 🧪 Testing

- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## 🔒 Security

- [ ] No hardcoded secrets
- [ ] Input validation implemented
- [ ] Security tests pass

## 📚 Documentation

- [ ] Code documentation updated
- [ ] API documentation updated
- [ ] README updated if needed

## ✅ Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Tests pass locally
- [ ] No breaking changes (or documented)
```

---

## ✅ **Quality Checklist** {#quality-checklist}

### **Before Submitting Code**

#### **Code Quality**
- [ ] ForgeHeader v3 added to all new files
- [ ] Type hints for all function parameters and returns
- [ ] Proper error handling with specific exceptions
- [ ] No hardcoded values (use configuration)
- [ ] Logging at appropriate levels
- [ ] Code is readable and well-structured

#### **Testing**
- [ ] Unit tests cover new functionality
- [ ] Integration tests for API changes
- [ ] Tests pass locally and in CI
- [ ] Performance tests for critical paths
- [ ] Edge cases covered

#### **Security**
- [ ] No secrets in code
- [ ] Input validation implemented
- [ ] SQL injection prevention
- [ ] XSS prevention for web components
- [ ] Authentication/authorization checks

#### **Documentation**
- [ ] Function/class docstrings updated
- [ ] API documentation updated
- [ ] README updated if needed
- [ ] Configuration examples provided

#### **Performance**
- [ ] No obvious performance bottlenecks
- [ ] Database queries optimized
- [ ] Caching implemented where appropriate
- [ ] Memory usage considerations

---

## 🚨 **Common Mistakes to Avoid**

### **For AI Agents**

1. **Missing ForgeHeader** - Every file must have the standardized header
2. **No type hints** - Python functions must have complete type annotations
3. **Bare except clauses** - Always catch specific exceptions
4. **Hardcoded values** - Use configuration or constants
5. **Missing error handling** - Handle all possible error scenarios
6. **No logging** - Add appropriate logging statements
7. **Incomplete docstrings** - Document all parameters and return values
8. **No tests** - Every function needs corresponding tests

### **Quick Validation**

```bash
# Before submitting, run these checks:
python -m mypy .                    # Type checking
python -m ruff check .              # Linting
python -m pytest --cov=. tests/     # Testing with coverage
python -m bandit -r .               # Security scanning
```

---

<div align=\"center\">

**🤖 AI Agent Compliance Required**

*This guide must be followed by all AI assistance tools*

</div>
