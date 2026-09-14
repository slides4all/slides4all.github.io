---
name: slides4all
description: Use ao criar, revisar ou refazer slides de uma apresentação técnica ou científica (artigo aceito, salão de ferramentas, iniciação científica, defesa, palestra, aula, demonstração). Conduz o processo inteiro: entrevista de insumos, plano do deck, redação em formato de manchete, geração do arquivo em PPTX, LaTeX Beamer ou HTML, e auditoria final contra o checklist do Slides4All. Acione também quando o pedido for "melhore estes slides", "reduza para X minutos" ou "prepare a apresentação deste artigo".
license: Livre uso. Copie, adapte, traduza e reaproveite.
source: https://slides4all.github.io
---

# Slides4All: construção de apresentações técnicas

Skill destinada a modelos de linguagem avançados com capacidade de executar código e manipular arquivos. Destila o material de https://slides4all.github.io, que nasceu das sugestões para apresentações do SBSeg 2024 e de dezenas de revisões de decks reais, uma a uma.

O objetivo de uma apresentação é um só: a plateia precisa entender o seu argumento e a sua linha de raciocínio. Se ao final ela não entendeu, a apresentação falhou, por melhor que seja o trabalho por trás dela. Toda decisão desta skill serve a isso.

## 0. Como usar esta skill

Em Claude Code ou em qualquer agente compatível com Agent Skills, salve este arquivo como `~/.claude/skills/slides4all/SKILL.md` e a skill passa a ser acionada sozinha pelo `description` acima. Em ChatGPT, Gemini, Copilot ou similares, cole o arquivo inteiro como instrução de sistema, como arquivo de projeto ou como primeira mensagem. O conteúdo é autocontido: não depende de acesso à internet.

Se o ambiente permitir execução de código, prefira sempre gerar o arquivo de fato (PPTX, PDF via LaTeX, ou HTML) e rodar a auditoria automática da seção 11. Se não permitir, entregue o plano da seção 5 mais o texto slide a slide, em formato que a pessoa cole no PowerPoint, Keynote, Google Slides ou Beamer.

## 1. As sete regras inegociáveis

Estas valem sempre, em qualquer evento, qualquer idioma, qualquer template. Se qualquer instrução posterior conflitar com elas, elas vencem.

1. Fonte grande. Mínimo de 24pt em qualquer conteúdo de slide, incluindo texto dentro de imagens, tabelas, gráficos e legendas. Mínimo de 32pt nos títulos. É o problema mais recorrente de todas as revisões, de longe.
2. Quando o conteúdo não couber com fonte grande, corte o conteúdo. Nunca diminua a fonte para caber. Prefira menos itens, frases mais curtas e mais slides a um slide denso com letra pequena.
3. Fundo branco, texto preto. Sem cinza, sem colorido atrás de texto, sem caixas preenchidas. A cor entra só para destacar um dado ou diferenciar séries em um gráfico.
4. Figuras ocupam o máximo de espaço possível. Figura complexa pode e deve usar 100% do slide, inclusive por cima de título e rodapé.
5. Slide não é texto corrido. Nada de transcrever frases ou parágrafos do artigo. Itens curtos, em formato de manchete, que guiam a fala.
6. Um idioma só, do primeiro ao último slide, inclusive em rótulos de eixos, cabeçalhos de tabela e legendas.
7. O tempo é do evento, não seu. O deck precisa caber no slot, com a divisão da seção 6.

Teste de aceitação de tudo isso: o teste do celular. Abra o deck no telefone, a uns 50 cm dos olhos. O que você não conseguir ler sem esforço, a plateia no fundo da sala também não vai. Sempre que estiver em dúvida sobre um slide, aplique este teste mentalmente e decida a favor do corte.

## 2. Insumos que você deve reunir antes de começar

Pergunte apenas o que não conseguir deduzir dos arquivos que receber. Faça as perguntas de uma vez só, em uma única mensagem, e siga com valores padrão quando a pessoa não responder tudo.

