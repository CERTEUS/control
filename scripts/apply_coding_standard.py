#!/usr/bin/env python3
# +=====================================================================+
# |                          CERTEUS                                    |
# +=====================================================================+
# | FILE: tools/apply_coding_standard.py                               |
# | ROLE: Application module                                           |
# | PLIK: tools/apply_coding_standard.py                               |
# | ROLA: Moduł aplikacji                                              |
# +=====================================================================+

"""
PL: Moduł zapewniający funkcjonalność apply_coding_standard

EN: Module providing apply_coding_standard functionality
"""

# === IMPORTY / IMPORTS ===

# === IMPORTY / IMPORTS ===
from __future__ import annotations

import re
import sys
from pathlib import Path

# === KONFIGURACJA / CONFIGURATION ===

# ForgeHeader v3 templates
PYTHON_HEADER_TEMPLATE = '''

"""
PL: {description_pl}

EN: {description_en}
"""

# === IMPORTY / IMPORTS ===

from __future__ import annotations

'''

BASH_HEADER_TEMPLATE = """#!/usr/bin/env bash

# PL: {description_pl}
# EN: {description_en}

set -Eeuo pipefail
trap 'echo "[ERR] $0 line:$LINENO status:$?" >&2' ERR

"""

# Patterns for different file types
CERTEUS_BANNER_PATTERN = re.compile(
    r"# \+[=\-]+\+.*?CERTEUS.*?\+[=\-]+\+.*?(?=\n[^#]|\n\n|\Z)", re.DOTALL | re.MULTILINE
)

SHEBANG_PATTERN = re.compile(r"^#![^\n]*\n")
ENCODING_PATTERN = re.compile(r"^# -\*- coding:[^\n]*\n")

# === MODELE / MODELS ===


