#!/usr/bin/env python3
"""Verifica o site gerado antes de considerar a versao pronta.

Confere, em todas as paginas de pt/, en/, es/ e na raiz:
  - todo link interno resolve para um arquivo existente;
  - todo recurso referenciado (css, js, imagem) existe;
  - toda imagem tem atributo alt;
  - nenhum marcador de template sobrou sem substituir;
  - nenhum texto contem travessao;
  - as paginas equivalentes nos tres idiomas tem o mesmo numero de secoes;
  - nenhum arquivo passa de 100 MB, limite rigido do GitHub.
"""
import os
import re
import sys
from urllib.parse import urldefrag, urlparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from build import IDIOMAS, SLUGS, caminho_pagina  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
problemas = []


def resolver(pagina, destino):
    destino = urldefrag(destino)[0]
    if not destino:
        return None
    alvo = os.path.normpath(os.path.join(os.path.dirname(pagina), destino))
    if os.path.isdir(alvo):
        alvo = os.path.join(alvo, "index.html")
    return alvo


def conferir_pagina(caminho):
    rel = os.path.relpath(caminho, ROOT)
    texto = open(caminho, encoding="utf-8").read()

    for ref in re.findall(r'(?:href|src)="([^"]+)"', texto):
        if urlparse(ref).scheme or ref.startswith(("//", "#", "mailto:")):
            continue
        alvo = resolver(caminho, ref)
        if alvo and not os.path.exists(alvo):
            problemas.append("%s: link quebrado %s" % (rel, ref))

    for tag in re.findall(r"<img\b[^>]*>", texto):
        if 'alt="' not in tag:
            problemas.append("%s: imagem sem alt: %s" % (rel, tag[:70]))

    if "{{" in texto:
        problemas.append("%s: marcador de template nao substituido" % rel)
    if "—" in texto:
        problemas.append("%s: contem travessao" % rel)

    return len(re.findall(r"<h2[ >]", texto))


def main():
    secoes = {}
    total = 0

    for chave in SLUGS:
        for idioma in IDIOMAS:
            caminho = os.path.join(ROOT, caminho_pagina(idioma, chave), "index.html")
            if not os.path.exists(caminho):
                problemas.append("pagina ausente: %s" % os.path.relpath(caminho, ROOT))
                continue
            secoes.setdefault(chave, {})[idioma] = conferir_pagina(caminho)
            total += 1

    raiz = os.path.join(ROOT, "index.html")
    if os.path.exists(raiz):
        conferir_pagina(raiz)
        total += 1
    else:
        problemas.append("index.html da raiz nao foi gerado")

    for chave, por_idioma in sorted(secoes.items()):
        if len(set(por_idioma.values())) != 1:
            problemas.append("pagina %s tem numero de secoes diferente entre idiomas: %s"
                             % (chave, por_idioma))

    for base, dirs, arquivos in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d != ".git"]
        for a in arquivos:
            p = os.path.join(base, a)
            if os.path.getsize(p) > 100 * 1024 * 1024:
                problemas.append("arquivo acima de 100 MB: %s" % os.path.relpath(p, ROOT))

    print("%d paginas verificadas" % total)
    if problemas:
        for p in problemas:
            print("PROBLEMA  %s" % p, file=sys.stderr)
        raise SystemExit("%d problema(s)" % len(problemas))
    print("links, recursos, alt de imagens, paridade de secoes e tamanhos: tudo certo")


if __name__ == "__main__":
    main()
