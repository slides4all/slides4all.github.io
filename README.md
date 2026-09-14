# Slides4All

Site trilíngue (português, inglês e espanhol) sobre como preparar e apresentar uma ótima apresentação técnica, com galeria de exemplos reais em PDF e PPTX.

Publicado em https://slides4all.github.io

O material tem origem na página de sugestões para apresentações do [SBSeg 2024](https://sbseg2024.ita.br/autores/sugestoes-para-apresentacoes/) e na [galeria de exemplos](https://sbseg24.github.io/slides/) associada, somadas às notas de revisão, à síntese de sugestões e ao checklist produzidos desde então.

## Como o site é construído

Não há framework, nem Node, nem Ruby. O conteúdo mora em JSON e um gerador em Python 3 escreve o HTML estático que o GitHub Pages serve.

```
content/pt.json  en.json  es.json   texto de todas as páginas
content/gallery.json                catálogo de exemplos, comum aos três idiomas
content/checklist.json              itens do checklist, nos três idiomas
build.py                            gera pt/, en/, es/ e index.html
assets/                             css, js, decks e miniaturas
assets/skill/skill_slides4all.md    skill de construção de apresentações para LLMs
tools/                              importadores e verificador
```

Para regerar o site depois de editar qualquer conteúdo:

```sh
python3 build.py
python3 tools/check_site.py
```

O gerador falha, em vez de publicar um site quebrado, quando uma chave existe em um idioma e falta em outro, quando uma entrada da galeria aponta para um arquivo inexistente ou quando um item do checklist não tem tradução nos três idiomas. É o que impede os idiomas de desandarem com o tempo.

O verificador confere links internos, recursos referenciados, atributo `alt` nas imagens, paridade de seções entre os idiomas e o limite de tamanho de arquivo do GitHub.

As pastas `pt/`, `en/`, `es/` e o `index.html` da raiz são gerados e versionados, para que o GitHub Pages publique direto, sem etapa de build.

## Ferramentas de importação

`tools/import_slides.py` copia os decks locais para `assets/slides/`, com nome normalizado, e gera as miniaturas com `pdftoppm`. A escolha entre versões duplicadas é declarada explicitamente no script.

`tools/fetch_sbseg24.py` espelha os arquivos da galeria do SBSeg 2024 e preserva os links originais de Google Drive, Canva e GitHub.

`tools/build_gallery.py` monta `content/gallery.json` a partir dos dois anteriores.

Esses três só precisam ser executados quando novos exemplos entram na galeria. Requerem `pdftoppm` e `pdfinfo`, do poppler.

## Skill para modelos de linguagem

`assets/skill/skill_slides4all.md` destila todo o conteúdo do site em um único arquivo Markdown, escrito para modelos de linguagem avançados conduzirem a construção da apresentação de ponta a ponta: entrevista de insumos, plano do deck em YAML, redação em formato de manchete, geração em PPTX, LaTeX Beamer ou HTML, auditoria automática do arquivo gerado e o checklist completo. Está publicado na página de templates e pode ser salvo como skill do Claude Code em `~/.claude/skills/slides4all/SKILL.md`, ou colado como instrução em qualquer assistente.

Os dois trechos de código publicados na skill, o de geração com `python-pptx` e o de auditoria do `.pptx`, foram executados contra decks reais da galeria antes da publicação.

## Conteúdo

Todo o conteúdo é de livre uso. Copie, adapte, traduza e reaproveite.

Os exemplos da galeria são publicados com autorização e com crédito nominal aos autores. Para remover um exemplo ou corrigir uma atribuição, abra uma issue.

Site publicado e mantido pelo [AI Horizon Labs](https://ai-horizon-labs.github.io/).
