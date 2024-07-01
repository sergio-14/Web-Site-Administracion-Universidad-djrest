function loadForm(formFile) {
  const formContainer = document.getElementById('form-container');

  // Realiza una solicitud HTTP para obtener el contenido del formulario
  fetch(formFile)
    .then(response => response.text())
    .then(html => {
      formContainer.innerHTML = html;
    })
    .catch(error => console.error('Error al cargar el formulario:', error));
}