import React from "react";
import api from "../api"; // Import the Axios instance
import "../styles/File.css";

function File({ file, onDelete }) {
  const formattedDate = new Date(file.created_at).toLocaleDateString("en-US");

  // Function to handle file download
  const handleDownload = async () => {
    try {
      // Make a GET request to the file download endpoint
      const response = await api.get(`/api/files/${file.id}/download`, {
        responseType: "blob", // Set response type to blob
      });

      console.log(response.headers)
      // Get the file name from the header
      const contentDisposition = response.headers["content-disposition"];
      console.log("Content-Disposition:", contentDisposition);
      const filenameRegex = /filename=["']?([^"']+)/;

      const matches = filenameRegex.exec(contentDisposition);
      console.log("Matches:", matches);

      let filename = "downloaded_file";
      if (matches != null && matches[1]) {
        filename = matches[1];
      }

      console.log("Final filename:", filename);

      // Create a URL for the blob response
      const url = window.URL.createObjectURL(new Blob([response.data]));

      // Create a temporary link element and click it to trigger download
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", filename); // Set the filename for download
      document.body.appendChild(link);
      link.click();

      // Clean up: remove the temporary link and revoke the URL object
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Error downloading file:", error);
    }
  };

  return (
    <div className="file-container">
      <p className="file-title">{file.title}</p>
      <button className="delete-button" onClick={handleDownload}>
        Download
      </button>
      <p className="file-content">{file.content}</p>
      <p className="file-date">{formattedDate}</p>
      <button className="delete-button" onClick={() => onDelete(file.id)}>
        Delete
      </button>
    </div>
  );
}

export default File;
