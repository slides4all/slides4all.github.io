#!/usr/bin/env python3
"""Monta content/gallery.json a partir dos decks importados e do espelho do SBSeg 2024.

Titulos e autores foram extraidos do primeiro slide de cada PDF e revisados a
mao. O numero de slides vem dos proprios arquivos, nunca digitado.
"""
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLIDES = os.path.join(ROOT, "assets", "slides")

# slug -> titulo, autores, evento, ano, trilha, idioma do deck
LOCAIS = [
 ("tp-anna-statisticalranking-sbseg2026",
  "Statistical Ranking: A Voting-Based Ensemble Approach to Feature Selection in Android Malware Detection",
  "Anna Luiza Gomes, Lucas Ferreira, Angelo Gaspar, Diego Kreutz, Dionatan Schmidt, Rodrigo Mansilha, Kayuã Paim",
  "sbseg2026", 2026, "tp", "pt"),
 ("tp-beatriz-mulitaminer-versoes-sbseg2026",
  "MulitaMiner: avaliação multi-versão de extração de relatórios de vulnerabilidade com LLMs",
  "Beatriz Machado, Douglas Lautert, Cristhian Kapelinski, Diego Kreutz, Isadora Garcia Ferrão, Alessandro Bof",
  "sbseg2026", 2026, "tp", "pt"),
 ("tp-cristhian-dockerrandomsample-sbseg2026",
  "Uma medição de segurança das imagens do Docker Hub por amostra aleatória uniforme",
  "Cristhian Kapelinski, Diego Kreutz", "sbseg2026", 2026, "tp", "pt"),
 ("tp-cristhian-oscensus-sbseg2026",
  "OSCensus: um censo com múltiplos scanners das imagens-base Linux do Docker Hub",
  "Cristhian Kapelinski, Diego Kreutz", "sbseg2026", 2026, "tp", "pt"),
 ("tp-cristhian-quantizer4bitpii-sbseg2026",
  "Nem todo quantizador de 4 bits é igual: mitigação, na implantação, do vazamento de dados pessoais em modelos de linguagem pequenos ajustados",
  "Cristhian Kapelinski, Diego Kreutz", "sbseg2026", 2026, "tp", "pt"),
 ("tp-francis-securityevaluationiac-sbseg2026",
  "Security-First Evaluation of Text-to-Terraform: Benchmarking LLMs and SLMs for Secure IaC Generation",
  "Francis Vargas, Rodrigo Brandão Mansilha, Diego Kreutz", "sbseg2026", 2026, "tp", "pt"),
 ("tp-lucas-whenbalancingharms-sbseg2026",
  "When Balancing Harms: condições estruturais que degradam a detecção de malware Android após o balanceamento",
  "Lucas Ferreira, Anna Luiza Gomes, Angelo Diniz, Diego Kreutz, Dionatan R. Schmidt, Rodrigo Mansilha, Kayuã Oleques Paim",
  "sbseg2026", 2026, "tp", "pt"),
 ("tp-priscila-siemrules-sbseg2026",
  "Context-Aware SIEM Rule Generation with LLMs: When Site Profiles Are Not Enough",
  "Priscila Schafhauzer, Cristhian Kapelinski, Marcio Pohlmann, Diego Kreutz", "sbseg2026", 2026, "tp", "pt"),
 ("sf-ciocca-rulesfarmer-sbseg2026",
  "Toward Agentic Intrusion Detection in the Internet of Things: Rule Generation and Live Validation for XRCE-DDS Attacks",
  "Matheus Ciocca, Emanuel Ferreira, Tuigg Barcelos, Silvio Quincozes, Diego Kreutz, Paulo Souza",
  "sbseg2026", 2026, "sf", "pt"),
 ("sf-cristhian-zerolinc-sbseg2026",
  "ZeroLINC: Training-Free Local Classification of Security Incident Reports",
  "Cristhian Kapelinski, Beatriz Machado, Diego Kreutz", "sbseg2026", 2026, "sf", "pt"),
 ("sf-douglas-mulitaminer-sbseg2026",
  "MulitaMiner: An LLM-Based Tool for Structuring Vulnerability Scanner Reports",
  "Douglas Lautert, Beatriz Machado, Cristhian Kapelinski, Diego Kreutz", "sbseg2026", 2026, "sf", "pt"),
 ("sf-emanuel-ioteducore-sbseg2026",
  "IoTEdu Core: correlação multi-IDS e contenção automatizada de ataques em redes IoT institucionais",
  "Emanuel Ferreira, Matheus Ciocca, Douglas Fideles, Silvio Quincozes, Diego Kreutz",
  "sbseg2026", 2026, "sf", "pt"),
 ("sf-francis-aiacgateguard-sbseg2026",
  "AIaCGateGuard: A Security-First Pipeline for Benchmarking LLM- and SLM-Generated IaC",
  "Francis Luis Santos Vargas, Rodrigo Brandão Mansilha, Diego Kreutz", "sbseg2026", 2026, "sf", "pt"),
 ("sf-leonardo-attackzoo-sbseg2026",
  "AttackZoo: A Reproducible Testbed for Attack Execution and Network Traffic Dataset Generation",
  "Leonardo Bitzki, Diego Kreutz, Leandro Bertholdo, Cristhian Kapelinski", "sbseg2026", 2026, "sf", "pt"),
 ("sf-rui-adminforge-sbseg2026",
  "AdminForge: Declarative Privileged-Identity Management for Linux Server Fleets",
  "Rui de Quadros Ribeiro, Cristhian Kapelinski, Diego Kreutz", "sbseg2026", 2026, "sf", "pt"),
 ("wticg-beatriz-mulitaminer-slms-sbseg2026",
  "Local vs. nuvem: LLMs locais para extração de vulnerabilidades de relatórios de scanners de segurança",
  "Beatriz Machado, Cristhian Kapelinski, Diego Kreutz", "sbseg2026", 2026, "wticg", "pt"),
 ("wticg-cristhian-cryptocensus-sbseg2026",
  "CryptoCensus: postura criptográfica e prontidão pós-quântica do Docker Hub",
  "Cristhian Kapelinski, Diego Kreutz", "sbseg2026", 2026, "wticg", "pt"),
 ("wticg-cristhian-pixguardsim-sbseg2026",
  "PixGuard-Sim: um testbed sensível a prazo para detectores de fraude no Pix",
  "Cristhian Kapelinski, Diego Kreutz", "sbseg2026", 2026, "wticg", "pt"),
 ("wticg-cristhian-ragtrap-sbseg2026",
  "RAGtrap: revogação de fontes e consulta indexada de proveniência para corpora RAG envenenados",
  "Cristhian Kapelinski, Diego Kreutz", "sbseg2026", 2026, "wticg", "pt"),
]

