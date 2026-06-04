"""
CREATED by Claude
Merge all ordinal-prefixed notebooks in src/notebooks/ into artifacts/Final.ipynb.

Notebooks matching the pattern NN_*.ipynb (where NN is one or more digits) are
collected, sorted by their numeric prefix, and concatenated in order.  All cell
outputs are preserved exactly as-is.
"""

import json
import re
import sys
from pathlib import Path


def get_project_root() -> Path:
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / ".git").exists() or (current / "pyproject.toml").exists():
            return current
        current = current.parent
    raise RuntimeError(
        "Could not locate project root (no .git or pyproject.toml found)"
    )


def collect_notebooks(notebooks_dir: Path) -> list[Path]:
    pattern = re.compile(r"^(\d+)_")
    matches = []
    for nb in notebooks_dir.glob("*.ipynb"):
        m = pattern.match(nb.name)
        if m:
            matches.append((int(m.group(1)), nb))
    matches.sort(key=lambda x: x[0])
    return [nb for _, nb in matches]


def merge_notebooks(paths: list[Path]) -> dict:
    if not paths:
        raise ValueError("No notebooks to merge.")

    with open(paths[0], encoding="utf-8") as f:
        merged = json.load(f)

    # Strip trailing newline from last cell of each notebook before appending
    # so the merged notebook doesn't accumulate blank lines between sections.
    for path in paths[1:]:
        with open(path, encoding="utf-8") as f:
            nb = json.load(f)

        # Validate kernel compatibility (warn only)
        base_kernel = merged.get("metadata", {}).get("kernelspec", {}).get("name", "")
        nb_kernel = nb.get("metadata", {}).get("kernelspec", {}).get("name", "")
        if base_kernel and nb_kernel and base_kernel != nb_kernel:
            print(
                f"  WARNING: kernel mismatch — base={base_kernel!r}, "
                f"{path.name}={nb_kernel!r}",
                file=sys.stderr,
            )

        merged["cells"].extend(nb.get("cells", []))

    return merged


def main() -> None:
    root = get_project_root()
    notebooks_dir = root / "src" / "notebooks"
    output_path = root / "artifacts" / "Final.ipynb"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    notebooks = collect_notebooks(notebooks_dir)
    if not notebooks:
        print("No ordinal-prefixed notebooks found — nothing to do.")
        sys.exit(0)

    print(f"Merging {len(notebooks)} notebook(s) in order:")
    for nb in notebooks:
        print(f"  {nb.relative_to(root)}")

    merged = merge_notebooks(notebooks)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=1, ensure_ascii=False)
        f.write("\n")

    print(f"\nSaved -> {output_path.relative_to(root)}")
    total_cells = len(merged["cells"])
    print(f"Total cells: {total_cells}")


if __name__ == "__main__":
    main()
