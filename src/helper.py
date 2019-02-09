import subprocess
import os


def to_pdf(filename, latex_str, path):
    tex_path = os.path.join(path, filename + ".tex")
    with open(tex_path, 'w') as f:
        f.write(latex_str)
    proc = subprocess.Popen(['pdflatex', "-output-directory", path, tex_path])
    proc.communicate()


def save_as_png(filename, latex_str, path):
    raise RuntimeError("Ne lez ono teba sozhret")
    pdf_name = filename + ".pdf"
    to_pdf(filename, latex_str, path)
    proc = subprocess.Popen(['pdftoppm', os.path.join(path, pdf_name), os.path.join(path, filename), '-png'])
    proc.communicate()
