import { useState } from "react";
import "./Home.css";
import settingsIcon from "../res/icons/settings.png";
import SciSketchIcon from "../res/icons/SciSketch.png";
import addIcon from "../res/icons/add.png";
import optionsIcon from "../res/icons/options.png";
import { useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCloudArrowUp, faNoteSticky, faRobot } from '@fortawesome/free-solid-svg-icons';
import FilesDragAndDrop from "../components/FilesDragAndDrop";

function Home() {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState("");
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false); 
  const userFiles = [
    { id: 1, name: "File 1" },
    { id: 2, name: "File 2" },
    { id: 3, name: "File 3" },
    { id: 4, name: "File 4" },
    { id: 5, name: "File 5" },
    { id: 6, name: "File 6" },
    { id: 7, name: "File 7" },
    // sample files
  ];

  const openAddModal = () => {
    setIsAddModalOpen(true);
  };

  const closeAddModal = () => {
    setIsAddModalOpen(false);
  };

  const openUploadModal = () => {
    setIsUploadModalOpen(true);
  };

  const closeUploadModal = () => {
    setIsUploadModalOpen(false);
  };

  const [filesView, setFilesView] = useState("grid"); // 'grid' 或 'list'
  const [sortOrder, setSortOrder] = useState("name-asc");

  const toggleView = () => {
    setFilesView(filesView === "grid" ? "list" : "grid");
  };

  const sortFiles = (order) => {
    setSortOrder(order);
  };

  const navigateToEditDiagram = () => {
	console.log("Navigating to edit diagram");
    navigate("/edit-diagram");
  };

  const onUpload = (files) => {
    console.log(files);
  };

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
          <img src={settingsIcon} alt="List View" className="tool-icon" />
        </button>
        <button onClick={() => sortFiles("name-asc")}>
          <img src={settingsIcon} alt="Sort A-Z" className="tool-icon" />
        </button>
        <button onClick={() => sortFiles("name-desc")}>
          <img src={settingsIcon} alt="Sort Z-A" className="tool-icon" />
        </button>
        {/* 根据需要添加更多按钮 */}
      </div>

      <div className="content">
        {userFiles.map((file) => (
          <div key={file.id} className="file">
            {file.name}
            <button
              className="file-options-button"
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

      <button className="hover:bg-gray-700 fab" onClick={openAddModal}>
        <img src={addIcon} alt="FAB" className="fab-icon" />
      </button>

      {isAddModalOpen && (
        <div className="fixed z-10 inset-0 overflow-y-auto" onClick={closeAddModal}>
          <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 transition-opacity" aria-hidden="true">
              <div className="absolute inset-0 bg-gray-500 opacity-75"></div>
            </div>

            <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

            <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-md sm:w-full" onClick={e => e.stopPropagation()}>
              <div className="flex flex-col gap-3 bg-white p-4 justify-center items-center">
                <button type="button" className="h-24 w-full justify-center text-center rounded-md border-2 border-dashed border-slate-300 shadow-sm px-4 py-2 text-xl font-medium text-black hover:bg-gray-100">
                <div className="flex gap-2 justify-center">
                    <div>Blank</div>
                    <FontAwesomeIcon icon={faNoteSticky} className="fa-lg fa-regular" />
                  </div>
                </button>
                <button type="button" className="h-24 w-full justify-center text-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-xl font-medium text-white hover:bg-gradient-to-r hover:from-purple-700 hover:to-pink-700">
                <div className="flex gap-2 justify-center">
                    <div>Create with AI</div>
                    <FontAwesomeIcon icon={faRobot} className="fa-lg" />
                  </div>
                </button>
                <button type="button" className="h-24 w-full justify-center text-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-xl font-medium text-white hover:bg-blue-700" onClick={() => {
                  closeAddModal();
                  openUploadModal();  
                }}>
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
        <div className="fixed z-10 inset-0 overflow-y-auto" onClick={closeUploadModal}>
          <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 transition-opacity" aria-hidden="true">
              <div className="absolute inset-0 bg-gray-500 opacity-75"></div>
            </div>

            <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

            <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle w-1/2" onClick={e => e.stopPropagation()}>
              <div className="flex flex-col gap-3 bg-white p-4">
                <div className="text-2xl font-bold">Upload your document</div>
                <FilesDragAndDrop
                  onUpload={onUpload}
                />
              </div>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}

export default Home;
