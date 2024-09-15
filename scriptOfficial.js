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
    fetch('http://127.0.0.1:5000/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.blob(); // Read the response as a blob
            })
            .then(blob => {
                // Create a link element, use it to download the file
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = 'schedule.ics'; // Suggested name for the downloaded file
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                uploadStatus.innerHTML = 'File uploaded and downloaded successfully!';
            })
            .catch(error => {
                uploadStatus.innerHTML = 'Error uploading file.';
                console.error('Error:', error);
            });
  });
  