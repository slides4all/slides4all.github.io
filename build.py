#!/usr/bin/env python3
"""Gera o site estatico a partir de content/*.json.

  python3 build.py

Escreve pt/, en/, es/ e index.html na raiz do repositorio. O conteudo vem de
content/<idioma>.json, o catalogo de content/gallery.json e o checklist de
content/checklist.json.

O gerador falha, em vez de produzir um site quebrado, quando:
  - uma pagina, um bloco ou uma chave existe em um idioma e falta em outro;
  - um bloco tem tipo diferente entre idiomas na mesma posicao;
  - uma entrada da galeria aponta para arquivo inexistente;
  - um item do checklist nao tem traducao nos tres idiomas.
"""
import html
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content")
IDIOMAS = ["pt", "en", "es"]
PADRAO = "pt"

# chave da pagina -> slug por idioma. Slug vazio significa a raiz do idioma.
SLUGS = {
    "home": {"pt": "", "en": "", "es": ""},
    "slides": {"pt": "slides", "en": "slides", "es": "slides"},
    "presenting": {"pt": "apresentar", "en": "presenting", "es": "presentar"},
    "mistakes": {"pt": "erros", "en": "mistakes", "es": "errores"},
    "checklist": {"pt": "checklist", "en": "checklist", "es": "checklist"},
    "timing": {"pt": "tempo", "en": "timing", "es": "tiempo"},
    "gallery": {"pt": "galeria", "en": "gallery", "es": "galeria"},
    "templates": {"pt": "templates", "en": "templates", "es": "plantillas"},
    "credits": {"pt": "creditos", "en": "credits", "es": "creditos"},
}
ORDEM_NAV = ["slides", "presenting", "mistakes", "checklist", "timing",
             "gallery", "templates"]
NOMES_IDIOMA = {"pt": "Português", "en": "English", "es": "Español"}

# Listas que podem ter tamanho diferente entre idiomas sem que isso seja erro.
LISTAS_LIVRES = {"paragraphs"}

erros = []
avisos = []


def e(txt):
    return html.escape(str(txt), quote=True)


# --------------------------------------------------------------------------
# Validacao entre idiomas
# --------------------------------------------------------------------------

def comparar(a, b, caminho, ia, ib):
    """Compara a estrutura de dois valores vindos de idiomas diferentes."""
    if isinstance(a, dict):
        if not isinstance(b, dict):
            erros.append("%s: e objeto em %s e %s em %s" % (caminho, ia, type(b).__name__, ib))
            return
        for k in a:
            if k not in b:
                erros.append("%s.%s existe em %s e falta em %s" % (caminho, k, ia, ib))
            else:
                comparar(a[k], b[k], "%s.%s" % (caminho, k), ia, ib)
        for k in b:
            if k not in a:
                erros.append("%s.%s existe em %s e falta em %s" % (caminho, k, ib, ia))
    elif isinstance(a, list):
        if not isinstance(b, list):
            erros.append("%s: e lista em %s e %s em %s" % (caminho, ia, type(b).__name__, ib))
            return
        chave = caminho.rsplit(".", 1)[-1]
        if len(a) != len(b):
            if chave in LISTAS_LIVRES:
                avisos.append("%s tem %d itens em %s e %d em %s"
                              % (caminho, len(a), ia, len(b), ib))
                return
            erros.append("%s tem %d itens em %s e %d em %s"
                         % (caminho, len(a), ia, len(b), ib))
            return
        for i, (x, y) in enumerate(zip(a, b)):
            comparar(x, y, "%s[%d]" % (caminho, i), ia, ib)


def validar(conteudo):
    base = conteudo[PADRAO]
    for idioma in IDIOMAS:
        if idioma == PADRAO:
            continue
        comparar(base, conteudo[idioma], "raiz", PADRAO, idioma)
    for chave in SLUGS:
        for idioma in IDIOMAS:
            if chave not in conteudo[idioma]["pages"]:
                erros.append("pagina %s nao existe em %s" % (chave, idioma))


