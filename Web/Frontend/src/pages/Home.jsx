import { useState } from "react";
import "./Home.css";
import settingsIcon from "../res/icons/settings.png";
import SciSketchIcon from "../res/icons/SciSketch.png";
import addIcon from "../res/icons/add.png";
import optionsIcon from "../res/icons/options.png";
import { useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState("");
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

      <button className="fab">
        <img src={addIcon} alt="FAB" className="fab-icon" />
      </button>
    </div>
  );
}

export default Home;