# slug do espelho -> titulo, autores, evento, ano, trilha, idioma
ESPELHO = {
 "wticg2023-analise": ("Análise do protocolo Committeeless Proof-of-Stake: em busca de um melhor ponto de operação",
   "Vinícius Peixoto, Marco Aurélio Amaral Henriques", "sbseg2023", 2023, "wticg", "pt"),
 "wticg2023-aplicacao": ("Aplicação de criptografia homomórfica na mineração de dados em fluxos de roteadores de borda na Internet",
   "Felipe M. F. Assis, Evandro L. C. Macedo, Luís Felipe M. de Moraes", "sbseg2023", 2023, "wticg", "pt"),
 "wticg2023-impacto": ("Impacto da otimização de funções hash no desempenho do algoritmo de assinaturas digitais pós-quântica CRYSTALS-Dilithium",
   "Rodrigo Duarte de Meneses, Marco Aurélio Amaral Henriques", "sbseg2023", 2023, "wticg", "pt"),
 "wticg2023-modelagem": ("Modelagem das áreas de risco de sistemas de detecção de intrusão para cálculo de métricas de privacidade",
   "Jessica Yumi Nakano Sato, Daniel Macêdo Batista", "sbseg2023", 2023, "wticg", "pt"),
 "wticg2023-secflow": ("SecFlow: aprendizado não supervisionado para análise e detecção de anomalias em redes de computadores",
   "Felipe Salles, Luiz Claudio Schara, Taiane Ramos", "sbseg2023", 2023, "wticg", "pt"),
 "wrseg2018-idvvs-opensgx-slides": ("Inicialização e geração de iDVVs com Intel SGX e OpenSGX",
   "Rodrigo Masera, Rodrigo Machado, Diego Kreutz", "wrseg2018", 2018, "wrseg", "pt"),
 "wrseg2018-seguraai-slides": ("SeguraAí: confidencialidade de dados sensíveis com SGX",
   "Felipe Antunes, Filipe Garcia, Diego Kreutz", "wrseg2018", 2018, "wrseg", "pt"),
 "wrseg2020-formsonline-slides": ("Viralização de questionários online: desafios e oportunidades",
   "Maurício El Uri, Rafael Kreutz, Maurício Fiorenza, Diego Kreutz, Thiago Escarrone, Daniel Temp, Vinicius Nunez, Rodrigo Mansilha",
   "wrseg2020", 2020, "wrseg", "pt"),
 "wrseg2023-autodroid": ("AutoDroid: disponibilizando a ferramenta DroidAugmentor como serviço",
   "Luiz Felipe Laviola, Kayuã Paim, Diego Kreutz, Rodrigo Mansilha", "wrseg2023", 2023, "wrseg", "pt"),
 "wrseg2023-ewebapi": ("eWebAPI: uma API para assinar digitalmente lotes de certificados eletrônicos utilizando o e-certsDS",
   "Alan Schulze, Diego Kreutz", "wrseg2023", 2023, "wrseg", "pt"),
 "wrseg2023-fs3ev2": ("Avaliação de métodos de seleção de características de amostras Android com a ferramenta FS3E (v2)",
   "Nicolas Neves, Vanderson Rocha, Diego Kreutz, Hendrio Bragança, Eduardo Feitosa", "wrseg2023", 2023, "wrseg", "pt"),
 "sbseg2020-auth4app-slides": ("Auth4App: Protocols for Identification and Authentication using Mobile Applications",
   "Diego Kreutz, Rafael Fernandes, Giulliano Paz, Tadeu Jenuario, Rodrigo Mansilha, Roger Immich, Charles C. Miers",
   "sbseg2020", 2020, "tp", "pt"),
 "sbseg2020-fws-hybridnets-slides": ("Gerenciamento de firewalls em redes híbridas",
   "Maurício Fiorenza, Diego Kreutz, Rodrigo Mansilha", "sbseg2020", 2020, "tp", "pt"),
 "sbseg2021-sf-ecertsds": ("e-certsDS: certificados eletrônicos com assinatura digital",
   "Maurício El Uri, Luciano Vargas, Diego Kreutz", "sbseg2021", 2021, "sf", "pt"),
 "sbseg2022-sf-adbuilder": ("ADBuilder: ferramenta de construção de datasets para detecção de malwares Android",
   "Lucas Vilanova, Diego Kreutz, Joner Assolin, Vagner Quincozes, Charles Miers, Rodrigo Mansilha, Eduardo Feitosa",
   "sbseg2022", 2022, "sf", "pt"),
 "sbseg2022-sf-autocar": ("AutoCAR: automação e reprodutibilidade de testes de métodos de classificação baseados em regras de associação",
   "Vanderson Rocha, Diego Kreutz, Eduardo Feitosa", "sbseg2022", 2022, "sf", "pt"),
 "sbseg2022-tp-analise": ("Uma análise de métodos de seleção de características aplicados à detecção de malwares Android",
   "Taina Soares, Diego Kreutz, Vanderson Rocha, Estevão Costa, Luiza Leão, Jonas Pontes, Joner Assolin, Gustavo Rodrigues, Eduardo Feitosa",
   "sbseg2022", 2022, "tp", "pt"),
 "sbseg2022-tp-metodos": ("Avaliação de métodos de classificação baseados em regras de associação para detecção de malwares Android",
   "Vanderson Rocha, Diego Kreutz, Jonas Pontes, Eduardo Feitosa", "sbseg2022", 2022, "tp", "pt"),
 "sbseg2023-sf-amgenerator-amexplorer": ("AMGenerator e AMExplorer: geração de metadados e construção de datasets Android",
   "Vanderson Rocha, Joner Assolin, Hendrio Bragança, Diego Kreutz, Eduardo Feitosa", "sbseg2023", 2023, "sf", "pt"),
 "sbrc2020-https-br-slides": ("Uma análise da utilização de HTTPS no Brasil",
   "Maurício Fiorenza, Diego Kreutz, Thiago Escarrone, Daniel Temp", "sbrc2020", 2020, "sbrc", "pt"),
 "dsn2023-ibc-performance": ("Analyzing the Performance of the Inter-Blockchain Communication Protocol",
   "João Otávio Chervinski, Diego Kreutz, Xiwei Xu, Jiangshan Yu", "dsn2023", 2023, "dsn", "en"),
}