def validar_checklist(grupos):
    for g in grupos:
        for idioma in IDIOMAS:
            if idioma not in g["title"]:
                erros.append("checklist: grupo %s sem titulo em %s" % (g["id"], idioma))
        for it in g["items"]:
            for idioma in IDIOMAS:
                if not it.get(idioma):
                    erros.append("checklist: item %s sem texto em %s" % (it["id"], idioma))


def validar_galeria(entradas):
    vistos = set()
    for ent in entradas:
        if ent["slug"] in vistos:
            erros.append("galeria: slug repetido %s" % ent["slug"])
        vistos.add(ent["slug"])
        if not os.path.exists(os.path.join(ROOT, ent["thumb"])):
            erros.append("galeria: miniatura ausente %s" % ent["thumb"])
        if not ent["files"]:
            erros.append("galeria: %s sem nenhum formato" % ent["slug"])
        for f in ent["files"]:
            if f["type"] != "external" and not os.path.exists(os.path.join(ROOT, f["url"])):
                erros.append("galeria: arquivo ausente %s" % f["url"])


# --------------------------------------------------------------------------
# Caminhos
# --------------------------------------------------------------------------

def caminho_pagina(idioma, chave):
    slug = SLUGS[chave][idioma]
    return "%s/" % idioma if not slug else "%s/%s/" % (idioma, slug)


def url_relativa(origem_chave, idioma, destino_chave):
    """Link entre paginas do mesmo idioma, relativo a pagina de origem."""
    origem = SLUGS[origem_chave][idioma]
    destino = SLUGS[destino_chave][idioma]
    subir = "" if not origem else "../"
    if destino:
        return subir + destino + "/"
    return subir if subir else "./"


def prefixo_raiz(idioma, chave):
    return "../" * (1 if not SLUGS[chave][idioma] else 2)


# --------------------------------------------------------------------------
# Blocos de conteudo
# --------------------------------------------------------------------------

def render_lead(b, ctx):
    return '<p class="lead">%s</p>' % e(b["text"])


def render_prose(b, ctx):
    saida = []
    if b.get("heading"):
        saida.append("<h2>%s</h2>" % e(b["heading"]))
    for p in b.get("paragraphs", []):
        saida.append("<p>%s</p>" % e(p))
    return "\n".join(saida)


def render_note(b, ctx):
    return '<aside class="note"><p>%s</p></aside>' % e(b["text"])


def render_section(b, ctx):
    saida = ["<section class=\"block\">"]
    if b.get("heading"):
        saida.append("<h2>%s</h2>" % e(b["heading"]))
    if b.get("intro"):
        saida.append('<p class="intro">%s</p>' % e(b["intro"]))
    if b.get("items"):
        saida.append("<ul class=\"rules\">")
        for it in b["items"]:
            saida.append("<li>%s</li>" % e(it))
        saida.append("</ul>")
    if b.get("linkPage"):
        saida.append('<p class="block-link"><a href="%s">%s</a></p>'
                     % (url_relativa(ctx["chave"], ctx["idioma"], b["linkPage"]),
                        e(b["linkLabel"])))
    saida.append("</section>")
    return "\n".join(saida)


def render_callout(b, ctx):
    saida = ['<section class="callout">']
    saida.append("<h2>%s</h2>" % e(b["heading"]))
    if b.get("text"):
        saida.append("<p>%s</p>" % e(b["text"]))
    saida.append('<ul class="split">')
    for it in b.get("items", []):
        saida.append("<li>%s</li>" % e(it))
    saida.append("</ul>")
    if b.get("linkPage"):
        saida.append('<p class="block-link"><a href="%s">%s</a></p>'
                     % (url_relativa(ctx["chave"], ctx["idioma"], b["linkPage"]),
                        e(b["linkLabel"])))
    saida.append("</section>")
    return "\n".join(saida)


