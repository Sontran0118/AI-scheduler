import React, { useState } from 'react';

const PdfUpload = () => {
    const [file, setFile] = useState(null); // State to store the selected file

    const handleFileChange = (event) => {
        setFile(event.target.files[0]); // Update file state when user selects a file
    };

    const handleSubmit = async (event) => {
      event.preventDefault();
  
      if (!file) {
          alert("Please select a PDF file.");
          return;
      }
  
      const formData = new FormData();
      formData.append("file", file);
  
      try {
          const response = await fetch('http://127.0.0.1:5000/upload', {
              method: 'POST',
              body: formData,
          });
  
          if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
          }
  
          const data = await response.json();
          console.log("File processed successfully:", data);
      } catch (error) {
          console.error("Error uploading file:", error);
          alert("Error uploading the file. Please try again.");
      }
  };

    // Return JSX with file input and submit button
    return (
        <form onSubmit={handleSubmit}>
            <input
                type="file"
                id="pdf-upload"
                accept=".pdf"
                onChange={handleFileChange} // Trigger file change handler on selection
            />
            <button type="submit">Upload PDF</button>
        </form>
    );
};

export default PdfUpload;