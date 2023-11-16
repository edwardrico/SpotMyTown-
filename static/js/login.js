
$(document).ready(function () {

    $(document).on('click', '#errorPopup .close', function () {
        $('#errorPopup').modal('hide');
    });

    var errorList = $('.modal-body ul');
    if (errorList.length > 0 && errorList.find('li').length > 0) {
        $('#errorPopup').modal('show');
    }
});

