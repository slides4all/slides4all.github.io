# Slides4All: site trilíngue sobre como fazer ótimas apresentações

Data: 2026-09-11
Repositório: `slides4all/slides4all.github.io` (GitHub Pages)
Autor principal: Diego Kreutz

## 1. Objetivo

Publicar um site público, em português do Brasil, inglês e espanhol, que ensine a preparar e a executar uma ótima apresentação técnica, acompanhado de uma galeria de exemplos reais de slides com os arquivos disponíveis para download e edição.

O ponto de partida é a página "Sugestões para Apresentações" do SBSeg 2024 (https://sbseg2024.ita.br/autores/sugestoes-para-apresentacoes/) e a galeria associada (https://sbseg24.github.io/slides/). A esse material somam-se três documentos internos de 2026: as notas e observações gerais, a síntese das sugestões e o checklist de revisão de slides. O site consolida tudo isso num recurso permanente, independente de edição de evento, e em três idiomas.

## 2. Decisões já tomadas

Estas decisões foram acordadas com o autor antes da redação desta spec e não estão em aberto.

| Assunto | Decisão |
| --- | --- |
| Tecnologia | HTML, CSS e JavaScript estáticos, sem dependência de execução no visitante além do próprio navegador. Sem Ruby, sem Node. |
| Fonte do conteúdo | Arquivo JSON por idioma (`content/pt.json`, `en.json`, `es.json`) mais um gerador em Python 3 (`build.py`) que produz HTML estático versionado no repositório. |
| Idioma na raiz | `/index.html` redireciona conforme o idioma do navegador, com português como padrão, e mostra os três links caso o JavaScript esteja desativado. |
| Arquivos da galeria | PDF e PPTX versionados no próprio repositório, deduplicados, mais miniaturas geradas localmente. |
| Exemplos do SBSeg 2024 | Os 27 arquivos de https://sbseg24.github.io/slides/files/ são espelhados no repositório (60 MB), preservando também os links originais de Google Drive, LaTeX e Canva. |
| Autorização dos decks locais | Publicação autorizada pelo autor principal, com crédito nominal a cada autor. |
| Decks IoTEdu | Ficam fora da galeria (material institucional de divulgação, não exemplo didático). |
| Identidade visual | Fundo branco, tipografia grande, muito espaço em branco, filetes finos, uma única cor de destaque. O site aplica em si mesmo as regras que ensina. |
| Créditos | Os cinco colaboradores do SBSeg 2024 mais os contribuidores da galeria, com nota de origem. |
| Páginas extras | Checklist interativo, galeria de erros comuns antes e depois, calculadora de tempo e página de templates. |

## 3. Mapa do site

Nove páginas por idioma, com slug traduzido. O gerador mantém a tabela de equivalência entre idiomas, de modo que o seletor de idioma sempre leva à página correspondente, e não à home.

| Página | PT | EN | ES |
| --- | --- | --- | --- |
| Home | `/pt/` | `/en/` | `/es/` |
| Fazer os slides | `/pt/slides/` | `/en/slides/` | `/es/slides/` |
| Apresentar | `/pt/apresentar/` | `/en/presenting/` | `/es/presentar/` |
| Erros comuns | `/pt/erros/` | `/en/mistakes/` | `/es/errores/` |
| Checklist | `/pt/checklist/` | `/en/checklist/` | `/es/checklist/` |
| Tempo | `/pt/tempo/` | `/en/timing/` | `/es/tiempo/` |
| Galeria | `/pt/galeria/` | `/en/gallery/` | `/es/galeria/` |
| Templates | `/pt/templates/` | `/en/templates/` | `/es/plantillas/` |
| Créditos | `/pt/creditos/` | `/en/credits/` | `/es/creditos/` |

São nove páginas por idioma, 27 no total, mais a raiz.

A divisão entre "Fazer os slides" e "Apresentar" substitui as três listas do SBSeg 2024 ("Dicas Gerais", "Dicas de Conteúdo", "Dicas de Preparação"), que se sobrepõem entre si: as duas primeiras tratam do artefato, a terceira trata da pessoa. Nenhum conteúdo do material original é descartado nessa reorganização.

## 4. Conteúdo das páginas

### 4.1 Home

Abertura com a tese central: uma apresentação existe para que a plateia entenda o argumento, não para exibir o texto do artigo. Se ao final a plateia não entendeu, a apresentação falhou.

Três chamadas diretas para os caminhos mais usados: o checklist (para quem já tem os slides prontos), a página de slides (para quem vai começar) e a galeria (para quem quer se inspirar). Uma linha final registra que o site segue as próprias regras que ensina e que nasceu do material do SBSeg 2024.

### 4.2 Fazer os slides

Seis blocos, na ordem de impacto observado nas revisões reais:

1. **Fontes e legibilidade.** Mínimo de 24pt para conteúdo e 32pt ou mais para títulos. O teste do celular a 50 cm como critério objetivo de aprovação. A regra decisiva: quando falta espaço, corte conteúdo, nunca a fonte. Assuma sempre sala grande e lotada.
2. **Figuras e gráficos.** Ocupar o máximo de espaço possível, inclusive 100% do slide, sobrepondo título e rodapé quando a figura for complexa. Apresentação progressiva de figuras de fluxo, uma etapa por slide. Todo experimento precisa de uma figura de pipeline ou fluxograma. Preferência por vetorial ou alta definição, e rejeição de recortes de tela. Remoção de figuras decorativas.
3. **Texto.** Itens curtos no lugar de frases. A técnica da manchete de jornal, com o exemplo do SBSeg 2024 preservado ("O novo sistema XPTO desenvolvido neste trabalho teve um desempenho que superou em 30% a melhor versão da literatura" vira "XPTO: desempenho 30% superior ao estado da arte"). Nada de bloco de texto ao lado do gráfico. Nada de palavras fortes sem evidência. Um idioma só por deck.
4. **Visual.** Fundo branco, sem cinza nem colorido atrás de texto. Contraste, com as três leituras recomendadas do SBSeg 2024. Remoção de números decorativos das caixas, usando o espaço para as palavras-chave. Texto que não encosta nem vaza das bordas. Logomarcas do primeiro slide grandes o suficiente.
5. **Consistência.** Mesma fonte, cor, alinhamento e espaçamento para elementos equivalentes, do primeiro ao último slide. Ou abrevia tudo, ou não abrevia nada. Ou tudo em português, ou tudo em inglês.
6. **Tabelas e trabalhos relacionados.** Fonte grande no conteúdo, cabeçalho bem formatado, tabela reconstruída em vez de copiada do artigo, exibição progressiva com destaque. A tabela de trabalhos relacionados precisa evidenciar a lacuna, não apenas listar trabalhos, e quando aparece no início da apresentação o título melhor é "O que já existe e o que falta".

Fecha com a estrutura recomendada da apresentação: problema, desafios, o que já existe e o que falta, solução, resultados, considerações. Inclui a sugestão de fugir do slide de roteiro tradicional e abrir com uma motivação forte, e a prática de manter slides de reserva para perguntas da banca, observada no exemplo IoTEduCore.

### 4.3 Apresentar

Ensaio: pelo menos cinco vezes, em pé e falando alto, porque só a partir do quinto ou sexto ensaio o discurso fica fluido. A lista dos sinais de falta de ensaio que a plateia percebe. A recomendação de gravar áudio ou vídeo e ouvir depois.

Tempo: respeitar o slot com tolerância de 5% nos ensaios e jamais ultrapassar 10%. O constrangimento das duas falhas simétricas, terminar tarde e terminar cedo demais. A divisão sugerida do tempo, que na página aparece junto com o link para a calculadora.

Execução: olhar para a plateia, não ler os slides, numerar os slides, não ficar mais de dois minutos no mesmo slide, não passar informação fundamental só pela fala.

Revisão: pelo menos duas revisões com os coautores, e a revisão final por alguém que não participou da elaboração, feita no celular.

### 4.4 Erros comuns

Cada padrão do documento de notas vira um par antes e depois, com uma frase explicando por que o erro atrapalha e o que fazer no lugar. Padrões cobertos: fundo cinza ou colorido; fonte pequena em corpo, tabela e gráfico; bloco de texto ao lado do gráfico; figura pequena com espaço em branco sobrando; figura complexa num slide só; números decorativos nas caixas; texto encostando ou vazando da borda; mistura de português e inglês; abreviação inconsistente; tabela de trabalhos relacionados que só lista; logomarca minúscula no primeiro slide.

**As ilustrações são criadas do zero, em SVG, reproduzindo o erro descrito.** Não se usam recortes dos decks reais dos autores para ilustrar erro, mesmo com autorização geral de publicação: quem contribuiu de boa-fé com um bom exemplo não deve aparecer como caso negativo.

### 4.5 Checklist

Os oito blocos e os 35 itens do documento `COISAS - CHECKLIST DE REVISÃO DE SLIDES.docx`, na íntegra e na mesma ordem: teste do celular, fontes, figuras e gráficos, texto, visual, consistência, tabelas, antes de enviar.

Comportamento: caixas clicáveis, contador de progresso por bloco e total, estado salvo no navegador por idioma, botão para reiniciar e botão para copiar o checklist como texto simples, útil para colar num e-mail de orientação.

O estado usa `localStorage` com leitura e escrita protegidas, e a página funciona normalmente quando o armazenamento não está disponível: perde apenas a persistência.

### 4.6 Tempo

Entrada: duração do slot em minutos. Saída: os minutos de cada parte segundo a divisão de 30% para fundamentação, 15% para objetivo e problema, 45% para contribuição e resultados, 10% para considerações e agradecimentos; a faixa recomendada de slides; a tolerância de 5% em segundos; e o limite absoluto de 10%.

Botões rápidos para os slots mais comuns (15, 20, 25 e 30 minutos) e a ressalva do material original: um slide por minuto é uma boa regra de bolso, mais precisa em apresentações curtas do que em longas.

Cálculo inteiramente no navegador, sem servidor.

### 4.7 Galeria

Catálogo único com 40 entradas, vindas de duas origens: 19 trabalhos locais de 2026 e 21 exemplos espelhados do SBSeg 2024. As entradas de template da galeria original não entram aqui: vão para a página de templates.

**Origem 1, decks locais de 2026 (19 trabalhos).** O template do evento SBSeg 2024, também presente na pasta local, não entra na galeria: vai para a página de templates. Deduplicação já decidida por comparação de conteúdo slide a slide:

| Trabalho | Versões encontradas | Versão mantida | Critério |
| --- | --- | --- | --- |
| Ciocca, RulesFarmer | 21, 20 e 20 slides | 21 slides (`SF_Ciocca_RulesFarmer_SBSeg2026_Slides.pptx` e `... .pptx (2).pdf`) | única com apresentação progressiva por etapas e texto revisado |
| Douglas, MulitaMiner | 16 e 9 slides | 16 slides (`SF_Douglas_MulitaMiner_SBSeg2026_Slides(1).pptx` e `... .pptx.pdf`) | quebra o pipeline em quatro slides progressivos |
| Emanuel, IoTEduCore | 37 e 20 slides | 37 slides (`SF_Emanuel_IoTEduCore_SBSeg2026.pptx` e `... .pptx (1).pdf`) | contém a de 20 mais 15 slides de reserva para perguntas |

Os demais 16 trabalhos têm versão única. Os três decks IoTEdu ficam fora. Nenhuma conversão de formato é necessária: todos os PPTX mantidos já possuem PDF correspondente, verificado por contagem de páginas e pelo texto do primeiro slide. Os PDFs apenas seguem três padrões de nome diferentes (`x.pptx.pdf`, `x.pptx (n).pdf` e `x.pdf`), que o importador normaliza.

**Origem 2, espelho do SBSeg 2024 (21 exemplos mais 1 template).** A galeria de origem tem 25 entradas, das quais 4 são templates (o do SBSeg 2024, listado duas vezes, e os dois em LaTeX), restando 21 exemplos. Os 27 arquivos de `sbseg24.github.io/slides/files/` (60 MB no total) são baixados para o repositório. Os links originais de Google Drive, Canva e GitHub, presentes na galeria de origem, são preservados como formato adicional de cada entrada.

**Metadados por entrada:** identificador, título, autores, evento, ano, trilha (TP, SF, WTICG, WRSeg, minicurso ou template), número de slides, idioma do deck, miniatura e lista de formatos disponíveis com URL de cada um.

**Filtros no navegador:** por evento, por trilha e por formato, sem recarregar a página e sem servidor. A lista completa é renderizada no HTML pelo gerador, de modo que a galeria continua legível com o JavaScript desativado; os filtros são um acréscimo, não um pré-requisito.

**Miniaturas:** primeira página de cada PDF, via `pdftoppm`, largura de 640 px, em PNG. São 41 miniaturas (40 da galeria mais a do template), aproximadamente 7 MB.

### 4.8 Templates

Separada da galeria, reúne três templates que servem de ponto de partida: o do SBSeg 2024 em PPTX, PDF e Google Drive, e os dois em LaTeX de Émerson Mello (`ifscyan` e `ifsclean`, no GitHub).

O template do evento presente na pasta local e o `SBSeg2024_Slides_Template_v1` remoto são o mesmo material: 22 slides, conteúdo idêntico, diferindo apenas nos metadados de exportação do PDF. Publica-se uma única entrada, usando a cópia local como arquivo canônico.

### 4.9 Créditos

Os colaboradores do texto original do SBSeg 2024: Diego Kreutz (UNIPAMPA), Marco A. Amaral Henriques (UNICAMP), Charles Christian Miers (UDESC), Cintia Borges Margi (USP) e Rodrigo Brandão Mansilha (UNIPAMPA). Os contribuidores da galeria original: Diego Kreutz, Émerson Mello, Felipe Assis, Felipe Salles, Isadora Ferrão, Jessica Sato, João Otávio Chervinski e Vinícius Rodrigues. Os autores dos decks de 2026, nomeados em cada entrada da galeria. Nota de origem e link para a página do SBSeg 2024. Licença de uso do material e convite para contribuir com novos exemplos.

## 5. Arquitetura

### 5.1 Estrutura de diretórios

```
build.py                        gerador
tools/import_slides.py          importa, deduplica, renomeia e gera miniaturas
tools/fetch_sbseg24.py          baixa o espelho dos 27 arquivos do SBSeg 2024
content/pt.json                 texto de todas as páginas, em português
content/en.json                 idem, inglês
content/es.json                 idem, espanhol
content/gallery.json            catálogo de exemplos, comum aos três idiomas
content/checklist.json          itens do checklist, com texto nos três idiomas
templates/base.html             cabeçalho, rodapé, seletor de idioma
templates/*.html               um por tipo de página
assets/css/site.css
assets/js/checklist.js  timing.js  gallery.js  lang.js
assets/img/                     ilustrações SVG dos erros comuns
assets/slides/<slug>.pdf
assets/slides/<slug>.pptx
assets/thumbs/<slug>.png
pt/  en/  es/                   HTML gerado, versionado
index.html                      raiz, redirecionamento por idioma
```

A pasta `templates_exemplos/` é consumida pelo importador e sai do repositório ao final, substituída por `assets/slides/`. O `.gitignore` atual, herdado de um template de jogo Adventure Game Studio, é substituído por um adequado ao projeto.

### 5.2 O gerador

`python3 build.py` lê os JSON de conteúdo e os templates e escreve `pt/`, `en/`, `es/` e `index.html`.

Validações que fazem o gerador falhar com mensagem clara, em vez de produzir um site quebrado:

- chave presente em `pt.json` e ausente em `en.json` ou `es.json`, e vice-versa;
- entrada da galeria apontando para arquivo inexistente em `assets/slides/` ou `assets/thumbs/`;
- link interno para uma página que não existe na tabela de slugs;
- item do checklist sem tradução em algum dos três idiomas.

O gerador é idempotente: rodar duas vezes seguidas produz exatamente os mesmos arquivos.

### 5.3 Importador de slides

`python3 tools/import_slides.py` executa, de forma reproduzível e sem apagar nada do original:

1. lê a lista de decks mantidos, declarada explicitamente no próprio script (não por heurística de data, que é inconfiável nestes arquivos, pois os metadados internos foram removidos na exportação e o `mtime` reflete o download);
2. copia PDF e PPTX para `assets/slides/` com nome normalizado em minúsculas, sem espaços nem parênteses, no padrão `<trilha>-<autor>-<projeto>-<evento><ano>`;
3. extrai o número de slides de cada PDF;
4. gera a miniatura da primeira página com `pdftoppm -png -f 1 -l 1 -scale-to-x 640 -scale-to-y -1`;
5. emite um relatório do que copiou, do que ignorou e por quê.

`tools/fetch_sbseg24.py` faz o mesmo para os 27 arquivos remotos, com verificação de tamanho e repetição em caso de falha de rede.

Os dois scripts alimentam `content/gallery.json`, que depois é revisado à mão para títulos e autores legíveis.

### 5.4 Idioma e navegação

`index.html` na raiz lê `navigator.languages`, escolhe entre `pt`, `en` e `es`, e redireciona, gravando a escolha. Uma escolha manual no seletor de idioma tem prioridade sobre a detecção nas visitas seguintes. Sem JavaScript, a raiz mostra os três links em texto.

Cada página traz `<link rel="alternate" hreflang>` para as suas equivalentes, e `lang` correto no elemento raiz.

### 5.5 Design

Fundo branco puro, texto quase preto, uma única cor de destaque usada com parcimônia. Sem cartões preenchidos, sem sombras, sem fundo colorido. Hierarquia por tipografia, espaço em branco e filetes de 1px.

Corpo de texto em 19 a 20px com altura de linha generosa, títulos bem maiores, largura de leitura limitada. Tudo precisa funcionar em largura de celular, que é o próprio teste que o material prega.

O site respeita o tema do sistema apenas no sentido de não quebrar; o compromisso com fundo branco é deliberado e faz parte da mensagem.

## 6. Fora de escopo

- Sistema de contribuição de novos exemplos (por ora, e-mail de contato na página de créditos).
- Busca textual no conteúdo.
- Versão em PDF do site.
- Conversão de PPTX para PDF, desnecessária conforme verificação da seção 4.7.
- Análise automática de decks enviados pelo usuário.

## 7. Verificação antes de considerar pronto

1. `python3 build.py` termina sem aviso e é idempotente.
2. Um verificador percorre o HTML gerado e confirma que todo link interno resolve, que todo arquivo referenciado em `assets/` existe e que nenhuma imagem está sem `alt`.
3. As três versões têm o mesmo número de seções e de itens de checklist.
4. As 40 entradas da galeria e os 3 templates têm miniatura e pelo menos um formato baixável.
5. As páginas abrem corretamente em largura de 390px, sem rolagem horizontal.
6. Revisão do texto em português conforme as regras do projeto: sem travessão, sem quebra manual de linha, acentuação e gramática impecáveis. O mesmo padrão de qualidade se aplica ao inglês e ao espanhol.
7. Nenhum arquivo da galeria excede 100 MB, limite rígido do GitHub.

## 8. Riscos conhecidos

**Peso do repositório.** Cerca de 195 MB, o que torna o `git clone` lento. Fica dentro do recomendado pelo GitHub Pages (1 GB), mas se incomodar, o caminho é remover os PPTX mais pesados do repositório e publicá-los via GitHub Releases, sem mudar nada na estrutura do site: apenas a URL do formato muda em `gallery.json`.

**Tradução.** Português é a fonte; inglês e espanhol são traduções adaptadas, não literais. Nomes de trilha brasileiras (TP, SF, WTICG, WRSeg) recebem explicação no idioma de destino em vez de tradução forçada.

**Conteúdo de terceiros.** Os decks de 2026 são publicados com autorização do autor principal e crédito nominal. Se algum autor pedir remoção, basta retirar a entrada de `gallery.json` e os arquivos correspondentes, e regerar.
