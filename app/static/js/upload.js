document.addEventListener('DOMContentLoaded', function() {
  const fileInput = document.getElementById('id_pdf_file');
  const fileNameDisplay = document.getElementById('file-name');

  if (fileInput && fileNameDisplay) {
    fileInput.addEventListener('change', function(e) {
      const fileName = e.target.files[0] ? e.target.files[0].name : 'Файл не выбран';
      fileNameDisplay.textContent = fileName;
    });
  }
});
