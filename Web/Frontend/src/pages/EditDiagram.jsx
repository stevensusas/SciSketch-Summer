import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { fabric } from 'fabric';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCog, faUndo, faRedo, faMousePointer, faHandPaper, faSearch, faChevronLeft, faChevronRight } from '@fortawesome/free-solid-svg-icons';
// import './EditDiagram.css'; // Note: using tailwindcss instead for now


function EditDiagram() {
    console.log("MOUNTING");

  const { fileId } = useParams();
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [activeTab, setActiveTab] = useState('iconsLibrary');

  const [searchTerm, setSearchTerm] = useState('');

  const images = [
    '/icon_library/microscope.png',
    '/icon_library/mouse1.png',
    '/icon_library/mouse2.png',
    // Add more images as needed
  ];

  // const [images, setImages] = useState([]);


  useEffect(() => {
    

    const canvas = new fabric.Canvas('diagram-canvas');
    const parentDiv = document.getElementById('canvas-parent-div'); 

    const handleKeyDown = (e) => {
      if (e.key === 'Backspace') {
        const activeObjects = canvas.getActiveObjects();
        canvas.discardActiveObject();
        if (activeObjects.length) {
          canvas.remove.apply(canvas, activeObjects);
        }
      }
    };

    // Function to resize canvas
    const resizeCanvas = () => {
      canvas.setWidth(parentDiv.offsetWidth);
      canvas.setHeight(parentDiv.offsetHeight);
      canvas.renderAll();
    };

    // Initial resize
    resizeCanvas();

    // Resize canvas on window resize
    window.addEventListener('resize', resizeCanvas);
    window.addEventListener('keydown', handleKeyDown);


    canvas.backgroundColor = 'rgba(255,255,255,1)';
    canvas.renderAll();
  
    // Function to load images onto the canvas
    function handleDrop(e) {
      e.preventDefault();
      e.stopPropagation();
  
      const imageUrl = e.dataTransfer.getData("text");

      fabric.Image.fromURL(imageUrl, function(img) {
        img.set({
          left: e.layerX - (img.width / 2) / 2,
          top: e.layerY - (img.height / 2) / 2,
          scaleX: 0.5,
          scaleY: 0.5
        });
        canvas.add(img);
      });

    }

    
  
    // Adding event listeners for the drag and drop
    const canvasContainer = document.getElementById('diagram-canvas').parentNode;
    canvasContainer.addEventListener('dragover', e => e.preventDefault());
    canvasContainer.addEventListener('drop', handleDrop);
  
    // Clean up function
    return () => {
        console.log("cleaning up...");
    //   canvasContainer.removeEventListener('dragover', e => e.preventDefault());
    //   canvasContainer.removeEventListener('drop', handleDrop);
    };
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
        <div id="canvas-parent-div" className={`flex-1 bg-gray-300 my-4 mx-16 shadow-lg rounded-lg`}>
            <canvas id="diagram-canvas"></canvas>
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
                  <input type="text" placeholder="Search" className="w-full p-2 rounded-lg text-black" value={searchTerm}
      onChange={(e) => setSearchTerm(e.target.value)}/>
                  {!isCollapsed && <FontAwesomeIcon icon={faSearch} className="absolute top-3 right-3 text-gray-500" />}
                </div>
                <div className="grid grid-cols-3 gap-2">
                  {/* <div className="h-32 bg-gray-500 rounded-lg"></div> */}
                  {images.filter((image) => image.includes(searchTerm)).map((image, index) => (
                    <div key={index} className='flex justify-center p-2 2xl:w-48 bg-slate-800 rounded-lg'>
                        <img
                            key={index}
                            src={image}
                            alt={`Image ${index + 1}`}
                            className="h-32 rounded-lg cursor-pointer"
                            draggable="true"
                            onDragStart={(e) => {
                                e.dataTransfer.setData("text", image);
                            }}
                        />
                    </div>
                  ))}
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