1. Qual é o trabalho: artigo, ferramenta, resumo de iniciação científica, defesa, aula, demonstração. Peça o PDF, o `.tex` ou o texto.
2. Quantos minutos de slot, e se o tempo de perguntas está dentro ou fora dele. Padrão quando não informado: 20 minutos com perguntas à parte.
3. Qual evento, trilha e idioma da apresentação. Padrão: o idioma do artigo.
4. Quem apresenta, quem são os coautores, quais instituições e agências de fomento aparecem na capa.
5. Existe template obrigatório do evento. Se sim, peça o arquivo. Se não, use a especificação visual da seção 9.
6. Qual é a única frase que a plateia precisa levar embora. Se a pessoa não souber responder, ajude a formular: é a tese do deck, e todo o resto se subordina a ela.

Nunca invente números, resultados, nomes de autores, afiliações ou referências. Se um dado necessário não estiver nos insumos, deixe um marcador explícito no slide, como `[[FALTA: ganho médio em %]]`, e liste todos os marcadores no relatório final de entrega.

## 3. O processo, em sete etapas

Execute nesta ordem e mostre o resultado de cada etapa antes de seguir para a próxima quando a pessoa estiver acompanhando. As etapas 1 a 4 são de texto e custam pouco: é ali que a apresentação fica boa ou ruim. A etapa 5 é mecânica.

1. Leia os insumos e extraia: problema, desafios técnicos, lacuna na literatura, abordagem, figura de pipeline ou arquitetura, resultados principais, limitações, trabalhos futuros.
2. Escreva a tese em uma frase e as três a cinco mensagens que a sustentam. Descarte tudo o que não sustentar a tese, por mais interessante que seja.
3. Calcule o orçamento de tempo e de slides pela seção 6.
4. Monte o plano do deck no formato da seção 5, slide a slide, com título em manchete e conteúdo já redigido. Revise o plano contra as regras da seção 1 antes de gerar qualquer arquivo.
5. Gere o artefato pela seção 10.
6. Rode a auditoria automática da seção 11 e corrija tudo o que ela apontar. Repita até a auditoria passar limpa.
7. Passe o checklist da seção 12 e entregue o relatório da seção 13.

## 4. A coluna vertebral de uma apresentação técnica

Esta sequência vem dos decks reais da galeria do Slides4All e funciona para artigo completo, ferramenta e iniciação científica. Adapte, não siga cegamente.

1. Capa: título do trabalho, autores, instituições, evento e data. Logomarcas grandes, de verdade: elas ficam no ar enquanto você é apresentado, e quase sempre estão pequenas demais para serem reconhecidas.
2. O problema, já no segundo slide. Não abra com roteiro nem com contexto longo: abra com o problema ou com uma motivação forte. A apresentação fica muito mais envolvente.
3. Desafios técnicos, em um a três slides. É aqui que a plateia decide se o trabalho interessa, e é justamente a parte que mais costuma ficar sem tempo. Detalhe tecnicamente.
4. O que já existe e o que falta: a tabela de trabalhos relacionados, construída para evidenciar a lacuna, nunca para listar trabalhos. Não gaste muito tempo aqui.
5. Divisor numerado com a tese da parte, no padrão `01`, `02`, `03`, acompanhado de uma frase que afirma alguma coisa. Divisor é barato, orienta a plateia e dá respiro à fala.
6. A abordagem, começando pela figura de arquitetura ou de pipeline inteira, seguida da construção progressiva: um slide por etapa, acrescentando um elemento de cada vez, sempre destacando com retângulo, círculo ou seta a parte que está sendo explicada. Todo experimento tem um pipeline: mostre essa figura, ela explica melhor que qualquer lista.
7. Avaliação: o testbed ou protocolo experimental, depois os resultados, um argumento por slide.
8. O que os resultados sustentam e o que ainda não podemos afirmar. Dois slides que valem ouro na sessão de perguntas e que demonstram maturidade científica.
9. Conclusões: o que o trabalho entrega, em uma frase por contribuição, e trabalhos futuros.
10. Artefatos, selos, repositório e dados abertos, quando houver.
11. Agradecimentos e contato, com "perguntas são bem-vindas" e o e-mail do autor de contato legível de longe.
12. Slides de reserva, depois do slide final: respostas para as perguntas prováveis da banca, tabelas completas, detalhes de parâmetros, provas. Você não os mostra, mas eles salvam a discussão.

