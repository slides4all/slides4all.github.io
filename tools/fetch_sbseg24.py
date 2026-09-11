#!/usr/bin/env python3
"""Espelha os exemplos da galeria do SBSeg 2024.

Le https://sbseg24.github.io/slides/, extrai cada entrada com os seus links,
baixa os arquivos hospedados naquele dominio para assets/slides/ e gera as
miniaturas. Links externos (Google Drive, Canva, GitHub) sao preservados como
formato adicional, sem download.

Saida: tools/sbseg24_entries.json, consumido na montagem de content/gallery.json.
"""
import html
import json
import os
import re
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLIDES = os.path.join(ROOT, "assets", "slides")
THUMBS = os.path.join(ROOT, "assets", "thumbs")
ORIGEM = "https://sbseg24.github.io/slides/"
FILES = "https://sbseg24.github.io/slides/files/"

# Entradas da galeria de origem que sao template, nao exemplo.
TEMPLATES = {"SBSeg 2024 - Slides - Template (v1)", "SBSeg2024_Slides_Template_v1",
             "Template_LaTeX_IFSCyan", "Template_LaTeX_IFSClean"}


def baixar(url, destino, tentativas=3):
    for n in range(tentativas):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                dados = r.read()
            if len(dados) < 1024:
                raise IOError("resposta muito pequena (%d bytes)" % len(dados))
            with open(destino, "wb") as fh:
                fh.write(dados)
            return len(dados)
        except Exception as e:
            if n == tentativas - 1:
                raise
            print("   repetindo %s (%s)" % (url.split("/")[-1], e), file=sys.stderr)
    return 0


def parse_pagina(bruto):
    """Extrai [(titulo, [(rotulo, url)])] da pagina de origem."""
    corpo = re.sub(r"<script.*?</script>|<style.*?</style>|<head.*?</head>", "",
                   bruto, flags=re.S)
    corpo = corpo.split("Contributors")[0]
    pedacos = re.split(r"<h[2-5][^>]*>(.*?)</h[2-5]>", corpo, flags=re.S)
    entradas = []
    for i in range(1, len(pedacos) - 1, 2):
        titulo = html.unescape(re.sub("<[^>]+>", "", pedacos[i])).strip()
        if not titulo or "Slides Examples" in titulo:
            continue
        links = []
        for m in re.finditer(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>', pedacos[i + 1], re.S):
            rotulo = html.unescape(re.sub("<[^>]+>", "", m.group(2))).strip()
            if rotulo:
                links.append((rotulo, m.group(1)))
        if links:
            entradas.append((titulo, links))
    return entradas


def slugificar(titulo):
    s = titulo.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def miniatura(pdf, slug):
    destino = os.path.join(THUMBS, slug)
    subprocess.run(["pdftoppm", "-png", "-f", "1", "-l", "1",
                    "-scale-to-x", "640", "-scale-to-y", "-1",
                    pdf, destino], check=True)
    for sufixo in ("-1.png", "-01.png"):
        if os.path.exists(destino + sufixo):
            os.replace(destino + sufixo, os.path.join(THUMBS, slug + ".png"))
            return True
    return False


def paginas(pdf):
    out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
    m = re.search(r"Pages:\s+(\d+)", out)
    return int(m.group(1)) if m else None


def main():
    os.makedirs(SLIDES, exist_ok=True)
    os.makedirs(THUMBS, exist_ok=True)
    with urllib.request.urlopen(ORIGEM, timeout=60) as r:
        bruto = r.read().decode("utf-8", "replace")
    entradas = parse_pagina(bruto)
    print("%d entradas na galeria de origem" % len(entradas))

    saida = []
    for titulo, links in entradas:
        slug = slugificar(titulo)
        registro = {"slug": slug, "titulo_origem": titulo,
                    "template": titulo in TEMPLATES, "formatos": []}
        for rotulo, url in links:
            if url.startswith(FILES):
                nome = url.rsplit("/", 1)[-1]
                ext = nome.rsplit(".", 1)[-1].lower()
                local = os.path.join(SLIDES, "%s.%s" % (slug, ext))
                if not os.path.exists(local):
                    n = baixar(url, local)
                    print("   %-46s %6.1f MB" % (os.path.basename(local), n / 1e6))
                registro["formatos"].append({"tipo": ext, "url": "assets/slides/%s.%s" % (slug, ext)})
                if ext == "pdf":
                    registro["slides"] = paginas(local)
                    if not os.path.exists(os.path.join(THUMBS, slug + ".png")):
                        miniatura(local, slug)
            else:
                registro["formatos"].append({"tipo": "externo", "rotulo": rotulo, "url": url})
        saida.append(registro)

    destino = os.path.join(ROOT, "tools", "sbseg24_entries.json")
    with open(destino, "w", encoding="utf-8") as fh:
        json.dump(saida, fh, ensure_ascii=False, indent=2)
    exemplos = [e for e in saida if not e["template"]]
    print("\n%d entradas (%d exemplos, %d templates) em tools/sbseg24_entries.json"
          % (len(saida), len(exemplos), len(saida) - len(exemplos)))


if __name__ == "__main__":
    main()
