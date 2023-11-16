$(document).ready(function () {

    $(document).on('click', '#errorModal .close', function () {
        $('#errorModal').modal('hide');
    });

    $(document).on('submit', 'form', function () {
        var errorList = $('.modal-body ul');
        if (errorList.length > 0 && errorList.find('li').length > 0) {
            $('#errorModal').modal('show');
        }
    });
});