ROTULOS = {"Slides online at Google Drive": "Google Drive",
           "Slides in Google Drive": "Google Drive",
           "Slides online at Canvas": "Canva",
           "Slides Template on GitHub": "GitHub"}


def paginas(pdf):
    out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
    m = re.search(r"Pages:\s+(\d+)", out)
    return int(m.group(1)) if m else None


def formatos_locais(slug):
    fs = []
    for ext in ("pdf", "pptx"):
        p = os.path.join(SLIDES, "%s.%s" % (slug, ext))
        if os.path.exists(p):
            fs.append({"type": ext, "url": "assets/slides/%s.%s" % (slug, ext),
                       "bytes": os.path.getsize(p)})
    return fs


def main():
    entradas = []
    for slug, titulo, autores, evento, ano, trilha, idioma in LOCAIS:
        pdf = os.path.join(SLIDES, slug + ".pdf")
        entradas.append({
            "slug": slug, "title": titulo, "authors": autores, "event": evento,
            "year": ano, "track": trilha, "lang": idioma,
            "slides": paginas(pdf), "thumb": "assets/thumbs/%s.png" % slug,
            "files": formatos_locais(slug), "source": "local"})

    espelho = json.load(open(os.path.join(ROOT, "tools", "sbseg24_entries.json"),
                             encoding="utf-8"))
    for reg in espelho:
        slug = reg["slug"]
        if slug not in ESPELHO:
            continue
        titulo, autores, evento, ano, trilha, idioma = ESPELHO[slug]
        files = formatos_locais(slug)
        z = os.path.join(SLIDES, slug + ".zip")
        if os.path.exists(z):
            files.append({"type": "latex", "url": "assets/slides/%s.zip" % slug,
                          "bytes": os.path.getsize(z)})
        for f in reg["formatos"]:
            if f["tipo"] == "externo":
                files.append({"type": "external",
                              "label": ROTULOS.get(f["rotulo"], f["rotulo"]),
                              "url": f["url"]})
        entradas.append({
            "slug": slug, "title": titulo, "authors": autores, "event": evento,
            "year": ano, "track": trilha, "lang": idioma,
            "slides": reg.get("slides"), "thumb": "assets/thumbs/%s.png" % slug,
            "files": files, "source": "sbseg24"})

    faltantes = [e["slug"] for e in entradas
                 if not os.path.exists(os.path.join(ROOT, e["thumb"]))]
    if faltantes:
        raise SystemExit("sem miniatura: %s" % ", ".join(faltantes))

    entradas.sort(key=lambda e: (-e["year"], e["track"], e["slug"]))
    destino = os.path.join(ROOT, "content", "gallery.json")
    with open(destino, "w", encoding="utf-8") as fh:
        json.dump(entradas, fh, ensure_ascii=False, indent=2)
    print("%d entradas em content/gallery.json" % len(entradas))
    for ev in sorted({e["event"] for e in entradas}):
        print("   %-12s %d" % (ev, sum(1 for e in entradas if e["event"] == ev)))


if __name__ == "__main__":
    main()