def render_links(b, ctx):
    saida = ['<section class="block">']
    if b.get("heading"):
        saida.append("<h2>%s</h2>" % e(b["heading"]))
    saida.append('<ul class="links">')
    for it in b["items"]:
        saida.append('<li><a href="%s" rel="noopener">%s</a></li>'
                     % (e(it["url"]), e(it["label"])))
    saida.append("</ul></section>")
    return "\n".join(saida)


def render_people(b, ctx):
    saida = ['<section class="block">', "<h2>%s</h2>" % e(b["heading"])]
    if b.get("text"):
        saida.append('<p class="intro">%s</p>' % e(b["text"]))
    saida.append('<ul class="people">')
    for it in b["items"]:
        saida.append("<li>%s</li>" % e(it))
    saida.append("</ul></section>")
    return "\n".join(saida)


def render_cards(b, ctx):
    saida = ['<div class="cards">']
    for c in b["items"]:
        saida.append('<a class="card" href="%s">'
                     '<span class="card-kicker">%s</span>'
                     '<span class="card-title">%s</span>'
                     '<span class="card-text">%s</span></a>'
                     % (url_relativa(ctx["chave"], ctx["idioma"], c["page"]),
                        e(c["kicker"]), e(c["title"]), e(c["text"])))
    saida.append("</div>")
    return "\n".join(saida)


def render_example(b, ctx):
    return ("\n".join([
        '<section class="block">',
        "<h2>%s</h2>" % e(b["heading"]),
        '<p class="intro">%s</p>' % e(b["intro"]),
        '<div class="swap">',
        '<div class="swap-side swap-before"><span class="swap-label">%s</span>'
        '<p class="swap-text">%s</p></div>' % (e(b["before"]["label"]), e(b["before"]["text"])),
        '<div class="swap-side swap-after"><span class="swap-label">%s</span>'
        '<p class="swap-text">%s</p></div>' % (e(b["after"]["label"]), e(b["after"]["text"])),
        "</div></section>"]))


BLOCOS = {"lead": render_lead, "prose": render_prose, "note": render_note,
          "section": render_section, "callout": render_callout,
          "links": render_links, "people": render_people, "cards": render_cards,
          "example": render_example}


def render_blocos(blocos, ctx):
    saida = []
    for b in blocos:
        fn = BLOCOS.get(b["type"])
        if not fn:
            erros.append("bloco de tipo desconhecido: %s" % b["type"])
            continue
        saida.append(fn(b, ctx))
    return "\n".join(saida)


# --------------------------------------------------------------------------
# Mini-slides da pagina de erros
# --------------------------------------------------------------------------

def mini_slide(d):
    kind = d["kind"]
    cls = "mini mini-%s" % d.get("variant", "")
    corpo = []
    if d.get("title"):
        corpo.append('<div class="mini-title">%s</div>' % e(d["title"]))

    if kind == "bullets":
        corpo.append("<ul>%s</ul>" % "".join("<li>%s</li>" % e(i) for i in d["items"]))
    elif kind == "chart-text":
        corpo.append('<div class="mini-split">%s<ul class="mini-side">%s</ul></div>'
                     % (grafico(), "".join("<li>%s</li>" % e(i) for i in d["items"])))
    elif kind == "chart-only":
        corpo.append('<div class="mini-chart-full">%s</div>' % grafico())
    elif kind == "figure":
        corpo.append('<div class="mini-figure">%s</div>' % diagrama())
    elif kind == "steps":
        ativo = d.get("active")
        blocos = []
        for i, s in enumerate(d["steps"], 1):
            estado = "on" if (ativo is None or i <= ativo) else "off"
            blocos.append('<span class="mini-step %s">%s</span>' % (estado, e(s)))
        corpo.append('<div class="mini-steps">%s</div>' % "".join(blocos))
    elif kind == "boxes":
        blocos = []
        for bx in d["boxes"]:
            if "n" in bx:
                blocos.append('<div class="mini-box"><span class="mini-num">%s</span>'
                              '<span class="mini-box-text">%s</span></div>'
                              % (e(bx["n"]), e(bx["text"])))
            else:
                blocos.append('<div class="mini-box"><span class="mini-key">%s</span>'
                              '<span class="mini-box-text">%s</span></div>'
                              % (e(bx["key"]), e(bx["text"])))
        corpo.append('<div class="mini-boxes">%s</div>' % "".join(blocos))
    elif kind == "box-text":
        corpo.append('<div class="mini-textbox"><p>%s</p></div>' % e(d["text"]))
    elif kind == "table":
        cab = "".join("<th>%s</th>" % e(h) for h in d["head"])
        linhas = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % e(c) for c in r)
                         for r in d["rows"])
        corpo.append("<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>"
                     % (cab, linhas))
    elif kind == "title-logos":
        corpo = ['<div class="mini-cover"><span class="mini-cover-title">%s</span>'
                 '<span class="mini-cover-authors">%s</span>'
                 '<span class="mini-logos"><i></i><i></i><i></i></span></div>'
                 % (e(d["title"]), e(d["authors"]))]
    else:
        erros.append("mini-slide de tipo desconhecido: %s" % kind)
    return '<div class="%s" aria-hidden="true">%s</div>' % (cls.strip(), "".join(corpo))


