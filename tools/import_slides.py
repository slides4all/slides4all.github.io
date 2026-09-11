#!/usr/bin/env python3
"""Importa os decks locais para assets/slides/ e gera as miniaturas.

A lista de decks e a escolha entre versoes duplicadas sao declaradas
explicitamente aqui. Nao ha heuristica por data: os metadados internos dos
PPTX foram removidos na exportacao do Google Slides e o mtime do arquivo
reflete o download em lote, nao a autoria. A escolha veio da comparacao de
conteudo slide a slide, registrada na spec.
"""
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "templates_exemplos")
SLIDES = os.path.join(ROOT, "assets", "slides")
THUMBS = os.path.join(ROOT, "assets", "thumbs")

# slug -> (arquivo pdf, arquivo pptx)
DECKS = {
    "sf-ciocca-rulesfarmer-sbseg2026": (
        "SF_Ciocca_RulesFarmer_SBSeg2026_Slides.pptx (2).pdf",
        "SF_Ciocca_RulesFarmer_SBSeg2026_Slides.pptx"),
    "sf-cristhian-zerolinc-sbseg2026": (
        "SF_Cristhian_ZeroLINC_SBSeg2026_Slides.pptx.pdf",
        "SF_Cristhian_ZeroLINC_SBSeg2026_Slides.pptx"),
    "sf-douglas-mulitaminer-sbseg2026": (
        "SF_Douglas_MulitaMiner_SBSeg2026_Slides.pptx.pdf",
        "SF_Douglas_MulitaMiner_SBSeg2026_Slides(1).pptx"),
    "sf-emanuel-ioteducore-sbseg2026": (
        "SF_Emanuel_IoTEduCore_SBSeg2026.pptx (1).pdf",
        "SF_Emanuel_IoTEduCore_SBSeg2026.pptx"),
    "sf-francis-aiacgateguard-sbseg2026": (
        "SF_FrancisVargas_AIaCGateGuard_SBSeg2026.pptx.pdf",
        "SF_FrancisVargas_AIaCGateGuard_SBSeg2026.pptx"),
    "sf-leonardo-attackzoo-sbseg2026": (
        "SF_Leonardo_AttackZoo_SBSeg2026_Slides.pptx (1).pdf",
        "SF_Leonardo_AttackZoo_SBSeg2026_Slides.pptx"),
    "sf-rui-adminforge-sbseg2026": (
        "SF_Rui_AdminForge_SBSeg2026_Slides.pptx.pdf",
        "SF_Rui_AdminForge_SBSeg2026_Slides.pptx"),
    "tp-anna-statisticalranking-sbseg2026": (
        "TP_Anna_StatisticalRanking_SBSeg2026_Slides.pptx.pdf",
        "TP_Anna_StatisticalRanking_SBSeg2026_Slides.pptx"),
    "tp-beatriz-mulitaminer-versoes-sbseg2026": (
        "TP_Beatriz_MulitaMiner-Versoes_SBSeg2026_Slides.pptx.pdf",
        "TP_Beatriz_MulitaMiner-Versoes_SBSeg2026_Slides.pptx"),
    "tp-cristhian-dockerrandomsample-sbseg2026": (
        "TP_Cristhian_DockerRandomSample_SBSeg2026_Slides.pptx.pdf",
        "TP_Cristhian_DockerRandomSample_SBSeg2026_Slides.pptx"),
    "tp-cristhian-oscensus-sbseg2026": (
        "TP_Cristhian_OSCensus_SBSeg2026_Slides.pptx.pdf",
        "TP_Cristhian_OSCensus_SBSeg2026_Slides.pptx"),
    "tp-cristhian-quantizer4bitpii-sbseg2026": (
        "TP_Cristhian_Quantizer4bitPII_SBSeg2026_Slides.pptx.pdf",
        "TP_Cristhian_Quantizer4bitPII_SBSeg2026_Slides.pptx"),
    "tp-francis-securityevaluationiac-sbseg2026": (
        "TP_Francis_SecurityEvaluationIaC_SBSeg26_Slides.pptx.pdf",
        "TP_Francis_SecurityEvaluationIaC_SBSeg26_Slides.pptx"),
    "tp-lucas-whenbalancingharms-sbseg2026": (
        "TP_Lucas_WhenBalancingHarms_SBSeg2026_Slides.pptx.pdf",
        "TP_Lucas_WhenBalancingHarms_SBSeg2026_Slides.pptx"),
    "tp-priscila-siemrules-sbseg2026": (
        "TP_Priscila_SIEMRules_SBSeg2026.pptx.pdf",
        "TP_Priscila_SIEMRules_SBSeg2026.pptx"),
    "wticg-beatriz-mulitaminer-slms-sbseg2026": (
        "WTICG_Beatriz_MulitaMiner-SLMS_SBSeg2026_Slides.pptx.pdf",
        "WTICG_Beatriz_MulitaMiner-SLMS_SBSeg2026_Slides.pptx"),
    "wticg-cristhian-cryptocensus-sbseg2026": (
        "WTICG_Cristhian_CryptoCensus_SBSeg2026_Slides.pptx.pdf",
        "WTICG_Cristhian_CryptoCensus_SBSeg2026_Slides.pptx"),
    "wticg-cristhian-pixguardsim-sbseg2026": (
        "WTICG_Cristhian_PixGuardSim_SBSeg2026_Slides.pptx.pdf",
        "WTICG_Cristhian_PixGuardSim_SBSeg2026_Slides.pptx"),
    "wticg-cristhian-ragtrap-sbseg2026": (
        "WTICG_Cristhian_RAGTRAP_SBSeg2026_Slides.pptx.pdf",
        "WTICG_Cristhian_RAGTRAP_SBSeg2026_Slides.pptx"),
    "template-sbseg2024": (
        "SBSeg24 - Slides - Template do Evento - v1 - FINAL _ OFICIAL.pdf",
        "SBSeg24 - Slides - Template do Evento - v1 - FINAL _ OFICIAL.pptx"),
}

