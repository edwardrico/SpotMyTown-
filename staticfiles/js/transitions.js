$(document).ready(function () {
    // Au chargement de la page
    $('.fade-in').addClass('active');

    // Lors de la navigation vers une autre page
    $('.nav-link').click(function (e) {
        e.preventDefault();
        var targetPage = $(this).attr('href');
        $('.fade-in').removeClass('active');
        setTimeout(function () {
            window.location.href = targetPage;
        }, 500); // Attendez la fin de l'animation (500ms) avant de naviguer vers la nouvelle page
    });
});
