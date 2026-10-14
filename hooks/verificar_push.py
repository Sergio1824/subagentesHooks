"""Hook pre-push: verifica la suite antes de publicar cambios."""

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "proyecto-demo"


def main() -> int:
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=PROJECT,
        check=False,
    )
    if result.returncode:
        print("Push bloqueado: corrige los errores reportados por las pruebas.", file=sys.stderr)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
