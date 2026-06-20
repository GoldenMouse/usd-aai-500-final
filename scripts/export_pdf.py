"""
CREATED by Claude
Export the final report to PDF.

Two methods are supported; the default is the higher-fidelity one:

1. HTML -> PDF  (default, recommended)
   Renders the already-built, fully-styled report HTML through headless
   Chromium's own print engine (via Playwright) and prints it to PDF. Because
   it prints the same HTML/CSS/MathJax you see in a browser, the PDF matches
   the reviewed HTML exactly -- embedded figures, colored tables, and typeset
   LaTeX equations all render faithfully, with real page breaks and margins.
   It does NOT re-execute the notebook, so there is no rendering drift.

2. notebook -> PDF  (--from-notebook)
   Falls back to nbconvert's WebPDFExporter (the same path scripts/merge_notebooks.py
   uses). Renders a .ipynb straight to PDF. Use this when you only have the
   notebook, not a built HTML.

Usage:
    python scripts/export_pdf.py                       # HTML artifact -> PDF (default)
    python scripts/export_pdf.py --input path/to.html  # a specific HTML file
    python scripts/export_pdf.py --from-notebook        # merged report notebook -> PDF
    python scripts/export_pdf.py --from-notebook --input src/master.ipynb
    python scripts/export_pdf.py --paper Letter --output artifacts/report.pdf

Requirements (already in this project): playwright + its Chromium build, and
nbconvert for the --from-notebook path. If Chromium is missing, run:
    python -m playwright install chromium
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


# Default artifact locations.
DEFAULT_HTML = Path("artifacts") / "Final-Project-Report-Team-3.html"
DEFAULT_NOTEBOOK = Path("artifacts") / "Final-Project-Report-Team-3.ipynb"

# Page margins (inches) used for both methods.
MARGIN = {"top": "0.6in", "bottom": "0.6in", "left": "0.5in", "right": "0.5in"}


def html_to_pdf(html_path: Path, pdf_path: Path, paper: str = "A4") -> None:
    """Print a local HTML file to PDF with headless Chromium (Playwright)."""
    from playwright.sync_api import sync_playwright

    file_url = html_path.resolve().as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        # networkidle lets remote assets (e.g. the MathJax CDN that typesets the
        # LaTeX equations) finish loading before we print.
        page.goto(file_url, wait_until="networkidle", timeout=120_000)

        # If MathJax is present, wait for it to finish typesetting so equations
        # are rendered glyphs in the PDF, not raw "$...$" source.
        try:
            page.wait_for_function(
                "() => !window.MathJax || (window.MathJax.startup "
                "&& window.MathJax.startup.document "
                "&& window.MathJax.startup.document.state() >= 10)",
                timeout=30_000,
            )
        except Exception:
            page.wait_for_timeout(2_000)  # best-effort fallback

        # Use the page's print stylesheet, and keep background colors (the
        # role-colored summary table, header bands, etc.).
        page.emulate_media(media="print")
        page.pdf(
            path=str(pdf_path),
            format=paper,
            print_background=True,
            margin=MARGIN,
            prefer_css_page_size=True,
        )
        browser.close()


def notebook_to_pdf(nb_path: Path, pdf_path: Path) -> None:
    """Render a notebook directly to PDF via nbconvert's WebPDFExporter."""
    import asyncio

    # Windows Store Python defaults to SelectorEventLoop, which cannot spawn the
    # subprocess Playwright needs; WebPDFExporter requires ProactorEventLoop.
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    import nbformat
    from nbconvert import WebPDFExporter

    with open(nb_path, encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    exporter = WebPDFExporter()
    pdf_data, _ = exporter.from_notebook_node(nb)
    pdf_path.write_bytes(pdf_data)


def main() -> int:
    ap = argparse.ArgumentParser(description="Export the final report to PDF.")
    ap.add_argument(
        "--from-notebook",
        action="store_true",
        help="convert a notebook (.ipynb) to PDF instead of the HTML (lower fidelity).",
    )
    ap.add_argument(
        "--input",
        type=Path,
        default=None,
        help="input file. Defaults to the report HTML (or notebook with --from-notebook).",
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=None,
        help="output PDF path. Defaults to the input's name with a .pdf suffix.",
    )
    ap.add_argument(
        "--paper",
        default="A4",
        help="paper size for the HTML method (e.g. A4, Letter). Ignored for --from-notebook.",
    )
    args = ap.parse_args()

    root = get_project_root()

    if args.input is not None:
        in_path = args.input if args.input.is_absolute() else root / args.input
    else:
        in_path = root / (DEFAULT_NOTEBOOK if args.from_notebook else DEFAULT_HTML)

    if not in_path.exists():
        print(f"ERROR: input not found: {in_path}", file=sys.stderr)
        return 1

    out_path = (
        (args.output if args.output.is_absolute() else root / args.output)
        if args.output is not None
        else in_path.with_suffix(".pdf")
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)

    method = "notebook -> PDF (nbconvert)" if args.from_notebook else "HTML -> PDF (Chromium)"
    print(f"Method: {method}")
    print(f"Input:  {in_path.relative_to(root)}")

    if args.from_notebook:
        notebook_to_pdf(in_path, out_path)
    else:
        html_to_pdf(in_path, out_path, paper=args.paper)

    size_kb = out_path.stat().st_size / 1024
    print(f"Saved -> {out_path.relative_to(root)}  ({size_kb:,.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
