import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { fabric } from 'fabric';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCog, faUndo, faRedo, faMousePointer, faHandPaper, faSearch, faChevronLeft, faChevronRight } from '@fortawesome/free-solid-svg-icons';
// import './EditDiagram.css'; // Note: using tailwindcss instead for now

function EditDiagram() {
  const { fileId } = useParams();
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [activeTab, setActiveTab] = useState('iconsLibrary');

  useEffect(() => {
    const canvas = new fabric.Canvas('diagram-canvas');
    // Add Fabric.js canvas setup code here
  }, []);

  return (
    <div className={`flex flex-col h-screen ${isCollapsed ? 'collapsed' : ''}`}>
      <div className="flex justify-between items-center bg-gray-300 p-2">
        <span className="text-xl ml-3">Diagram Title</span>
        <button className="bg-green-500 hover:bg-green-600 text-white w-36 px-4 py-2 rounded-lg">Export</button>
      </div>
      <div className="flex items-center bg-gray-400 p-2">
        <button className="mr-2 w-10 h-10 rounded hover:bg-gray-600 transition">
          <FontAwesomeIcon icon={faCog} className="cursor-pointer fa-xl" />
        </button>
        <button className="mr-2 w-10 h-10 rounded hover:bg-gray-600 transition">
          <FontAwesomeIcon icon={faUndo} className="cursor-pointer fa-xl" />
        </button>
        <button className="mr-2 w-10 h-10 rounded hover:bg-gray-600 transition">
          <FontAwesomeIcon icon={faRedo} className="cursor-pointer fa-xl" />
        </button>
        <button className="mr-2 w-10 h-10 rounded hover:bg-gray-600 transition">
          <FontAwesomeIcon icon={faMousePointer} className="cursor-pointer fa-xl" />
        </button>
        <button className="mr-2 w-10 h-10 rounded hover:bg-gray-600 transition">
          <FontAwesomeIcon icon={faHandPaper} className="cursor-pointer fa-xl" />
        </button>
      </div>
      <div className="flex flex-1 bg-gray-200 rounded-lg p-2">
        <div className={`flex-1 bg-gray-300 p-2 my-4 mx-16 shadow-lg rounded-lg flex justify-center items-center`}>
            <canvas id="diagram-canvas" width="1000" height="800" className="bg-white rounded-lg shadow-md"></canvas>
        </div>
        <div className={`flex flex-col w-1/3 bg-gray-700 rounded-lg text-white transition-transform duration-500 ${isCollapsed ? 'transform translate-x-full w-0' : 'transform translate-x-0'}`}>
          <div className="flex items-center bg-gray-600 p-2 rounded-t-lg">
            <button
              className={`flex-1 p-2 rounded-l-lg border ${activeTab === 'iconsLibrary' ? 'bg-gray-500' : ''}`}
              onClick={() => setActiveTab('iconsLibrary')}
            >
              Icons Library
            </button>
            <button
              className={`flex-1 p-2 rounded-r-lg border-y border-r ${activeTab === 'aiControls' ? 'bg-gray-500' : ''}`}
              onClick={() => setActiveTab('aiControls')}
            >
              AI Controls
            </button>
            <button className="w-8 ml-2" onClick={() => setIsCollapsed(!isCollapsed)}>
              <FontAwesomeIcon icon={isCollapsed ? faChevronLeft : faChevronRight} />
            </button>
          </div>
          <div className="py-2 px-3 flex-1 relative">
            {activeTab === 'iconsLibrary' ? (
              <>
                <div className="relative mt-2 mb-4">
                  <input type="text" placeholder="Search" className="w-full p-2 rounded-lg text-black" />
                  {!isCollapsed && <FontAwesomeIcon icon={faSearch} className="absolute top-3 right-3 text-gray-500" />}
                </div>
                <div className="grid grid-cols-3 gap-2">
                  {/* Add icon placeholders here */}
                  <div className="h-32 bg-gray-500 rounded-lg"></div>
                  <div className="h-32 bg-gray-500 rounded-lg"></div>
                  <div className="h-32 bg-gray-500 rounded-lg"></div>
                  <div className="h-32 bg-gray-500 rounded-lg"></div>
                  <div className="h-32 bg-gray-500 rounded-lg"></div>
                  <div className="h-32 bg-gray-500 rounded-lg"></div>
                  <div className="h-32 bg-gray-500 rounded-lg"></div>
                  <div className="h-32 bg-gray-500 rounded-lg"></div>
                  {/* Add more icon placeholders as needed */}
                </div>
              </>
            ) : (
              <p>AI Controls</p>
            )}
          </div>
        </div>
        {isCollapsed && (
          <button
            className="absolute right-0 top-1/2 transform -translate-y-1/2 bg-gray-600 text-white rounded-l-lg p-2"
            onClick={() => setIsCollapsed(false)}
          >
            <FontAwesomeIcon icon={faChevronLeft} />
          </button>
        )}
      </div>
    </div>
  );
}

export default EditDiagram;
