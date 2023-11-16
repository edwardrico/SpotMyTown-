$(document).ready(function () {
    $('#infoModal').modal('show');

    $(document).on('click', '#infoModal .close', function () {
        $('#infoModal').modal('hide');
    });
});
