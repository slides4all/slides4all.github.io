/* Guarda a escolha manual de idioma, para que a raiz do site respeite a
   preferencia do visitante em vez de redetectar pelo navegador. */
(function () {
  Array.prototype.forEach.call(document.querySelectorAll('.lang a[lang]'), function (a) {
    a.addEventListener('click', function () {
      try {
        localStorage.setItem('s4a-lang', a.getAttribute('lang'));
      } catch (err) {
        /* sem persistencia: a navegacao continua normal */
      }
    });
  });
}());