## 5. O plano do deck, em YAML

Produza sempre esta representação intermediária antes de gerar qualquer arquivo. Ela é curta, revisável e verificável por programa, e evita retrabalho caro em PPTX.

```yaml
deck:
  titulo: "Título do trabalho"
  autores: "Nome Um, Nome Dois, Nome Três"
  instituicoes: "Instituição A, Instituição B"
  evento: "SBSeg 2026"
  idioma: pt
  minutos: 20
  tese: "A regra só merece confiança depois de enfrentar tráfego adversarial."
slides:
  - n: 1
    tipo: capa
    titulo: "Título do trabalho"
    notas: "Fala de abertura, 20 s."
  - n: 2
    tipo: manchete
    kicker: "ABERTURA"
    titulo: "Regras de IDS plausíveis na sintaxe ainda falham no tráfego real"
    itens:
      - "Sintaxe válida não é detecção"
      - "Protocolos emergentes sem assinatura pronta"
    minutos: 1.0
  - n: 6
    tipo: figura
    titulo: "A arquitetura do Rules Farmer"
    figura: "figuras/arquitetura.svg"
    ocupa_slide_inteiro: true
    progressivo: "1 de 4"
    minutos: 1.5
  - n: 14
    tipo: tabela
    kicker: "02 · AVALIAÇÃO EXPERIMENTAL"
    titulo: "A validação ao vivo convergiu nos quatro cenários"
    colunas: ["Cenário", "Execuções", "Convergiu"]
    linhas:
      - ["A", "42", "Sim"]
    destaque_linha: 1
    minutos: 1.0
  - n: 21
    tipo: contato
    titulo: "Obrigado! Perguntas são bem-vindas"
    contato: "nome@instituicao.br"
```

Tipos previstos: `capa`, `divisor`, `manchete`, `figura`, `tabela`, `grafico`, `citacao`, `contato`, `reserva`. A soma dos campos `minutos` precisa bater com o orçamento da seção 6, com tolerância de 5%. Verifique isso antes de gerar o arquivo.

## 6. Orçamento de tempo e de slides

Divisão sugerida do tempo total, validada em muitas apresentações. A plateia veio pelo problema e pela sua solução: fundamentação longa consome exatamente o tempo de que essas duas partes precisam.

| Parte | Fatia | Em 15 min | Em 20 min | Em 30 min |
| --- | --- | --- | --- | --- |
| Fundamentação, só o necessário para situar | 10% | 1,5 min | 2 min | 3 min |
| Problema e desafios, com detalhamento técnico | 25% | 3,75 min | 5 min | 7,5 min |
| Solução e resultados, com limitações | 55% | 8,25 min | 11 min | 16,5 min |
| Considerações finais e agradecimentos | 10% | 1,5 min | 2 min | 3 min |

Quantidade de slides: um slide por minuto é uma boa regra de bolso, mais precisa em apresentações curtas do que em longas. Contam aqui apenas os slides que serão mostrados, não os de reserva. Divisores e slides de construção progressiva consomem pouco tempo, então um deck progressivo bem feito costuma ter de 1,2 a 1,8 slide por minuto sem estourar.

Tolerância: meta de 5% para mais ou para menos nos ensaios, sem contar perguntas. Limite absoluto de 10% no momento da apresentação. Passar disso obriga o presidente da sessão a interromper. Terminar muito antes também é ruim: desperdiça um tempo de ouro e sugere que não havia o que explicar.

Regra de densidade: se a fala em um mesmo slide passa de dois minutos, aquele slide tem conteúdo demais e deveria virar dois ou três.

## 7. Redação dos slides: a técnica da manchete

A forma mais simples de passar o conteúdo é escrever como manchete de jornal e deixar a explicação completa para a fala.

| Frase de artigo | Manchete de slide |
| --- | --- |
| O novo sistema XPTO desenvolvido neste trabalho teve um desempenho que superou em 30% a melhor versão da literatura. | XPTO: desempenho 30% superior ao estado da arte |
| Os resultados indicam que o balanceamento não é universalmente benéfico, uma vez que seu efeito depende das características dos dados. | Balancear ajudou em 7 dos 11 datasets, prejudicou em 4 |
| Nesta seção apresentamos a avaliação experimental conduzida em quatro cenários distintos. | 167 execuções, 4 cenários |