class FileUpdater:
    """
    PL: Klasa odpowiedzialna za aktualizację plików zgodnie ze standardem.
    EN: Class responsible for updating files according to the standard.
    """

    def __init__(self, workspace_root: Path) -> None:
        self.workspace_root = workspace_root
        self.updated_files: list[Path] = []
        self.errors: list[str] = []

    # === LOGIKA / LOGIC ===

    def _detect_file_info(self, file_path: Path) -> dict[str, str]:
        """
        PL: Wykrywa informacje o pliku na podstawie ścieżki i zawartości.
        EN: Detects file information based on path and content.
        """
        relative_path = file_path.relative_to(self.workspace_root)
        path_str = str(relative_path).replace("\\", "/")

        # Detect role based on file path and name
        if "test_" in file_path.name or file_path.parent.name == "tests":
            role = "Test module for automated testing"
            role_pl = "Moduł testowy do automatycznych testów"
        elif file_path.name == "__init__.py":
            role = "Package initialization module"
            role_pl = "Moduł inicjalizacji pakietu"
        elif file_path.name == "main.py":
            role = "Main application entry point"
            role_pl = "Główny punkt wejścia aplikacji"
        elif "manager" in file_path.name:
            role = "Manager module for business logic"
            role_pl = "Moduł menedżera logiki biznesowej"
        elif "api" in file_path.name or "router" in file_path.name:
            role = "API endpoint and routing module"
            role_pl = "Moduł endpoint API i routingu"
        elif file_path.suffix == ".sh":
            role = "Shell script for automation"
            role_pl = "Skrypt shell do automatyzacji"
        elif file_path.suffix in [".yml", ".yaml"]:
            role = "Configuration file"
            role_pl = "Plik konfiguracyjny"
        else:
            role = "Application module"
            role_pl = "Moduł aplikacji"

        # Generate descriptions
        if "control" in path_str:
            desc_en = f"Control workspace management module for {file_path.stem}"
            desc_pl = f"Moduł zarządzania workspace control dla {file_path.stem}"
        elif "certeus" in path_str:
            desc_en = f"CERTEUS enterprise module for {file_path.stem}"
            desc_pl = f"Moduł enterprise CERTEUS dla {file_path.stem}"
        else:
            desc_en = f"Module providing {file_path.stem} functionality"
            desc_pl = f"Moduł zapewniający funkcjonalność {file_path.stem}"

        return {
            "file_path": path_str,
            "role": role,
            "role_pl": role_pl,
            "description_en": desc_en,
            "description_pl": desc_pl,
        }

    def _remove_existing_headers(self, content: str) -> str:
        """
        PL: Usuwa istniejące nagłówki CERTEUS z pliku.
        EN: Removes existing CERTEUS headers from file.
        """
        # Remove CERTEUS banner blocks
        content = CERTEUS_BANNER_PATTERN.sub("", content)

        # Remove multiple consecutive empty lines
        content = re.sub(r"\n\n\n+", "\n\n", content)

        return content.strip()

    def _update_python_file(self, file_path: Path) -> bool:
        """
        PL: Aktualizuje plik Python zgodnie ze standardem v3.0.
        EN: Updates Python file according to standard v3.0.
        """
        try:
            with file_path.open(encoding="utf-8") as f:
                original_content = f.read()

            info = self._detect_file_info(file_path)

            # Remove existing headers and docstrings
            content = self._remove_existing_headers(original_content)

            # Handle shebang and encoding
            shebang_match = SHEBANG_PATTERN.match(content)
            shebang = shebang_match.group(0) if shebang_match else ""
            if shebang:
                content = content[len(shebang) :]

            encoding_match = ENCODING_PATTERN.match(content)
            encoding = encoding_match.group(0) if encoding_match else ""
            if encoding:
                content = content[len(encoding) :]

            # Remove old docstrings at the beginning
            content = re.sub(r'^[\s]*""".*?"""[\s]*', "", content, flags=re.DOTALL)
            content = re.sub(r"^[\s]*\'\'\'.*?\'\'\'[\s]*", "", content, flags=re.DOTALL)

            # Build new content
            header = PYTHON_HEADER_TEMPLATE.format(**info)
            new_content = shebang + encoding + header + content.lstrip()

            # Only write if content changed
            if new_content != original_content:
                with file_path.open("w", encoding="utf-8") as f:
                    f.write(new_content)
                self.updated_files.append(file_path)
        except Exception as e:
            self.errors.append(f"Error updating {file_path}: {e}")
            return False
        else:
            return new_content != original_content

    def _update_bash_file(self, file_path: Path) -> bool:
        """
        PL: Aktualizuje plik bash zgodnie ze standardem v3.0.
        EN: Updates bash file according to standard v3.0.
        """
        try:
            with file_path.open(encoding="utf-8") as f:
                original_content = f.read()

            info = self._detect_file_info(file_path)

            # Remove existing headers
            content = self._remove_existing_headers(original_content)

            # Remove old shebang if present
            content = SHEBANG_PATTERN.sub("", content)

            # Build new content
            header = BASH_HEADER_TEMPLATE.format(**info)
            new_content = header + content.lstrip()

            # Only write if content changed
            if new_content != original_content:
                with file_path.open("w", encoding="utf-8") as f:
                    f.write(new_content)
                self.updated_files.append(file_path)
        except Exception as e:
            self.errors.append(f"Error updating {file_path}: {e}")
            return False
        else:
            return new_content != original_content

    def update_project_files(self) -> None:
        """
        PL: Aktualizuje wszystkie pliki w projektach Control i Certeus.
        EN: Updates all files in Control and Certeus projects.
        """
        print("🔄 Applying CERTEUS Enterprise Coding Standard v3.0...")  # noqa: T201  # Script output

        # Define file patterns to update
        patterns = [
            "**/*.py",
            "**/*.sh",
        ]

        # Define exclusions
        exclusions = {
            ".venv",
            "__pycache__",
            ".git",
            "node_modules",
            "dist",
            "build",
            ".pytest_cache",
            ".ruff_cache",
            ".mypy_cache",
        }

        for pattern in patterns:
            for file_path in self.workspace_root.glob(pattern):
                # Skip excluded directories
                if any(excl in file_path.parts for excl in exclusions):
                    continue

                if not file_path.is_file():
                    continue

                print(f"Processing: {file_path.relative_to(self.workspace_root)}")  # noqa: T201  # Script output

                if file_path.suffix == ".py":
                    self._update_python_file(file_path)
                elif file_path.suffix == ".sh":
                    self._update_bash_file(file_path)


# === I/O / ENDPOINTS ===


def main() -> None:
    """
    PL: Główna funkcja skryptu.
    EN: Main script function.
    """
    workspace_root = Path(__file__).parent.parent

    updater = FileUpdater(workspace_root)
    updater.update_project_files()

    print(f"\n✅ Updated {len(updater.updated_files)} files")  # noqa: T201  # Script output

    if updater.errors:
        print(f"❌ {len(updater.errors)} errors occurred:")  # noqa: T201  # Script output
        for error in updater.errors:
            print(f"  - {error}")  # noqa: T201  # Script output
        sys.exit(1)

    print("🎉 All files updated successfully according to CERTEUS Enterprise Standard v3.0!")  # noqa: T201  # Script output


if __name__ == "__main__":
    main()
