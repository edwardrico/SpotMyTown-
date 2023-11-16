document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
      const imagenPosts = form.querySelector('input[type="file"]');
      if (!imagenPosts.files.length) {
        event.preventDefault();
        alert('Ce champ est obligatoire. Vous devez fournir une image.');
      }
    });
  });