Regras de escrita que se aplicam a todo texto do deck.

1. Título de slide afirma alguma coisa. `Resultados` não diz nada; `A proposta supera a base em toda a faixa` diz. O título carrega a conclusão, a figura mostra a evidência.
2. Itens curtos e diretos, que servem de guia para a fala. Evite sentenças completas com sujeito, verbo, objeto e complementos: isso é para texto, não para slide.
3. No máximo 4 itens por slide, no máximo 10 palavras por item. Estourou, vira dois slides.
4. Sem palavras fortes sem evidência: comprovado, garantido, irrefutável, definitivo. Existe prova matemática formal? Se não, troque a palavra por o que os dados sustentam.
5. Sem números decorativos do tipo `01`, `02`, `03` dentro de caixas de contribuição. O número ocupa o espaço mais nobre sem dizer nada. Use o espaço para a palavra-chave da contribuição, em fonte maior.
6. Sem bloco de texto ao lado de gráfico. A plateia tenta ler e olhar ao mesmo tempo e não faz nem uma coisa nem outra. O texto vira fala, ou vira um slide próprio.
7. Idioma padronizado. Nada de "feature com ALTA variância". Se o deck é em português, é `característica`, `limiar`, `acurácia`, `revocação`.
8. Abreviação consistente. Ou abrevia tudo, ou não abrevia nada, em todos os slides.
9. Nunca use travessão no texto dos slides. Use vírgula, dois-pontos, parênteses ou ponto.

## 8. Figuras, tabelas e gráficos

Figuras.

1. Prioridade máxima é a boa visualização da figura, não preservar o enquadramento do template.
2. Formato vetorial sempre que possível: SVG, PDF, EPS. PNG grande serve. Recorte de tela é a pior alternativa: se ao dar zoom aparecer borrão ou quadriculado, a figura precisa ser refeita.
3. Figura complexa é apresentada progressivamente, em vários slides, uma etapa por vez. Se a figura mostra arquitetura, etapas ou fluxo e você vai falar de cada parte, faça um slide por parte.
4. Destaque com retângulo, círculo ou seta a parte que está sendo explicada naquele momento. Cor de destaque única, sempre a mesma ao longo do deck.
5. Remova figuras decorativas. Entre manter uma figura secundária e aumentar a fonte, aumente a fonte.
6. Muito espaço em branco sobrando quase sempre significa que a figura ou a fonte poderiam estar maiores.

Gráficos.

1. Rótulos de eixo, legendas e valores em 24pt ou mais. Gráfico gerado por matplotlib ou similar precisa ser regerado com fonte grande, não ampliado depois.
2. Sem grade pesada, sem fundo colorido, sem efeito 3D, sem sombra.
3. Série destacada em cor, demais séries em cinza. Cor só onde ela carrega informação.
4. O título do slide já entrega a leitura do gráfico, para que a plateia não precise interpretá-lo sozinha.

Tabelas.

1. Tabela do artigo foi feita para ser lida a 30 cm, no papel, com tempo. No slide ela vira uma mancha cinza. Refaça a tabela para o slide.
2. Menos colunas, menos linhas, fonte grande no conteúdo e não só no cabeçalho. Nem sempre é preciso mostrar a tabela inteira, nem todas as tabelas do artigo. Explicar bem os dados importantes vale mais do que passar por tudo correndo.
3. Cabeçalho sem quebra de linha estranha: é o defeito mais comum.
4. Exiba progressivamente, destacando a linha ou coluna que está sendo explicada.

A tabela de trabalhos relacionados merece regra própria, porque é a mais malfeita de todas. Ela não serve para listar trabalhos: serve para deixar evidente a lacuna que o seu trabalho preenche. Escolha as colunas a partir do foco do seu trabalho. Se você avalia técnicas de balanceamento, as colunas são quais técnicas cada trabalho usou e em que tipo de dado, e a última coluna é a lacuna que permanece. A última linha é o seu trabalho, com a lacuna vazia. Quando a tabela aparece logo depois do problema e dos desafios, o melhor título é `O que já existe e o que falta`.