def grafico():
    pontos_base = "0,62 40,55 80,50 120,47 160,45 200,44"
    pontos_prop = "0,52 40,38 80,28 120,20 160,14 200,10"
    return ('<svg class="mini-svg" viewBox="0 0 210 70" role="img" focusable="false">'
            '<polyline points="5,5 5,65 205,65" fill="none" stroke="currentColor" stroke-width="1.2"/>'
            '<polyline points="%s" fill="none" stroke="currentColor" stroke-width="2" opacity="0.45"/>'
            '<polyline points="%s" fill="none" stroke="currentColor" stroke-width="2.6"/>'
            "</svg>" % (pontos_base, pontos_prop))


def diagrama():
    return ('<svg class="mini-svg" viewBox="0 0 200 90" role="img" focusable="false">'
            '<rect x="6" y="30" width="46" height="30" fill="none" stroke="currentColor" stroke-width="1.6"/>'
            '<rect x="77" y="30" width="46" height="30" fill="none" stroke="currentColor" stroke-width="1.6"/>'
            '<rect x="148" y="30" width="46" height="30" fill="none" stroke="currentColor" stroke-width="1.6"/>'
            '<line x1="52" y1="45" x2="77" y2="45" stroke="currentColor" stroke-width="1.6"/>'
            '<line x1="123" y1="45" x2="148" y2="45" stroke="currentColor" stroke-width="1.6"/>'
            "</svg>")


def render_mistakes(pagina, ctx):
    ui = ctx["texto"]["ui"]
    saida = []
    for m in pagina["mistakes"]:
        saida.append(
            '<section class="mistake" id="%s">'
            "<h2>%s</h2>"
            '<p class="mistake-why">%s</p>'
            '<div class="pair">'
            '<figure class="pair-side is-wrong"><figcaption><span class="tag tag-wrong">%s</span></figcaption>%s</figure>'
            '<figure class="pair-side is-right"><figcaption><span class="tag tag-right">%s</span></figcaption>%s</figure>'
            "</div>"
            '<p class="mistake-fix">%s</p>'
            "</section>"
            % (e(m["id"]), e(m["title"]), e(m["why"]),
               e(ui["wrong"]), mini_slide(m["wrong"]),
               e(ui["right"]), mini_slide(m["right"]),
               e(m["fix"])))
    return "\n".join(saida)


# --------------------------------------------------------------------------
# Paginas com conteudo gerado
# --------------------------------------------------------------------------

