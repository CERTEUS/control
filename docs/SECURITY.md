# 🔐 Enterprise Security Guide

## Overview

This document outlines the security architecture and best practices for the Control platform. The platform follows enterprise-grade security standards with centralized key management, secure authentication, and comprehensive access controls.

## 🏗️ Security Architecture

### Key Management Structure
```
control/
├── internal/
│   ├── keys/                    # 🔒 Centralized key storage
│   │   ├── github-app-private-key.pem
│   │   ├── GITHUB_TOKEN.txt
│   │   └── *.pem, *.key        # All private keys
│   └── config/                  # Configuration files
├── .env                         # 🚫 Environment variables (git-ignored)
├── .env.example                 # ✅ Template file (safe for git)
└── .gitignore                   # Security exclusion patterns
```

### Security Layers

#### 1. Environment Variable Protection
- All sensitive values stored in `.env` file
- Environment variables take priority over file-based keys
- Production environments use secure secret management

#### 2. Key File Protection
- All private keys stored in `internal/keys/` directory
- Directory excluded from version control
- Strict file permissions enforced

#### 3. Git Security
- Comprehensive `.gitignore` patterns
- Automatic exclusion of common secret patterns
- Protected against accidental commits

## 🔑 Authentication Methods

### GitHub App Authentication (Recommended)

1. **Setup GitHub App**
   ```bash
   # Create GitHub App in your organization
   # Download private key to internal/keys/
   cp downloaded-private-key.pem internal/keys/github-app-private-key.pem
   ```

2. **Configure Environment**
   ```bash
   # Copy example configuration
   cp .env.example .env
   
   # Edit with your values
   vim .env
   ```

3. **Environment Variables**
   ```env
   GH_APP_ID=123456
   GH_APP_INSTALLATION_ID=789012
   GH_APP_PRIVATE_KEY_PATH=internal/keys/github-app-private-key.pem
   ```

### Personal Access Token (Alternative)

```env
GITHUB_TOKEN=ghp_your_personal_access_token_here
```

## 🛡️ Security Best Practices

### Development Environment

1. **Never commit secrets to git**
   ```bash
   # Check before committing
   git status
   git diff --cached
   ```

2. **Use proper file permissions**
   ```bash
   chmod 600 internal/keys/*.pem
   chmod 700 internal/keys/
   ```

3. **Validate .gitignore coverage**
   ```bash
   # Ensure no tracked secrets
   git check-ignore internal/keys/
   git ls-files | grep -E '\.(pem|key)$'
   ```

### Production Environment

1. **Use environment-based secrets**
   - GitHub Codespaces: Repository secrets
   - CI/CD: Encrypted environment variables
   - Docker: Secret management systems

2. **Regular key rotation**
   ```bash
   # Generate new GitHub App key
   # Update in secure storage
   # Remove old key files
   ```

3. **Audit trail**
   - Log all authentication attempts
   - Monitor key usage patterns
   - Track access to sensitive operations

## 🚨 Security Incidents

### Key Compromise Response

1. **Immediate Actions**
   ```bash
   # Revoke compromised key
   # Generate new credentials
   # Update all environments
   ```

2. **Investigation**
   - Review git history for leaked secrets
   - Check access logs
   - Identify potential exposure scope

3. **Recovery**
   - Deploy new credentials
   - Verify system integrity
   - Document incident for future prevention

### Common Vulnerabilities

#### Accidental Git Commits
```bash
# Remove from history if committed
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch internal/keys/*' \
  --prune-empty --tag-name-filter cat -- --all
```

#### Environment Variable Exposure
- Never log environment variables
- Sanitize debug output
- Use secure variable substitution

## 🔍 Security Auditing

### Regular Checks

1. **Dependency Scanning**
   ```bash
   pip audit
   safety check
   ```

2. **Secret Detection**
   ```bash
   git secrets --scan
   truffleHog --regex --entropy=False .
   ```

3. **Permission Validation**
   ```bash
   find internal/keys/ -type f -exec ls -la {} \;
   ```

### Compliance Standards

- **SOC 2 Type II**: Access controls and monitoring
- **ISO 27001**: Information security management
- **GDPR**: Data protection and privacy
- **OWASP**: Secure coding practices

## 📞 Security Contacts

| Role | Contact | Responsibility |
|------|---------|----------------|
| Security Lead | security@company.com | Overall security strategy |
| DevOps Team | devops@company.com | Infrastructure security |
| Compliance | compliance@company.com | Regulatory requirements |

## 📚 Additional Resources

- [GitHub App Authentication](https://docs.github.com/en/developers/apps/building-github-apps/authenticating-with-github-apps)
- [Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [Enterprise Security Best Practices](https://enterprise.github.com/security)
- [OWASP Secure Coding Guidelines](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)

---

**⚠️ Remember**: Security is everyone's responsibility. When in doubt, err on the side of caution and consult the security team.