## 9. Especificação visual padrão

Use quando não houver template obrigatório do evento. Quando houver, mantenha a identidade do template mas aplique tipografia e fundo desta especificação, e nunca deixe o template impedir que uma figura ocupe o slide inteiro.

| Elemento | Valor |
| --- | --- |
| Proporção | 16:9, 33,87 cm por 19,05 cm, ou 13,333 por 7,5 polegadas |
| Fundo | Branco puro, em todos os slides, sem exceção |
| Texto | Preto ou cinza muito escuro, por exemplo `#111111` |
| Título de slide | 32pt a 44pt, peso semibold ou bold |
| Corpo, itens, células de tabela | 24pt no mínimo, 28pt preferencial |
| Etiqueta superior, do tipo `02 · AVALIAÇÃO` | 16pt a 18pt, maiúsculas, cinza médio |
| Rodapé e numeração de slide | 14pt a 16pt, cinza médio |
| Número de destaque, do tipo `7 / 11` | 80pt a 140pt |
| Tipografia | Uma família só, sem serifa, de boa legibilidade projetada: Inter, Source Sans, Lato, Calibri, Helvetica |
| Cor de destaque | Uma só, usada com parcimônia, com contraste mínimo de 4,5:1 sobre branco |
| Margens | 4% da largura em cada lado, respeitadas por todo elemento de texto |
| Numeração | Presente em todos os slides, exceto capa. Ajuda a plateia a anotar e a direcionar perguntas, e ajuda você a controlar o tempo |

Título em todo slide é recomendável, mas não é obrigatório: às vezes aumentar a imagem vale mais do que colocar um título.

## 10. Geração do artefato

### PPTX com python-pptx

Recomendado quando a pessoa vai editar depois, que é o caso mais comum. Constantes a fixar no início do script, para que nenhuma decisão de tamanho fique dispersa pelo código.

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

LARGURA, ALTURA = Inches(13.333), Inches(7.5)   # 16:9
MARGEM = Inches(0.55)
PRETO, CINZA, DESTAQUE = RGBColor(0x11, 0x11, 0x11), RGBColor(0x66, 0x66, 0x66), RGBColor(0xC0, 0x39, 0x2B)
TITULO, CORPO, ETIQUETA, RODAPE = Pt(36), Pt(28), Pt(18), Pt(14)
MINIMO_CONTEUDO = Pt(24)   # piso absoluto, a auditoria da secao 11 falha abaixo disso

prs = Presentation()
prs.slide_width, prs.slide_height = LARGURA, ALTURA
branco = prs.slide_layouts[6]   # layout em branco, o unico que nao atrapalha
```

Cuidados que evitam os erros mais comuns com python-pptx.

1. Use sempre o layout em branco e posicione tudo você mesmo. Os placeholders do template padrão trazem tamanhos pequenos herdados e são a causa número um de fonte minúscula sem você perceber.
2. Defina `run.font.size` explicitamente em todo run, inclusive nas células de tabela. Tamanho `None` significa herdado, e o herdado quase sempre é pequeno demais.
3. Desligue o autoajuste que encolhe texto: `tf.word_wrap = True` e nunca `MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE`. Encolher para caber é exatamente o que a regra 2 da seção 1 proíbe. Se não coube, corte texto.
4. Fundo branco explícito por slide, não confie no tema.
5. Para figura que ocupa o slide inteiro, insira a imagem em `(0, 0)` com largura igual à do slide e deixe que ela cubra título e rodapé.
6. Tabela: defina o tamanho da fonte célula a célula, percorrendo `cell.text_frame.paragraphs[*].runs[*]`, e aumente a altura das linhas em vez de reduzir a fonte.
7. Numere os slides escrevendo uma caixa de texto no canto, porque a numeração automática depende do layout.

### LaTeX Beamer

Recomendado quando o trabalho já está em LaTeX e há muita fórmula. Use `\documentclass[aspectratio=169,14pt]{beamer}`, tema limpo com fundo branco, `\setbeamercolor{background canvas}{bg=white}`, e desative sombras e gradientes. Para figura de slide inteiro, use `\begin{frame}[plain]` com `\includegraphics[width=\paperwidth]`. Construção progressiva sai natural com `\pause`, `\onslide<2->` e `\includegraphics` de versões sucessivas da figura. Confira o PDF final com `pdftoppm` e olhe as miniaturas: o teste do celular vale igual.

### HTML

Recomendado para demonstração ao vivo ou publicação na web. Página única, CSS próprio, sem framework pesado. Fixe `font-size` em unidades relativas a `vw` para que a escala acompanhe a tela, com piso equivalente a 24pt em 1920 por 1080. Fundo branco, uma cor de destaque, transição simples. Exporte para PDF antes de apresentar: em sala, o PDF nunca falha, o navegador às vezes sim.

## 11. Auditoria automática do resultado

Rode sempre que o ambiente permitir executar código, antes de entregar. Este script verifica no PPTX gerado o que mais aparece nas revisões. Ele não substitui o checklist da seção 12, que cobre o que só humano avalia.

```python
"""Audita um .pptx contra as regras do Slides4All.  Uso: python3 audita.py deck.pptx"""
import sys
from pptx import Presentation
from pptx.util import Pt
from pptx.enum.shapes import MSO_SHAPE_TYPE