# Decks deliberadamente fora da galeria.
IGNORADOS = {
    "IoTEdu - Forum RNP+ TEND 2026 - Brasilia - FINAL _ OFICIAL":
        "material institucional de divulgacao, nao exemplo didatico",
    "IoTEdu - RNP+ (Lab) - FINAL _ OFICIAL":
        "material institucional de divulgacao, nao exemplo didatico",
    "IoTEdu - WTIC IFES 2026 - FINAL _ OFICIAL":
        "material institucional de divulgacao, nao exemplo didatico",
}


def paginas(pdf):
    out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
    m = re.search(r"Pages:\s+(\d+)", out)
    if not m:
        raise SystemExit("nao consegui ler o numero de paginas de %s" % pdf)
    return int(m.group(1))


def miniatura(pdf, slug):
    destino = os.path.join(THUMBS, slug)
    subprocess.run(["pdftoppm", "-png", "-f", "1", "-l", "1",
                    "-scale-to-x", "640", "-scale-to-y", "-1",
                    pdf, destino], check=True)
    gerado = destino + "-1.png"
    if not os.path.exists(gerado):
        gerado = destino + "-01.png"
    if not os.path.exists(gerado):
        raise SystemExit("pdftoppm nao gerou miniatura para %s" % slug)
    final = os.path.join(THUMBS, slug + ".png")
    os.replace(gerado, final)
    return final


def main():
    if not os.path.isdir(SRC):
        raise SystemExit("pasta %s nao encontrada" % SRC)
    os.makedirs(SLIDES, exist_ok=True)
    os.makedirs(THUMBS, exist_ok=True)

    faltando = []
    for slug, (pdf, pptx) in DECKS.items():
        for f in (pdf, pptx):
            if not os.path.exists(os.path.join(SRC, f)):
                faltando.append((slug, f))
    if faltando:
        for slug, f in faltando:
            print("FALTA  %s -> %s" % (slug, f), file=sys.stderr)
        raise SystemExit("arquivos de origem ausentes")

    relatorio = {}
    for slug, (pdf, pptx) in sorted(DECKS.items()):
        src_pdf = os.path.join(SRC, pdf)
        shutil.copy2(src_pdf, os.path.join(SLIDES, slug + ".pdf"))
        shutil.copy2(os.path.join(SRC, pptx), os.path.join(SLIDES, slug + ".pptx"))
        n = paginas(src_pdf)
        miniatura(src_pdf, slug)
        relatorio[slug] = {"slides": n, "pdf": pdf, "pptx": pptx}
        print("  %-44s %3d slides" % (slug, n))

    for nome, motivo in sorted(IGNORADOS.items()):
        print("  ignorado: %s (%s)" % (nome, motivo))

    saida = os.path.join(ROOT, "tools", "import_report.json")
    with open(saida, "w", encoding="utf-8") as fh:
        json.dump(relatorio, fh, ensure_ascii=False, indent=2, sort_keys=True)
    print("\n%d decks importados, relatorio em tools/import_report.json" % len(relatorio))


if __name__ == "__main__":
    main()
