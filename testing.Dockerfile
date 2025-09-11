# +=====================================================================+
# |              CONTROL - Testing Environment Dockerfile               |
# +=====================================================================+
# | FILE: testing.Dockerfile                                            |
# | ROLE: Complete testing environment with all CI tools                |
# +=====================================================================+

FROM python:3.11-slim

# === SYSTEM PACKAGES ===
RUN apt-get update && apt-get install -y \
    # Build tools
    build-essential \
    gcc \
    g++ \
    make \
    cmake \
    # System tools
    curl \
    wget \
    git \
    openssl \
    ca-certificates \
    # Shell tools
    shellcheck \
    jq \
    # Network tools
    netcat-openbsd \
    iputils-ping \
    # FUSE support (for PFS tests)
    fuse \
    libfuse-dev \
    # Clean up
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# === PYTHON ENVIRONMENT ===
WORKDIR /workspace

# Upgrade pip and basic tools
RUN python -m pip install --upgrade pip wheel setuptools

# === CORE DEPENDENCIES ===
COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install -r /tmp/requirements.txt

# === TESTING & CI DEPENDENCIES ===
RUN python -m pip install \
    # Testing framework
    pytest \
    pytest-cov \
    pytest-xdist \
    pytest-asyncio \
    coverage \
    hypothesis \
    # HTTP client for API tests
    httpx \
    # Linting & formatting
    ruff \
    mypy \
    types-requests \
    # Code quality & security
    bandit \
    safety \
    codespell \
    pre-commit \
    # Documentation
    mkdocs \
    mkdocs-material \
    # Supply chain security
    cyclonedx-bom \
    pip-audit \
    # Schema validation
    openapi-spec-validator \
    jsonschema \
    # Cryptography & P2P
    cryptography \
    aioquic \
    oqs \
    # YAML processing
    pyyaml \
    # FUSE filesystem (Linux PFS tests)
    fusepy \
    # Z3 theorem prover
    z3-solver \
    # Core web stack with constraints
    fastapi \
    uvicorn \
    starlette \
    pydantic \
    python-multipart \
    prometheus-client \
    requests

# === PROJECT INSTALLATION ===
COPY . /workspace
RUN python -m pip install -e .

# === ENVIRONMENT SETUP ===
ENV PYTHONPATH="/workspace:$PYTHONPATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# === RUNTIME USER ===
RUN useradd -m -s /bin/bash certeus
RUN chown -R certeus:certeus /workspace
USER certeus

# === EXPOSE PORTS ===
EXPOSE 8000 8081 8082

# === DEFAULT COMMAND ===
CMD ["python", "-m", "uvicorn", "services.api_gateway.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
