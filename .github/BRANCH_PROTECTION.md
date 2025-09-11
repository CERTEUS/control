# +=====================================================================+
# |                    ENTERPRISE BRANCH PROTECTION                     |
# +=====================================================================+

# This file defines branch protection rules and repository settings
# for enterprise-grade development workflow

## Main Branch Protection
- **Branch**: `main`
  - Require pull request reviews: ✅ (minimum 1)
  - Require status checks: ✅
  - Require branches to be up to date: ✅
  - Required status checks:
    - `lint/Code Quality & Linting`
    - `security/Security Scan`
    - `type-check/Type Checking`
    - `test/Tests (Python 3.11 on ubuntu-latest)`
  - Restrict pushes to pull requests: ✅
  - Allow force pushes: ❌
  - Allow deletions: ❌
  - Require signed commits: ✅ (recommended)

## Work Branches Protection  
- **Branches**: `work/*`, `feature/*`, `hotfix/*`
  - Require status checks: ✅
  - Required status checks:
    - `lint/Code Quality & Linting`
    - `security/Security Scan`
  - Allow force pushes: ✅ (for work branches)
  - Auto-delete head branches: ✅

## Repository Settings
- Default branch: `main`
- Allow merge commits: ✅
- Allow squash merging: ✅ (preferred)
- Allow rebase merging: ✅
- Auto-delete head branches: ✅
- Automatically delete head branches after merge: ✅

## Security Settings
- Dependency graph: ✅
- Dependabot alerts: ✅
- Dependabot security updates: ✅
- Code scanning alerts: ✅
- Secret scanning: ✅
- Private vulnerability reporting: ✅

## Actions Settings
- Allow GitHub Actions: ✅
- Allow actions created by GitHub: ✅
- Allow actions by Marketplace verified creators: ✅
- Allow specified actions: ✅
  - `actions/checkout@*`
  - `actions/setup-python@*`
  - `docker/*`
  - `aquasecurity/trivy-action@*`
  - `codecov/codecov-action@*`

## Environment Protection
- **Production Environment**:
  - Required reviewers: repository admins
  - Deployment branches: `main` only
  - Wait timer: 5 minutes
  
- **Staging Environment**:
  - Required reviewers: maintainers
  - Deployment branches: `main`, `work/*`
  - Wait timer: 1 minute
