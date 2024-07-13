import React, { useState, useEffect } from "react";
import "./Home.css";
import settingsIcon from "../res/icons/settings.png";
import SciSketchIcon from "../res/icons/SciSketch.png";
import addIcon from "../res/icons/add.png";
import optionsIcon from "../res/icons/options.png";
import sortIcon from "../res/icons/bx_sort.png";
import { useNavigate } from "react-router-dom";
import gridIcon from "../res/icons/grid.png";
import axios from "axios";
import blank from "../res/images/blank.png";

function Home() {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState("");
  const [documents, setDocuments] = useState([]);
  const [filesView, setFilesView] = useState("grid");
  const [sortOrder, setSortOrder] = useState("name-asc");
  const [optionsMenu, setOptionsMenu] = useState(null); // Track which menu is open

  useEffect(() => {
    const fetchDocuments = async () => {
      try {
        const response = await axios.get("http://localhost:5000/api/documents");
        setDocuments(response.data);
      } catch (error) {
        console.error("Error fetching documents:", error);
      }
    };

    fetchDocuments();
  }, []);

  useEffect(() => {
    const sortDocuments = (order) => {
      const sortedDocuments = [...documents].sort((a, b) => {
        if (order === "name-asc") {
          return a.name.localeCompare(b.name);
        } else if (order === "name-desc") {
          return b.name.localeCompare(a.name);
        }
        return 0;
      });
      setDocuments(sortedDocuments);
    };
    sortDocuments(sortOrder);
  }, [sortOrder]);

  const toggleView = () => {
    setFilesView(filesView === "grid" ? "list" : "grid");
  };

  const sortFiles = (order) => {
    sortOrder === "name-asc"
      ? setSortOrder("name-desc")
      : setSortOrder("name-asc");
  };

  const handleFileClick = (documentId) => {
    navigate(`/documents/${documentId}`);
  };

  const handleOptionsMenu = (event, documentId) => {
    event.stopPropagation();
    setOptionsMenu(documentId === optionsMenu ? null : documentId);
    handleDeleteDocument(documentId);
  };

  const handleDeleteDocument = async (documentId) => {
    try {
      await axios.delete(`http://localhost:5000/api/documents/${documentId}`);
      setDocuments(documents.filter((doc) => doc.id !== documentId));
      setOptionsMenu(null); // Close the options menu after deletion
    } catch (error) {
      console.error("Error deleting document:", error);
    }
  };

  const filteredDocuments = documents.filter((document) =>
    document.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="app-container">
      <div className="header">
        <img src={SciSketchIcon} alt="sciSketch" className="logo" />
        <input
          type="text"
          placeholder="Search"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="search-bar"
        />
        <button className="settings-button">
          <img src={settingsIcon} alt="Settings" className="settings-icon" />
        </button>
      </div>

      <div className="tool-bar">
        <button onClick={toggleView}>
          <img src={gridIcon} alt="List View" className="tool-icon" />
        </button>
        <button onClick={() => sortFiles("name-asc")}>
          <img src={sortIcon} alt="Sort A-Z" className="tool-icon" />
        </button>
        <button onClick={() => sortFiles("name-desc")}>
          <img src={sortIcon} alt="Sort Z-A" className="tool-icon" />
        </button>
      </div>

      <div className="content">
        {filteredDocuments.map((document) => (
          <div
            key={document.id}
            className="file"
            onClick={() => handleFileClick(document.id)}
            onMouseEnter={() => setOptionsMenu(document.id)}
            onMouseLeave={() => setOptionsMenu(null)}
          >
            <p className="file-name">{document.name}</p>

            <button
              className="file-options-button"
              onClick={(e) => handleOptionsMenu(e, document.id)}
            >
              <img
                src={optionsIcon}
                alt="Options"
                className="file-options-icon"
              />
            </button>
          </div>
        ))}
      </div>

      <button className="fab">
        <img src={addIcon} alt="FAB" className="fab-icon" />
      </button>
    </div>
  );
}

export default Home;
