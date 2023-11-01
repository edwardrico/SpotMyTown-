var changeSmileyButton = document.getElementById('changeSmileyButton');
var smileIcon = document.querySelector('.smile-icon');

changeSmileyButton.addEventListener('mouseover', function() {
    smileIcon.classList.remove('fa-frown');
    smileIcon.classList.add('fa-smile');

});

changeSmileyButton.addEventListener('mouseout', function() {
    smileIcon.classList.remove('fa-smile');
    smileIcon.classList.add('fa-frown');

});