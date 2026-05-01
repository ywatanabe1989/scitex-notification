"""PS303 example mirror stub: ensure examples/01_alert_demo.py is syntactically valid."""

import subprocess
import sys
from pathlib import Path

EXAMPLE = Path(__file__).resolve().parents[2] / "examples" / "01_alert_demo.py"


def test_01_alert_demo_compiles():
    assert EXAMPLE.exists(), f"missing example: {EXAMPLE}"
    subprocess.run(
        [sys.executable, "-m", "py_compile", str(EXAMPLE)],
        check=True,
    )
