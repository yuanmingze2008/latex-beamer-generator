from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile a generated Beamer project if latexmk is available.")
    parser.add_argument("--project-dir", required=True, help="Directory containing main.tex.")
    parser.add_argument("--clean", action="store_true", help="Run latexmk cleanup after compilation.")
    args = parser.parse_args()

    project_dir = Path(args.project_dir)
    main_tex = project_dir / "main.tex"
    if not main_tex.exists():
        raise SystemExit(f"main.tex not found in {project_dir}")

    latexmk = shutil.which("latexmk")
    if not latexmk:
        raise SystemExit("latexmk is not available in PATH")

    subprocess.run(
        [latexmk, "-pdf", "-interaction=nonstopmode", "main.tex"],
        cwd=project_dir,
        check=True,
    )

    if args.clean:
        subprocess.run([latexmk, "-c"], cwd=project_dir, check=True)


if __name__ == "__main__":
    main()
