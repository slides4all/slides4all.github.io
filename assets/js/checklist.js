/* Checklist: marca, conta e guarda o progresso neste navegador.
   O armazenamento pode falhar (janela privativa, dados bloqueados), entao
   toda leitura e escrita e protegida e a pagina continua funcionando sem ele. */
(function () {
  var raiz = document.querySelector('.checklist');
  if (!raiz) { return; }

  var chave = 's4a-checklist-' + (document.documentElement.lang || 'pt');
  var caixas = Array.prototype.slice.call(raiz.querySelectorAll('input[data-ck]'));
  var total = caixas.length;
  var feitos = document.getElementById('ckDone');
  var barra = document.getElementById('ckFill');
  var pronto = document.getElementById('ckAllDone');
  var btnLimpar = document.getElementById('ckReset');
  var btnCopiar = document.getElementById('ckCopy');

  function ler() {
    try {
      var bruto = localStorage.getItem(chave);
      return bruto ? JSON.parse(bruto) : {};
    } catch (err) {
      return {};
    }
  }

  function gravar(estado) {
    try {
      localStorage.setItem(chave, JSON.stringify(estado));
    } catch (err) {
      /* sem persistencia: a pagina segue utilizavel */
    }
  }

  function atualizar() {
    var n = caixas.filter(function (c) { return c.checked; }).length;
    feitos.textContent = String(n);
    barra.style.width = total ? (n / total * 100) + '%' : '0';
    pronto.hidden = n !== total;
  }

  var estado = ler();
  caixas.forEach(function (c) {
    if (estado[c.getAttribute('data-ck')]) { c.checked = true; }
    c.addEventListener('change', function () {
      var atual = ler();
      if (c.checked) {
        atual[c.getAttribute('data-ck')] = 1;
      } else {
        delete atual[c.getAttribute('data-ck')];
      }
      gravar(atual);
      atualizar();
    });
  });
  atualizar();

  if (btnLimpar) {
    btnLimpar.addEventListener('click', function () {
      var pergunta = btnLimpar.getAttribute('data-confirm');
      if (pergunta && !window.confirm(pergunta)) { return; }
      caixas.forEach(function (c) { c.checked = false; });
      gravar({});
      atualizar();
    });
  }

  if (btnCopiar) {
    var rotulo = btnCopiar.textContent;
    btnCopiar.addEventListener('click', function () {
      var linhas = [];
      Array.prototype.forEach.call(raiz.querySelectorAll('.ck-group'), function (g) {
        linhas.push('');
        linhas.push(g.querySelector('h2').textContent);
        Array.prototype.forEach.call(g.querySelectorAll('label'), function (l) {
          var marcado = l.querySelector('input').checked;
          linhas.push((marcado ? '[x] ' : '[ ] ') + l.querySelector('span').textContent);
        });
      });
      var texto = linhas.join('\n').trim();
      function avisar() {
        btnCopiar.textContent = btnCopiar.getAttribute('data-copied') || rotulo;
        window.setTimeout(function () { btnCopiar.textContent = rotulo; }, 1600);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(texto).then(avisar, function () {});
      }
    });
  }
}());