MINIMO_CONTEUDO = Pt(24)   # piso de fonte no conteudo do slide
MINIMO_ETIQUETA = Pt(14)   # piso para etiqueta, rodape e numero de slide
BANDA = 0.12               # faixa superior e inferior onde etiqueta e rodape sao aceitos
DPI_MINIMO = 110           # resolucao efetiva aceitavel na projecao
problemas, avisos = [], []


def secundario(sh, texto, alt):
    """Etiqueta, rodape ou numero de slide: texto curto, colado no topo ou no rodape."""
    if len(texto) > 60 or sh.top is None:
        return False
    meio = sh.top + (sh.height or 0) / 2
    return meio < alt * BANDA or meio > alt * (1 - BANDA)


def conferir(tf, sh, onde, alt, dentro_de_tabela=False):
    for par in tf.paragraphs:
        for run in par.runs:
            txt = run.text.strip()
            if not txt:
                continue
            rotulo = "%s%s" % (onde, ", tabela" if dentro_de_tabela else "")
            if run.font.size is None:
                problemas.append("%s: fonte herdada, defina o tamanho: %r" % (rotulo, txt[:40]))
            elif not dentro_de_tabela and secundario(sh, txt, alt):
                if run.font.size < MINIMO_ETIQUETA:
                    avisos.append("%s: etiqueta ou rodape a %.0fpt: %r" % (rotulo, run.font.size.pt, txt[:40]))
            elif run.font.size < MINIMO_CONTEUDO:
                problemas.append("%s: fonte %.0fpt, abaixo de %.0fpt: %r"
                                 % (rotulo, run.font.size.pt, MINIMO_CONTEUDO.pt, txt[:40]))


prs = Presentation(sys.argv[1])
larg, alt = prs.slide_width, prs.slide_height

for i, slide in enumerate(prs.slides, 1):
    onde = "slide %d" % i
    for sh in slide.shapes:
        if sh.has_text_frame:
            conferir(sh.text_frame, sh, onde, alt)
            if sh.left is not None and sh.text_frame.text.strip():
                if sh.left < 0 or sh.top < 0 or sh.left + sh.width > larg or sh.top + sh.height > alt:
                    problemas.append("%s: caixa de texto vazando da area do slide" % onde)
        if getattr(sh, "has_table", False):
            for linha in sh.table.rows:
                for cel in linha.cells:
                    conferir(cel.text_frame, sh, onde, alt, dentro_de_tabela=True)
        if sh.shape_type == MSO_SHAPE_TYPE.PICTURE and sh.width:
            dpi = sh.image.size[0] / (sh.width / 914400.0)
            if dpi < DPI_MINIMO:
                avisos.append("%s: imagem a %.0f dpi efetivos, risco de borrao" % (onde, dpi))

print("%d slides" % len(prs.slides._sldIdLst))
for a in avisos:
    print("aviso     %s" % a)