def render_checklist(pagina, ctx, grupos):
    idioma = ctx["idioma"]
    ui = pagina["ui"]
    total = sum(len(g["items"]) for g in grupos)
    saida = ['<div class="checklist" data-total="%d">' % total,
             '<div class="checklist-bar" role="status" aria-live="polite">',
             '<span class="checklist-count"><strong id="ckDone">0</strong> / %d %s</span>'
             % (total, e(ui["progress"])),
             '<span class="checklist-track"><i id="ckFill"></i></span>',
             '<span class="checklist-actions">',
             '<button type="button" id="ckCopy" class="btn" data-copied="%s">%s</button>'
             % (e(ui["copied"]), e(ui["copy"])),
             '<button type="button" id="ckReset" class="btn" data-confirm="%s">%s</button>'
             % (e(ui["resetConfirm"]), e(ui["reset"])),
             "</span></div>",
             '<p class="checklist-done" id="ckAllDone" hidden>%s</p>' % e(ui["allDone"])]
    for g in grupos:
        saida.append('<section class="ck-group"><h2>%s</h2><ul>' % e(g["title"][idioma]))
        for it in g["items"]:
            saida.append('<li><label><input type="checkbox" data-ck="%s"><span>%s</span></label></li>'
                         % (e(it["id"]), e(it[idioma])))
        saida.append("</ul></section>")
    saida.append("</div>")
    return "\n".join(saida)


def render_timing(pagina, ctx):
    ui = pagina["ui"]
    partes = [("foundation", 30), ("problem", 15), ("contribution", 45), ("closing", 10)]
    linhas = []
    for chave, pct in partes:
        linhas.append(
            '<tr><th scope="row">%s</th><td class="pct">%d%%</td>'
            '<td class="val" data-part="%s">-</td></tr>'
            % (e(ui["parts_" + chave]), pct, chave))
    return "\n".join([
        '<form class="timing" id="timingForm" autocomplete="off">',
        '<label class="timing-label" for="timingInput">%s</label>' % e(ui["label"]),
        '<input type="number" id="timingInput" min="1" max="180" step="1" value="20" inputmode="numeric">',
        '<div class="timing-quick"><span>%s</span>' % e(ui["quick"]),
        "".join('<button type="button" class="btn quick" data-min="%d">%d</button>' % (m, m)
                for m in (15, 20, 25, 30)),
        "</div></form>",
        '<section class="block"><h2>%s</h2>' % e(ui["parts"]),
        '<table class="timing-table"><tbody>%s</tbody></table></section>' % "".join(linhas),
        '<section class="block"><h2>%s</h2>' % e(ui["slidesLabel"]),
        '<p class="timing-big"><span id="timingSlides">-</span></p>',
        '<p class="intro">%s</p></section>' % e(ui["slidesHint"]),
        '<section class="block"><h2>%s</h2><ul class="rules">' % e(ui["toleranceLabel"]),
        '<li>%s <strong id="timingTol5">-</strong></li>' % e(ui["toleranceTarget"]),
        '<li>%s <strong id="timingTol10">-</strong></li>' % e(ui["toleranceLimit"]),
        "</ul></section>",
        '<div hidden id="timingStrings" data-min="%s" data-sec="%s" data-around="%s" data-oftotal="%s"></div>'
        % (e(ui["minutes"]), e(ui["seconds"]), e(ui["aroundLabel"]), e(ui["ofTotal"])),
    ])


