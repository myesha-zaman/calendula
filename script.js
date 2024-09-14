// script.js
document.getElementById('file-upload').addEventListener('change', function() {
    const fileName = document.getElementById('file-upload').files[0].name;
    document.getElementById('file-name').textContent = fileName;
  });
  
  document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission
    
    const fileInput = document.getElementById('file-upload');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
  
    const uploadStatus = document.getElementById('upload-status');
    uploadStatus.innerHTML = 'Uploading...';
  
    // Send the file data to the server via AJAX (optional)
    fetch('/upload', {
      method: 'POST',
      body: formData
    })
    .then(response => response.text())
    .then(result => {
      uploadStatus.innerHTML = 'File uploaded successfully!';
    })
    .catch(error => {
      uploadStatus.innerHTML = 'Error uploading file.';
    });
  });
  