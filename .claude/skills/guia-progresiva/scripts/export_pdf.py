"""Export GUIA.md to GUIA.pdf using whichever method is available.

Order of preference:
1. pandoc (best output, requires install)
2. Python markdown + weasyprint (pure Python if libs installed)
3. Python markdown + xhtml2pdf (lighter Python fallback)
4. Generate styled GUIA.html and instruct user to print-to-PDF from browser

Run from project root:
    python .claude/skills/guia-progresiva/scripts/export_pdf.py
"""

import shutil
import subprocess
import sys
from pathlib import Path


def find_project_root() -> Path:
    """Walk up from CWD looking for GUIA.md."""
    cwd = Path.cwd().resolve()
    for candidate in [cwd, *cwd.parents]:
        if (candidate / "GUIA.md").exists():
            return candidate
    print("ERROR: No se encontró GUIA.md en el directorio actual ni en padres.")
    sys.exit(1)


HTML_WRAPPER = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
  @page {{ size: A4; margin: 2cm 1.8cm; }}
  body {{
    font-family: -apple-system, "Segoe UI", Roboto, sans-serif;
    line-height: 1.55;
    color: #1a1a1a;
    max-width: 760px;
    margin: 0 auto;
  }}
  h1 {{ font-size: 28px; border-bottom: 2px solid #222; padding-bottom: 8px; }}
  h2 {{ font-size: 20px; margin-top: 32px; color: #222; border-bottom: 1px solid #ddd; padding-bottom: 4px; }}
  h3 {{ font-size: 15px; margin-top: 22px; color: #333; }}
  p, li {{ font-size: 12.5px; }}
  code {{ background: #f4f4f4; padding: 1px 5px; border-radius: 3px; font-size: 12px; }}
  pre {{ background: #f4f4f4; padding: 10px 12px; border-radius: 4px; overflow-x: auto; font-size: 11.5px; }}
  blockquote {{ border-left: 3px solid #888; padding-left: 12px; color: #555; margin: 12px 0; }}
  strong {{ color: #000; }}
  hr {{ border: none; border-top: 1px solid #ccc; margin: 24px 0; }}
  @media print {{ body {{ max-width: 100%; }} }}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def try_pandoc(md: Path, pdf: Path) -> bool:
    if not shutil.which("pandoc"):
        return False
    try:
        subprocess.run(
            ["pandoc", str(md), "-o", str(pdf), "--pdf-engine=wkhtmltopdf"],
            check=True, capture_output=True, text=True,
        )
        return pdf.exists()
    except subprocess.CalledProcessError:
        try:
            subprocess.run(
                ["pandoc", str(md), "-o", str(pdf)],
                check=True, capture_output=True, text=True,
            )
            return pdf.exists()
        except subprocess.CalledProcessError as e:
            print(f"pandoc disponible pero falló: {e.stderr[:200]}")
            return False


def try_weasyprint(md: Path, pdf: Path) -> bool:
    try:
        import markdown
        from weasyprint import HTML
    except ImportError:
        return False
    body = markdown.markdown(md.read_text(encoding="utf-8"), extensions=["fenced_code", "tables"])
    html = HTML_WRAPPER.format(title=md.stem, body=body)
    HTML(string=html).write_pdf(str(pdf))
    return pdf.exists()


def try_xhtml2pdf(md: Path, pdf: Path) -> bool:
    try:
        import markdown
        from xhtml2pdf import pisa
    except ImportError:
        return False
    body = markdown.markdown(md.read_text(encoding="utf-8"), extensions=["fenced_code", "tables"])
    html = HTML_WRAPPER.format(title=md.stem, body=body)
    with open(pdf, "wb") as f:
        result = pisa.CreatePDF(html, dest=f)
    return not result.err and pdf.exists()


def fallback_html(md: Path, html_path: Path) -> bool:
    try:
        import markdown
        body = markdown.markdown(md.read_text(encoding="utf-8"), extensions=["fenced_code", "tables"])
    except ImportError:
        body = "<pre>" + md.read_text(encoding="utf-8").replace("<", "&lt;") + "</pre>"
    html_path.write_text(HTML_WRAPPER.format(title=md.stem, body=body), encoding="utf-8")
    return html_path.exists()


def main() -> None:
    root = find_project_root()
    md = root / "GUIA.md"
    pdf = root / "GUIA.pdf"

    print(f"Origen: {md}")
    print(f"Destino: {pdf}\n")

    methods = [
        ("pandoc", try_pandoc),
        ("weasyprint", try_weasyprint),
        ("xhtml2pdf", try_xhtml2pdf),
    ]

    for name, func in methods:
        print(f"Intentando {name}...")
        if func(md, pdf):
            print(f"\nOK — PDF generado con {name}: {pdf}")
            return
        print(f"  {name} no disponible o falló.")

    html_path = root / "GUIA.html"
    print("\nNingún método de PDF directo funcionó. Generando HTML como fallback.")
    if fallback_html(md, html_path):
        print(f"\nOK — HTML generado: {html_path}")
        print("Abrilo en el navegador y usá Imprimir → Guardar como PDF.")
        print("\nPara generar PDF directo en futuros proyectos, instalá una de estas opciones:")
        print("  - pandoc:        winget install JohnMacFarlane.Pandoc")
        print("  - weasyprint:    pip install markdown weasyprint")
        print("  - xhtml2pdf:     pip install markdown xhtml2pdf")
    else:
        print("ERROR: ni siquiera el HTML fallback funcionó.")
        sys.exit(1)


if __name__ == "__main__":
    main()
