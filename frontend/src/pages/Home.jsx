import { useState, useEffect } from "react";
import api from "../api";
import File from "../components/File";
import "../styles/Home.css";

function Home() {
  // This is for displaying the files
  const [files, setFiles] = useState([]);
  // This is the file that is about to be uploaded (confusing I know)
  const [uploadFile, setUploadFile] = useState(null);
  const [content, setContent] = useState("");
  const [title, setTitle] = useState("");

  useEffect(() => {
    getFiles();
  }, []);

  /* const handleFileChange = (e) => {
    setUploadFile(e.target.files[0]);
  }; */

  const getFiles = () => {
    api
      .get("/api/files/")
      .then((res) => res.data)
      .then((data) => {
        setFiles(data);
        console.log(data);
      })
      .catch((err) => alert(err));
  };

  const deleteFile = (id) => {
    api
      .delete(`/api/files/delete/${id}/`)
      .then((res) => {
        if (res.status === 204) alert("File Deleted!");
        else alert("Failed to delete file.");
        getFiles();
      })
      .catch((error) => alert(error));
  };

  const createFile = (e) => {
    e.preventDefault();

    // Create a FormData object
    const formData = new FormData();
    formData.append("file", uploadFile);
    formData.append("content", content);
    formData.append("title", title);

    api
      .post("/api/files/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((res) => {
        if (res.status === 201) alert("File uploaded!");
        else alert("Failed to uploaded file.");
        getFiles();
      })
      .catch((error) => alert(error));
  };

  return (
    <div>
      <div>
        <h2>Files</h2>
        {files.map((file) => (
          <File file={file} onDelete={deleteFile} key={file.id} />
        ))}
      </div>
      <h2>Create a File</h2>
      <form onSubmit={createFile}>
        <label htmlFor="title">Title:</label>
        <br />
        <input
          type="text"
          id="title"
          name="title"
          required
          onChange={(e) => setTitle(e.target.value)}
          value={title}
        />
        <label htmlFor="file">File:</label>
        <br />
        <input
          type="file"
          id="file"
          name="file"
          required
          onChange={(e) => setUploadFile(e.target.files[0])}
        />
        <label htmlFor="content">Content:</label>
        <br />
        <textarea
          id="content"
          name="content"
          required
          onChange={(e) => setContent(e.target.value)}
          value={content}
        ></textarea>
        <br />
        <input type="submit" value="Submit"></input>
      </form>
    </div>
  );
}

export default Home;
