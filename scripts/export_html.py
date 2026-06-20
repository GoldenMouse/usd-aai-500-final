"""
CREATED by Claude
Export a report notebook to a single self-contained HTML file.

Renders a .ipynb to HTML with nbconvert's HTMLExporter using the "lab" template
(matching artifacts/Final-Project-Report-Team-3.html) and embeds all figures as
base64 directly in the file, so the result is one portable HTML with no sidecar
image folder. The notebook's cell outputs are used as-is -- nbconvert does NOT
re-run the kernel -- so the input notebook must already contain its outputs
(i.e. be an executed copy); an output-stripped source notebook will render with
no figures.

This is the HTML counterpart to scripts/export_pdf.py. A typical flow is:
    notebook (executed)  ->  export_html.py  ->  .html  ->  export_pdf.py  ->  .pdf

Usage:
    python scripts/export_html.py                          # src/master.ipynb -> deliverable HTML
    python scripts/export_html.py --input artifacts/Final-Project-Report-Team-3.ipynb
    python scripts/export_html.py --output artifacts/report.html
    python scripts/export_html.py --template classic       # classic instead of lab
    python scripts/export_html.py --no-embed               # link images instead of inlining

Requirements (already in this project): nbconvert, nbformat.
"""

import argparse
import sys
from pathlib import Path


def get_project_root() -> Path:
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / ".git").exists() or (current / "pyproject.toml").exists():
            return current
        current = current.parent
    raise RuntimeError("Could not locate project root (no .git or pyproject.toml found)")


# Defaults: the source report notebook and its published HTML deliverable name.
DEFAULT_INPUT = Path("src") / "master.ipynb"
DEFAULT_OUTPUT = Path("artifacts") / "Final-Project-Report-Team-3.html"


def notebook_to_html(
    nb_path: Path, html_path: Path, template: str = "lab", embed: bool = True
) -> int:
    """Convert a notebook to a single HTML file. Returns the number of embedded images."""
    import warnings

    import nbformat
    from nbconvert import HTMLExporter
    from nbformat.warnings import DuplicateCellId, MissingIDFieldWarning

    with open(nb_path, encoding="utf-8") as f:
        # Merged/concatenated notebooks can carry colliding cell ids; nbformat
        # silently repairs them on read, so we suppress the (harmless) per-cell
        # warnings to keep the console output clean.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DuplicateCellId)
            warnings.simplefilter("ignore", MissingIDFieldWarning)
            nb = nbformat.read(f, as_version=4)

    # embed_images=True inlines every figure as base64 -> one self-contained file.
    exporter = HTMLExporter(template_name=template, embed_images=embed)
    body, _ = exporter.from_notebook_node(nb)

    html_path.write_text(body, encoding="utf-8")
    return body.count("data:image/png;base64,")


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Export a report notebook to a self-contained HTML file."
    )
    ap.add_argument(
        "--input",
        type=Path,
        default=None,
        help="input notebook (.ipynb). Defaults to src/master.ipynb.",
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=None,
        help="output HTML path. Defaults to the published deliverable name "
        "(when --input is the default) or the input's name with a .html suffix.",
    )
    ap.add_argument(
        "--template",
        default="lab",
        help="nbconvert HTML template (e.g. lab, classic). Default: lab.",
    )
    ap.add_argument(
        "--no-embed",
        dest="embed",
        action="store_false",
        help="link images as separate files instead of inlining them as base64.",
    )
    args = ap.parse_args()

    root = get_project_root()

    if args.input is not None:
        in_path = args.input if args.input.is_absolute() else root / args.input
    else:
        in_path = root / DEFAULT_INPUT

    if not in_path.exists():
        print(f"ERROR: input not found: {in_path}", file=sys.stderr)
        return 1
    if in_path.suffix != ".ipynb":
        print(f"ERROR: input must be a .ipynb notebook, got: {in_path}", file=sys.stderr)
        return 1

    if args.output is not None:
        out_path = args.output if args.output.is_absolute() else root / args.output
    elif args.input is None:
        # Default input -> publish under the deliverable name.
        out_path = root / DEFAULT_OUTPUT
    else:
        out_path = in_path.with_suffix(".html")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Template: {args.template}  |  embed images: {args.embed}")
    print(f"Input:    {in_path.relative_to(root)}")

    n_images = notebook_to_html(in_path, out_path, template=args.template, embed=args.embed)

    size_kb = out_path.stat().st_size / 1024
    print(f"Saved -> {out_path.relative_to(root)}  ({size_kb:,.0f} KB, {n_images} embedded image(s))")
    if args.embed and n_images == 0:
        print(
            "  NOTE: 0 figures embedded -- the input notebook has no saved outputs. "
            "Execute it first (e.g. Run All) so figures are captured.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