def render_gallery(pagina, ctx, entradas):
    ui = pagina["ui"]
    trilhas = pagina["tracks"]
    eventos = pagina["events"]
    formatos = pagina["formats"]
    raiz = prefixo_raiz(ctx["idioma"], ctx["chave"])

    # Ano decrescente, com o nome do evento como criterio de desempate: sem ele a
    # ordem viria da iteracao de um set e mudaria a cada execucao do Python.
    anos = {}
    for x in entradas:
        anos[x["event"]] = max(anos.get(x["event"], 0), x["year"])
    eventos_usados = sorted(anos, key=lambda k: (-anos[k], k))
    trilhas_usadas = sorted({x["track"] for x in entradas})

    filtros = ['<div class="filters">',
               '<div class="filter"><span class="filter-label">%s</span><div class="chips">' % e(ui["filterEvent"]),
               '<button type="button" class="chip is-on" data-filter="event" data-value="">%s</button>' % e(ui["filterAll"])]
    for ev in eventos_usados:
        filtros.append('<button type="button" class="chip" data-filter="event" data-value="%s">%s</button>'
                       % (e(ev), e(eventos.get(ev, ev))))
    filtros.append("</div></div>")
    filtros.append('<div class="filter"><span class="filter-label">%s</span><div class="chips">' % e(ui["filterTrack"]))
    filtros.append('<button type="button" class="chip is-on" data-filter="track" data-value="">%s</button>' % e(ui["filterAll"]))
    for tr in trilhas_usadas:
        filtros.append('<button type="button" class="chip" data-filter="track" data-value="%s">%s</button>'
                       % (e(tr), e(trilhas.get(tr, tr))))
    filtros.append("</div></div></div>")
    filtros.append('<p class="results" id="galleryCount" role="status" aria-live="polite">'
                   '<span id="galleryShown">%d</span> %s</p>' % (len(entradas), e(ui["results"])))

    cartoes = ['<ul class="gallery" id="galleryList">']
    for x in entradas:
        arquivos = []
        for f in x["files"]:
            if f["type"] == "external":
                rotulo = f.get("label", formatos["external"])
                href = f["url"]
                extra = ' rel="noopener"'
            else:
                rotulo = formatos.get(f["type"], f["type"].upper())
                href = raiz + f["url"]
                extra = ""
            arquivos.append('<li><a class="file" href="%s"%s>%s</a></li>' % (e(href), extra, e(rotulo)))
        cartoes.append(
            '<li class="item" data-event="%s" data-track="%s">'
            '<a class="item-thumb" href="%s"><img src="%s" alt="%s %s" loading="lazy" width="640" height="360"></a>'
            '<div class="item-body">'
            '<span class="item-meta">%s &middot; %s &middot; %d %s</span>'
            "<h3>%s</h3>"
            '<p class="item-authors">%s</p>'
            '<ul class="files">%s</ul>'
            "</div></li>"
            % (e(x["event"]), e(x["track"]),
               e(raiz + x["files"][0]["url"] if x["files"][0]["type"] != "external" else x["files"][0]["url"]),
               e(raiz + x["thumb"]), e(ui["thumbAlt"]), e(x["title"]),
               e(eventos.get(x["event"], x["event"])), e(trilhas.get(x["track"], x["track"])),
               x["slides"] or 0, e(ui["slidesLabel"]),
               e(x["title"]), e(x["authors"]), "".join(arquivos)))
    cartoes.append("</ul>")
    cartoes.append('<p class="no-results" id="galleryEmpty" hidden>%s</p>' % e(ui["noResults"]))
    return "\n".join(filtros + cartoes)


def render_templates(pagina, ctx):
    raiz = prefixo_raiz(ctx["idioma"], ctx["chave"])
    formatos = ctx["texto"]["pages"]["gallery"]["formats"]
    saida = ['<ul class="gallery templates-list">']
    for t in pagina["items"]:
        arquivos = []
        for f in t["files"]:
            if f["type"] == "external":
                arquivos.append('<li><a class="file" href="%s" rel="noopener">%s</a></li>'
                                % (e(f["url"]), e(f.get("label", "Online"))))
            else:
                arquivos.append('<li><a class="file" href="%s">%s</a></li>'
                                % (e(raiz + f["url"]), e(formatos.get(f["type"], f["type"].upper()))))
        thumb = ""
        if t.get("thumb"):
            thumb = ('<div class="item-thumb"><img src="%s" alt="" loading="lazy" '
                     'width="640" height="360"></div>' % e(raiz + t["thumb"]))
        saida.append('<li class="item">%s<div class="item-body"><h3>%s</h3><p>%s</p>'
                     '<ul class="files">%s</ul></div></li>'
                     % (thumb, e(t["name"]), e(t["text"]), "".join(arquivos)))
    saida.append("</ul>")
    return "\n".join(saida)


