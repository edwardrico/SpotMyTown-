document.getElementById('settingsDropdown').addEventListener('click', function () {
    var dropdownMenu = document.querySelector('#settingsDropdown + .dropdown-menu');
    dropdownMenu.classList.toggle('show');
  });