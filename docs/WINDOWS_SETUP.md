# Windows Setup Instructions

## Environment Variables Setup

Add to your system environment or `.env` file:

```properties
# Required for UTF-8 support in Windows terminal
PYTHONIOENCODING=utf-8

# Optional: Docker BuildKit  
DOCKER_BUILDKIT=1
COMPOSE_DOCKER_CLI_BUILD=1

# Optional: Development flags
DEBUG=1
ENVIRONMENT=development
```

## Windows Terminal Configuration

For best emoji and Unicode support:

### Option 1: Windows Terminal Settings
1. Open Windows Terminal
2. Settings (Ctrl+,)
3. Profiles → Defaults
4. Additional settings → Environment variables
5. Add: `PYTHONIOENCODING=utf-8`

### Option 2: PowerShell Profile
Add to `$PROFILE`:
```powershell
$env:PYTHONIOENCODING="utf-8"
```

### Option 3: Global Environment Variable
```cmd
setx PYTHONIOENCODING utf-8
```

## Quick Setup Script (PowerShell)

```powershell
# Set environment variable
$env:PYTHONIOENCODING="utf-8"

# Navigate to project
cd "F:\projekty\control"

# Activate environment
.\.venv\Scripts\Activate.ps1

# Test Control CLI
python -m pkg.control.main health
python -m pkg.control.main status

# Run tests
python -m pytest test/ -v

# Start Docker testing stack
python -m pkg.control.docker start-testing-stack
```

## Verification

Run the verification script:
```bash
set PYTHONIOENCODING=utf-8
python scripts/verify_system.py
```

Should show:
```
🎉 System is READY for production use!
```

## Common Issues

### Unicode Errors
- **Problem**: `UnicodeEncodeError: 'charmap' codec can't encode character`
- **Solution**: Set `PYTHONIOENCODING=utf-8` environment variable

### Docker Issues
- **Problem**: Docker daemon not accessible
- **Solution**: Start Docker Desktop, ensure WSL integration enabled

### Git Issues  
- **Problem**: Line ending issues
- **Solution**: `git config core.autocrlf false`

### Python Path Issues
- **Problem**: VS Code can't find Python interpreter
- **Solution**: Ctrl+Shift+P → "Python: Select Interpreter" → Choose `.venv/Scripts/python.exe`