# --------------------------------------------------------------------------
# Esqueleto da pagina
# --------------------------------------------------------------------------

def montar_pagina(idioma, chave, texto, corpo, scripts):
    raiz = prefixo_raiz(idioma, chave)
    pagina = texto["pages"][chave]
    titulo = pagina["title"]
    if chave == "home":
        titulo_completo = "%s | %s" % (texto["site"]["name"], texto["site"]["tagline"])
    else:
        titulo_completo = "%s | %s" % (titulo, texto["site"]["name"])

    nav = []
    for k in ORDEM_NAV:
        atual = ' aria-current="page"' if k == chave else ""
        nav.append('<li><a href="%s"%s>%s</a></li>'
                   % (url_relativa(chave, idioma, k), atual, e(texto["nav"][k])))

    idiomas = []
    for outro in IDIOMAS:
        alvo = "%s%s" % (raiz, caminho_pagina(outro, chave))
        atual = ' aria-current="true"' if outro == idioma else ""
        idiomas.append('<a href="%s" lang="%s"%s>%s</a>'
                       % (e(alvo), outro, atual, e(NOMES_IDIOMA[outro])))

    alternates = "\n".join(
        '  <link rel="alternate" hreflang="%s" href="%s%s">'
        % (o, raiz, caminho_pagina(o, chave)) for o in IDIOMAS)

    js = "\n".join('<script src="%sassets/js/%s" defer></script>' % (raiz, s) for s in scripts)

    return """<!doctype html>
<html lang="%(lang)s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="stylesheet" href="%(root)sassets/css/site.css">
%(alt)s
  <link rel="alternate" hreflang="x-default" href="%(root)s%(default)s">
</head>
<body>
<a class="skip" href="#main">%(skip)s</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="%(home)s"><span class="brand-name">%(name)s</span><span class="brand-tagline">%(tagline)s</span></a>
    <nav class="site-nav" aria-label="%(menu)s"><ul>%(nav)s</ul></nav>
    <nav class="lang" aria-label="%(langlabel)s">%(langs)s</nav>
  </div>
</header>
<main id="main" class="wrap">
<h1>%(h1)s</h1>
%(body)s
</main>
<footer class="site-footer">
  <div class="wrap">
    <p>%(origin)s</p>
    <p><a href="%(credits)s">%(creditslink)s</a></p>
  </div>
</footer>
%(js)s
</body>
</html>
""" % {
        "lang": idioma,
        "title": e(titulo_completo),
        "desc": e(texto["site"]["description"]),
        "root": raiz,
        "alt": alternates,
        "default": caminho_pagina(PADRAO, chave),
        "skip": e(texto["ui"]["skip"]),
        "home": url_relativa(chave, idioma, "home"),
        "name": e(texto["site"]["name"]),
        "tagline": e(texto["site"]["tagline"]),
        "menu": e(texto["ui"]["menu"]),
        "nav": "".join(nav),
        "langlabel": e(texto["ui"]["language"]),
        "langs": "".join(idiomas),
        "h1": e(titulo),
        "body": corpo,
        "origin": e(texto["footer"]["origin"]),
        "credits": url_relativa(chave, idioma, "credits"),
        "creditslink": e(texto["footer"]["creditsLink"]),
        "js": js,
    }


