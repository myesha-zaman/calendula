document.getElementById('file-upload').addEventListener('change', function() {
    const fileInput = document.getElementById('file-upload');
    const fileName = fileInput.files.length > 0 ? fileInput.files[0].name : 'No file chosen';
    document.getElementById('file-name').textContent = fileName;
  });
  
  document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission
  
    const fileInput = document.getElementById('file-upload');
    const file = fileInput.files[0];
    
    if (!file) {
      // No file selected
      document.getElementById('upload-status').innerHTML = 'Please choose a file to upload.';
      return;
    }
  
    const formData = new FormData();
    formData.append('file', file);
  
    const uploadStatus = document.getElementById('upload-status');
    uploadStatus.innerHTML = 'Uploading...';
  
    // Send the file data to the server via AJAX
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
  