/* Calculadora de tempo: divide o slot em 30 / 15 / 45 / 10 por cento,
   estima o numero de slides e mostra as margens de 5% e 10%. */
(function () {
  var campo = document.getElementById('timingInput');
  if (!campo) { return; }

  var textos = document.getElementById('timingStrings');
  var MIN = textos.getAttribute('data-min');
  var SEG = textos.getAttribute('data-sec');
  var APROX = textos.getAttribute('data-around');

  var partes = { foundation: 30, problem: 15, contribution: 45, closing: 10 };

  function formatar(segundos) {
    var s = Math.round(segundos);
    if (s < 60) { return s + ' ' + SEG; }
    var m = Math.floor(s / 60);
    var r = s % 60;
    return r ? m + ' ' + MIN + ' ' + r + ' ' + SEG : m + ' ' + MIN;
  }

  function calcular() {
    var minutos = parseInt(campo.value, 10);
    if (!minutos || minutos < 1) { minutos = 0; }
    var segundos = minutos * 60;

    Object.keys(partes).forEach(function (nome) {
      var alvo = document.querySelector('[data-part="' + nome + '"]');
      if (alvo) {
        alvo.textContent = minutos ? formatar(segundos * partes[nome] / 100) : '-';
      }
    });

    var slides = document.getElementById('timingSlides');
    slides.textContent = minutos ? APROX + ' ' + minutos : '-';

    document.getElementById('timingTol5').textContent =
      minutos ? '± ' + formatar(segundos * 0.05) : '-';
    document.getElementById('timingTol10').textContent =
      minutos ? '± ' + formatar(segundos * 0.10) : '-';
  }

  campo.addEventListener('input', calcular);
  Array.prototype.forEach.call(document.querySelectorAll('.quick'), function (b) {
    b.addEventListener('click', function () {
      campo.value = b.getAttribute('data-min');
      calcular();
    });
  });
  calcular();
}());