def render_raiz():
    links = "".join('<li><a href="%s">%s</a></li>' % (caminho_pagina(i, "home"), NOMES_IDIOMA[i])
                    for i in IDIOMAS)
    return """<!doctype html>
<html lang="%s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Slides4All</title>
<link rel="stylesheet" href="assets/css/site.css">
%s
  <link rel="alternate" hreflang="x-default" href="%s">
<script>
(function () {
  var supported = %s;
  var saved = null;
  try { saved = localStorage.getItem('s4a-lang'); } catch (err) {}
  var wanted = saved;
  if (!wanted) {
    var list = navigator.languages || [navigator.language || ''];
    for (var i = 0; i < list.length && !wanted; i++) {
      var code = String(list[i]).slice(0, 2).toLowerCase();
      if (supported.indexOf(code) !== -1) { wanted = code; }
    }
  }
  location.replace((wanted || '%s') + '/');
}());
</script>
</head>
<body class="root-choice">
<main class="wrap">
<h1>Slides4All</h1>
<p>Escolha o idioma. Choose your language. Elige el idioma.</p>
<ul class="links">%s</ul>
</main>
</body>
</html>
""" % (PADRAO,
       "\n".join('  <link rel="alternate" hreflang="%s" href="%s">' % (i, caminho_pagina(i, "home"))
                 for i in IDIOMAS),
       caminho_pagina(PADRAO, "home"),
       json.dumps(IDIOMAS), PADRAO, links)


# --------------------------------------------------------------------------

def main():
    conteudo = {}
    for idioma in IDIOMAS:
        caminho = os.path.join(CONTENT, "%s.json" % idioma)
        with open(caminho, encoding="utf-8") as fh:
            conteudo[idioma] = json.load(fh)
    with open(os.path.join(CONTENT, "gallery.json"), encoding="utf-8") as fh:
        galeria = json.load(fh)
    with open(os.path.join(CONTENT, "checklist.json"), encoding="utf-8") as fh:
        checklist = json.load(fh)

    validar(conteudo)
    validar_checklist(checklist)
    validar_galeria(galeria)
    if erros:
        for x in erros:
            print("ERRO  %s" % x, file=sys.stderr)
        raise SystemExit("%d problema(s) de conteudo, nada foi gerado" % len(erros))

    total_checklist = str(sum(len(g["items"]) for g in checklist))

    paginas = 0
    for idioma in IDIOMAS:
        texto = conteudo[idioma]
        destino_idioma = os.path.join(ROOT, idioma)
        if os.path.isdir(destino_idioma):
            shutil.rmtree(destino_idioma)
        for chave in SLUGS:
            pagina = texto["pages"][chave]
            ctx = {"idioma": idioma, "chave": chave, "texto": texto}
            corpo = render_blocos(pagina.get("blocks", []), ctx)
            scripts = []
            if chave == "mistakes":
                corpo += "\n" + render_mistakes(pagina, ctx)
            elif chave == "checklist":
                corpo += "\n" + render_checklist(pagina, ctx, checklist)
                scripts.append("checklist.js")
            elif chave == "timing":
                corpo += "\n" + render_timing(pagina, ctx)
                corpo += "\n" + render_blocos(pagina.get("after", []), ctx)
                scripts.append("timing.js")
            elif chave == "gallery":
                corpo += "\n" + render_gallery(pagina, ctx, galeria)
                scripts.append("gallery.js")
            elif chave == "templates":
                corpo += "\n" + render_templates(pagina, ctx)
            scripts.append("lang.js")

            html_pagina = montar_pagina(idioma, chave, texto, corpo, scripts)
            html_pagina = html_pagina.replace("{{checklistCount}}", total_checklist)
            caminho = os.path.join(ROOT, caminho_pagina(idioma, chave), "index.html")
            os.makedirs(os.path.dirname(caminho), exist_ok=True)
            with open(caminho, "w", encoding="utf-8") as fh:
                fh.write(html_pagina)
            paginas += 1

    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(render_raiz())

    if erros:
        for x in erros:
            print("ERRO  %s" % x, file=sys.stderr)
        raise SystemExit("%d problema(s) durante a geracao" % len(erros))
    for x in avisos:
        print("aviso  %s" % x)
    print("%d paginas geradas (%d idiomas), %d exemplos na galeria, %d itens no checklist"
          % (paginas + 1, len(IDIOMAS), len(galeria), int(total_checklist)))


if __name__ == "__main__":
    main()
