/* Filtros da galeria. A lista inteira ja vem no HTML: sem JavaScript a
   galeria continua completa e legivel, apenas sem filtro. */
(function () {
  var lista = document.getElementById('galleryList');
  if (!lista) { return; }

  var itens = Array.prototype.slice.call(lista.querySelectorAll('.item'));
  var vazio = document.getElementById('galleryEmpty');
  var contador = document.getElementById('galleryShown');
  var ativos = { event: '', track: '' };

  function aplicar() {
    var n = 0;
    itens.forEach(function (li) {
      var ok = (!ativos.event || li.getAttribute('data-event') === ativos.event) &&
               (!ativos.track || li.getAttribute('data-track') === ativos.track);
      li.hidden = !ok;
      if (ok) { n += 1; }
    });
    contador.textContent = String(n);
    vazio.hidden = n !== 0;
  }

  Array.prototype.forEach.call(document.querySelectorAll('.chip'), function (chip) {
    chip.addEventListener('click', function () {
      var tipo = chip.getAttribute('data-filter');
      ativos[tipo] = chip.getAttribute('data-value');
      Array.prototype.forEach.call(
        document.querySelectorAll('.chip[data-filter="' + tipo + '"]'),
        function (outro) { outro.classList.remove('is-on'); });
      chip.classList.add('is-on');
      aplicar();
    });
  });
}());
