import React, { useState, useEffect } from "react";
import "./Home.css";
import settingsIcon from "../res/icons/settings.png";
import SciSketchIcon from "../res/icons/SciSketch.png";
import addIcon from "../res/icons/add.png";
import optionsIcon from "../res/icons/options.png";
import sortIcon from "../res/icons/bx_sort.png";
import { useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faCloudArrowUp,
  faNoteSticky,
  faRobot,
  faBars,
  faGrip,
} from "@fortawesome/free-solid-svg-icons";
import FilesDragAndDrop from "../components/FilesDragAndDrop";
import gridIcon from "../res/icons/grid.png";
import axios from "axios";
import { v4 as uuidV4 } from "uuid";

function Home() {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState("");
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);

  const openAddModal = () => {
    setIsAddModalOpen(true);
  };

  const closeAddModal = () => {
    setIsAddModalOpen(false);
  };

  const openUploadModal = () => {
    setIsUploadModalOpen(true);
  };

  const openNewFile = () => {
    navigate(`/documents/${uuidV4()}`);
  };

  const closeUploadModal = () => {
    setIsUploadModalOpen(false);
  };

  // const [filesView, setFilesView] = useState("grid"); // 'grid' 或 'list'
  const [documents, setDocuments] = useState([]);
  const [filesView, setFilesView] = useState("grid");
  const [sortOrder, setSortOrder] = useState("name-asc");
  const [optionsMenu, setOptionsMenu] = useState(null); // Track which menu is open

  useEffect(() => {
    const fetchDocuments = async () => {
      try {
        // const response = await axios.get("http://localhost:5000/api/documents");
        const response = await axios.get("http://127.0.0.1:5000/api/documents");
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
        } else if (order === "date-asc") {
          console.log(a);
          return new Date(a.date) - new Date(b.date);
        } else if (order === "date-desc") {
          return new Date(b.date) - new Date(a.date);
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
    if (order === "name") {
      sortOrder.startsWith("name")
        ? setSortOrder(sortOrder === "name-asc" ? "name-desc" : "name-asc")
        : setSortOrder("name-asc");
    } else if (order === "date") {
      sortOrder.startsWith("date")
        ? setSortOrder(sortOrder === "date-asc" ? "date-desc" : "date-asc")
        : setSortOrder("date-asc");
    }
  };

  const handleFileClick = (documentId) => {
    navigate(`/documents/${documentId}`);
  };

  const onUpload = (files) => {
    console.log(files);
  };

  const handleOptionsMenu = (event, documentId) => {
    event.stopPropagation();
    setOptionsMenu(documentId === optionsMenu ? null : documentId);
    handleDeleteDocument(documentId);
  };

  const handleDeleteDocument = async (documentId) => {
    try {
      await axios.delete(`http://127.0.0.1:5000/api/documents/${documentId}`);
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
        <button onClick={toggleView} className="mx-2">
          {filesView === "grid" ? (
            <FontAwesomeIcon
              icon={faBars}
              className="fa-lg fa-regular"
              color="gray"
            />
          ) : (
            <FontAwesomeIcon
              icon={faGrip}
              className="fa-lg fa-regular"
              color="gray"
            />
          )}
          {/* <img src={gridIcon} alt="List View" className="tool-icon" /> */}
        </button>
        <button onClick={() => sortFiles("name")}>
          <img src={sortIcon} alt="Sort by name" className="tool-icon" />
        </button>
        <button onClick={() => sortFiles("date")}>
          <img src={sortIcon} alt="Sort by date" className="tool-icon" />
        </button>
      </div>

      <div>
        {filesView === "grid" ? (
          <div className="content">
            {" "}
            {/* Grid Display */}
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
        ) : (
          <div className="flex flex-col gap-2 mt-10">
            {" "}
            {/* List Display */}
            {filteredDocuments.map((document) => (
              <div
                key={document.id}
                className="bg-gray-300 rounded-lg mx-20 p-5"
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
        )}
      </div>

      <button className="hover:bg-gray-700 fab" onClick={openAddModal}>
        <img src={addIcon} alt="FAB" className="fab-icon" />
      </button>

      {isAddModalOpen && (
        <div
          className="fixed z-10 inset-0 overflow-y-auto"
          onClick={closeAddModal}
        >
          <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div
              className="fixed inset-0 transition-opacity"
              aria-hidden="true"
            >
              <div className="absolute inset-0 bg-gray-500 opacity-75"></div>
            </div>

            <span
              className="hidden sm:inline-block sm:align-middle sm:h-screen"
              aria-hidden="true"
            >
              &#8203;
            </span>

            <div
              className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-md sm:w-full"
              onClick={() => {
                openNewFile();
              }}
            >
              <div className="flex flex-col gap-3 bg-white p-4 justify-center items-center">
                <button
                  type="button"
                  className="h-24 w-full justify-center text-center rounded-md border-2 border-dashed border-slate-300 shadow-sm px-4 py-2 text-xl font-medium text-black hover:bg-gray-100"
                >
                  <div className="flex gap-2 justify-center">
                    <div>Blank</div>

                    <FontAwesomeIcon
                      icon={faNoteSticky}
                      className="fa-lg fa-regular"
                    />
                  </div>
                </button>
                <button
                  type="button"
                  className="h-24 w-full justify-center text-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-xl font-medium text-white hover:bg-gradient-to-r hover:from-purple-700 hover:to-pink-700"
                >
                  <div className="flex gap-2 justify-center">
                    <div>Create with AI</div>
                    <FontAwesomeIcon icon={faRobot} className="fa-lg" />
                  </div>
                </button>
                <button
                  type="button"
                  className="h-24 w-full justify-center text-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-xl font-medium text-white hover:bg-blue-700"
                  onClick={() => {
                    closeAddModal();
                    openUploadModal();
                  }}
                >
                  <div className="flex gap-2 justify-center">
                    <div>Upload</div>
                    <FontAwesomeIcon icon={faCloudArrowUp} className="fa-lg" />
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {isUploadModalOpen && (
        <div
          className="fixed z-10 inset-0 overflow-y-auto"
          onClick={closeUploadModal}
        >
          <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div
              className="fixed inset-0 transition-opacity"
              aria-hidden="true"
            >
              <div className="absolute inset-0 bg-gray-500 opacity-75"></div>
            </div>

            <span
              className="hidden sm:inline-block sm:align-middle sm:h-screen"
              aria-hidden="true"
            >
              &#8203;
            </span>

            <div
              className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle w-1/2"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex flex-col gap-3 bg-white p-4">
                <div className="text-2xl font-bold">Upload your document</div>
                <FilesDragAndDrop onUpload={onUpload} />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Home;
