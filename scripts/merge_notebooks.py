"""
CREATED by Claude
Merge all ordinal-prefixed notebooks in src/notebooks/ into artifacts/Final.ipynb.

Notebooks matching the pattern NN_*.ipynb (where NN is one or more digits) are
collected, sorted by their numeric prefix, executed end-to-end (each in its own
fresh kernel) to populate fresh outputs, and concatenated in order.  The source
notebooks on disk are never modified — outputs only live in the merged artifact.
"""

import re
import sys
from pathlib import Path

# Generous per-cell timeout (seconds) so model-training cells don't get killed.
CELL_TIMEOUT = 1200


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
    # Match a numeric prefix followed by an optional letter suffix, e.g.
    # "03_", "03a_", "03b_". The suffix lets several notebooks share the same
    # ordinal while keeping an explicit order (03a before 03b).
    pattern = re.compile(r"^(\d+)([a-zA-Z]*)_")
    matches = []
    for nb in notebooks_dir.glob("*.ipynb"):
        m = pattern.match(nb.name)
        if m:
            matches.append((int(m.group(1)), m.group(2).lower(), nb))
    # Sort by numeric prefix, then letter suffix, then filename so notebooks
    # sharing a prefix (e.g. 03_modeling_andre, 03_modeling_michael or
    # 03a_..., 03b_...) merge in a stable, deterministic order instead of
    # filesystem-dependent glob order.
    matches.sort(key=lambda x: (x[0], x[1], x[2].name))
    return [nb for _, _, nb in matches]


def execute_notebook(path: Path):
    """Read a notebook and run it end-to-end in a fresh kernel, returning the
    executed NotebookNode. A cell error raises CellExecutionError, which we let
    propagate so the build fails instead of producing a half-baked artifact."""
    import nbformat
    from nbclient import NotebookClient

    with open(path, encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    kernel_name = nb.get("metadata", {}).get("kernelspec", {}).get("name") or "python3"
    client = NotebookClient(
        nb,
        timeout=CELL_TIMEOUT,
        kernel_name=kernel_name,
        # Run with the kernel cwd set to the notebook's own directory.
        resources={"metadata": {"path": str(path.parent)}},
    )
    client.execute()
    return nb


def merge_notebooks(paths: list[Path]):
    if not paths:
        raise ValueError("No notebooks to merge.")

    print(f"  Executing {paths[0].name} ...")
    merged = execute_notebook(paths[0])

    for path in paths[1:]:
        print(f"  Executing {path.name} ...")
        nb = execute_notebook(path)

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


def export_pdf(nb, ipynb_path: Path) -> None:
    import asyncio
    # Windows Store Python uses SelectorEventLoop by default, which cannot spawn
    # subprocesses — Playwright requires ProactorEventLoop on Windows.
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    from nbconvert import WebPDFExporter

    pdf_path = ipynb_path.with_suffix(".pdf")

    exporter = WebPDFExporter()
    pdf_data, _ = exporter.from_notebook_node(nb)

    with open(pdf_path, "wb") as f:
        f.write(pdf_data)

    print(f"Saved -> {pdf_path.relative_to(ipynb_path.parent.parent)}")


def main() -> None:
    root = get_project_root()
    notebooks_dir = root / "src" / "notebooks"
    output_path = root / "artifacts" / "Final-Project-Report-Team-3.ipynb"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    notebooks = collect_notebooks(notebooks_dir)
    if not notebooks:
        print("No ordinal-prefixed notebooks found — nothing to do.")
        sys.exit(0)

    print(f"Merging {len(notebooks)} notebook(s) in order:")
    for nb in notebooks:
        print(f"  {nb.relative_to(root)}")

    print("\nExecuting notebooks end-to-end:")
    merged = merge_notebooks(notebooks)

    import nbformat

    with open(output_path, "w", encoding="utf-8") as f:
        nbformat.write(merged, f)

    print(f"\nSaved -> {output_path.relative_to(root)}")
    print(f"Total cells: {len(merged['cells'])}")

    print("\nExporting PDF...")
    export_pdf(merged, output_path)


if __name__ == "__main__":
    main()