for p in problemas:
    print("PROBLEMA  %s" % p)
print("%d problema(s), %d aviso(s)" % (len(problemas), len(avisos)))
```

Verificações complementares, que valem a pena fazer mesmo sem script.

1. Exporte para PDF, gere miniaturas com `pdftoppm -r 40` e olhe a folha de contatos inteira. Slide que vira mancha cinza na miniatura tem texto demais.
2. Reduza o PDF a 15% da tela e confirme que os títulos ainda se distinguem. É a aproximação mais honesta do teste do celular.
3. Conte os slides e compare com os minutos do slot.
4. Procure a palavra do idioma errado: um `accuracy` perdido em deck português, um `limiar` perdido em deck inglês.

## 12. Checklist de revisão, em oito blocos

Passe item a item, no deck final. É o mesmo checklist publicado em https://slides4all.github.io, reproduzido aqui para uso offline.

**1. Teste do celular, faça primeiro**
- [ ] Abri o deck no celular, a uns 50 cm, e consegui ler tudo sem esforço.
- [ ] Identifiquei o slide mais problemático e corrigi os principais problemas.

**2. Fontes**
- [ ] Não há fonte pequena no corpo dos slides.
- [ ] Não há fonte pequena em tabelas.
- [ ] Não há fonte pequena em gráficos ou legendas.
- [ ] Não há fonte pequena em caixas de texto laterais.
- [ ] Quando faltou espaço, cortei conteúdo em vez de reduzir a fonte.

**3. Figuras e gráficos**
- [ ] Cada figura ocupa o máximo de espaço possível.
- [ ] Figuras complexas usam o slide inteiro, mesmo que seja necessário sobrepor título ou rodapé.
- [ ] Figuras de fluxo com várias etapas foram divididas em slides progressivos.
- [ ] A abordagem possui uma figura de pipeline ou fluxograma.
- [ ] Removi figuras decorativas que ocupavam espaço sem acrescentar informação.

**4. Texto**
- [ ] Substituí frases longas por itens curtos e objetivos.
- [ ] Não há bloco de texto competindo visualmente com um gráfico ou figura.
- [ ] Não há palavras fortes sem evidência, como comprovado, garantido ou irrefutável.
- [ ] O idioma está padronizado.
- [ ] Removi números decorativos das caixas.
- [ ] Destaquei visualmente as palavras-chave.

**5. Visual**
- [ ] O fundo é branco em todos os slides.
- [ ] Não há fundo cinza ou colorido atrás de textos.
- [ ] Nenhum texto está encostado ou vazando das bordas das caixas.
- [ ] As logomarcas do primeiro slide estão suficientemente grandes e legíveis.

**6. Consistência**
- [ ] Elementos do mesmo nível usam a mesma fonte.
- [ ] Os mesmos tipos de elementos usam as mesmas cores.
- [ ] Mantive o mesmo padrão de alinhamento e espaçamento.
- [ ] As abreviações estão padronizadas.

**7. Tabelas**
- [ ] Os cabeçalhos não apresentam quebras de linha estranhas.
- [ ] A fonte do conteúdo está grande o suficiente para leitura no celular.
- [ ] A tabela de trabalhos relacionados evidencia a lacuna de pesquisa, e não apenas lista trabalhos.
- [ ] Quando a tabela aparece no início da apresentação, o título é o que já existe e o que falta.

**8. Antes de enviar**
- [ ] Passei por todos os slides, um por um.
- [ ] O título de cada slide corresponde claramente ao conteúdo apresentado.
- [ ] Pedi para alguém que não participou da elaboração do deck revisar os slides no celular.
- [ ] Ensaiei pelo menos cinco vezes, em pé, falando alto e cronometrando.

Perguntas de consistência que pegam quase todos os deslizes restantes: por que um termo está abreviado e outro do mesmo tipo não; por que um nome está em português e outro em inglês; por que uma fonte está maior que outra para elementos do mesmo nível; por que os mesmos elementos usam cores diferentes em slides diferentes; por que há diferença de alinhamento, espaçamento, tamanho ou estilo entre elementos equivalentes.

## 13. O que entregar ao final

Entregue, sempre, nesta ordem.

1. O arquivo gerado, com o caminho, e o PDF exportado quando possível.
2. O mapa do deck: número do slide, título e minutos previstos, em tabela, com o total e a comparação com o slot.
3. A lista de marcadores `[[FALTA: ...]]` que restaram, se houver.
4. O resultado da auditoria da seção 11, honestamente, mesmo quando encontrou problemas que você não conseguiu resolver.
5. As decisões editoriais que você tomou por conta própria: o que cortou, o que fundiu, o que moveu para slides de reserva. A pessoa precisa poder discordar.
6. Um lembrete de ensaio: cinco vezes, em pé, falando alto, cronometrando. A experiência mostra que só a partir do quinto ou sexto ensaio o discurso fica fluido, bem organizado e sem redundância. A plateia percebe quando não houve ensaio, e os sinais são sempre os mesmos: gaguejar, repetir o que já foi dito, não passar a mensagem principal no tempo, ser interrompido, ficar sem tempo para as perguntas, que estão entre os maiores benefícios de apresentar.

## 14. Erros comuns, com a correção

| Erro | Por que é grave | Correção |
| --- | --- | --- |
| Fonte pequena no conteúdo | Na sala grande, quem está no fundo simplesmente não lê | 24pt ou mais; se não couber, corte itens, nunca a fonte |
| Fundo cinza ou colorido | Reduz contraste e cansa a vista, e projetores variam muito mais do que a sua tela | Fundo branco, texto preto, cor só para destacar um dado |
| Bloco de texto ao lado do gráfico | A plateia tenta ler e olhar ao mesmo tempo e não faz nem uma coisa nem outra | Gráfico grande sozinho no slide, o texto vira fala |
| Figura pequena com espaço sobrando | Espaço em branco sobrando significa figura que poderia estar maior | Amplie até o limite do slide, ou ocupe 100% dele |
| Figura complexa num slide só | Enquanto você explica a etapa 1, metade da plateia decifra a etapa 4 | Quebre em vários slides, uma etapa por vez |
| Números decorativos nas caixas | O número grande ocupa o espaço mais nobre sem dizer nada | Use o espaço para a palavra-chave da contribuição |
| Texto encostando ou vazando da borda | Fica visivelmente desleixado e no projetor a última linha às vezes some | Respiro dentro da caixa, confira todas as bordas |
| Português e inglês misturados | A troca de idioma no meio da frase trava a leitura | Um idioma só, inclusive em rótulos e cabeçalhos |
| Abreviação inconsistente | A plateia procura significado na diferença e não há nenhum | Ou abrevia tudo, ou não abrevia nada |
| Tabela copiada do artigo | Feita para ser lida no papel, a 30 cm, com tempo | Refaça para o slide: menos colunas, menos linhas, fonte grande |
| Trabalhos relacionados que só listam | Listar não diz nada, a plateia precisa ver a lacuna | Colunas escolhidas pelo seu foco, lacuna visível, seu trabalho na última linha |
| Logomarca minúscula no primeiro slide | O slide fica no ar enquanto você é apresentado e ninguém identifica nada | Aumente bastante as logomarcas da capa |
| Roteiro como primeiro slide de conteúdo | Gasta o momento de maior atenção com informação de baixo valor | Abra com o problema ou com uma motivação forte |
| Fundamentação longa | Consome justamente o tempo de que problema e solução precisam | 10% do tempo, só o necessário para situar o trabalho |

## 15. Limites

Não invente dados, resultados, referências, afiliações nem financiamentos. Não altere números vindos do artigo, nem para arredondar. Não transforme um resultado condicional em afirmação categórica: se o artigo diz que ajudou em 7 de 11 datasets, o slide diz isso, e não que o método funciona. Não use deck da galeria do Slides4All como exemplo negativo: os exemplos são publicados com autorização e com crédito nominal aos autores.

---

Derivado do material de https://slides4all.github.io, que por sua vez vem das sugestões para apresentações do SBSeg 2024 e das revisões, da síntese de sugestões e do checklist produzidos desde então. Conteúdo de livre uso: copie, adapte, traduza e reaproveite.
