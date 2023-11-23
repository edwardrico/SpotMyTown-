document.addEventListener("DOMContentLoaded", function () {
    var prevScrollpos = window.pageYOffset;
    var navbar = document.getElementById("mainNavigation");

    window.onscroll = function () {
      var currentScrollPos = window.pageYOffset;

      // Si el scroll es hacia abajo y no estás en la parte superior de la página, oculta la barra de navegación
      if (prevScrollpos < currentScrollPos && currentScrollPos > 0) {
        navbar.classList.add("hidden");
      } else {
        // Si el scroll es hacia arriba o estás en la parte superior de la página, muestra la barra de navegación
        navbar.classList.remove("hidden");
      }

      // Si llegas al final de la página, muestra la barra de navegación
      if (
        window.innerHeight + currentScrollPos >=
        document.body.offsetHeight
      ) {
        navbar.classList.remove("hidden");
      }

      prevScrollpos = currentScrollPos;
    };
  });