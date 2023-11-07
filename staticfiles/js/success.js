$(document).ready(function() {
    // Après 2 secondes (2000 millisecondes), affichez l'icône "check-circle" et masquez l'icône de chargement
    setTimeout(function() {
        $("#loading-container").hide();
        $("#success-container").show();
    }, 2000);
});

