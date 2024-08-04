import { useCallback, useEffect, useState } from "react";
import Quill from "quill";
import "quill/dist/quill.snow.css";
import { useParams, useNavigate, Link, useLocation } from "react-router-dom";
import axios from "axios";
import ImageResize from "quill-image-resize-module-react";
import "./EditFile.css";
import { v4 as uuidV4 } from "uuid";

// Register the ImageResize module with Quill
Quill.register("modules/imageResize", ImageResize);

// CUSTOM IMAGE BLOT
const ImageBlot = Quill.import('formats/image');

class CustomImageBlot extends ImageBlot {
  static create(value) {
    console.log("Creating custom image blot with value:", value);
    let node = super.create();
    node.setAttribute('src', value.src);
    node.setAttribute('data-diagram-id', value.diagramId);
    console.log(node);
    return node;
  }

  static value(node) {
    return {
      src: node.getAttribute('src'),
      diagramId: node.getAttribute('data-diagram-id'),
    };
  }
}

CustomImageBlot.blotName = 'customImage';
CustomImageBlot.tagName = 'img';

Quill.register(CustomImageBlot, true);
// END CUSTOM IMAGE BLOT

const SAVE_INTERVAL_MS = 2000;
const TOOLBAR_OPTIONS = [
  [{ header: [1, 2, 3, 4, 5, 6, false] }],
  [{ font: [] }],
  [{ list: "ordered" }, { list: "bullet" }],
  ["bold", "italic", "underline"],
  [{ color: [] }, { background: [] }],
  [{ script: "sub" }, { script: "super" }],
  [{ align: [] }],
  ["image", "blockquote", "code-block"],
  ["clean"],
];

export default function TextEditor() {
  const { id: documentId } = useParams();
  const navigate = useNavigate();
  const location = useLocation(); 
  const [quill, setQuill] = useState(null);
  const [fileName, setFileName] = useState(null);

  const [contextMenu, setContextMenu] = useState({ visible: false, x: 0, y: 0, diagramId: null });

  useEffect(() => {
    const fetchDocument = async () => {
      try {
        const response = await axios.get(
          //`http://localhost:5000/api/documents/${documentId}`
          `http://127.0.0.1:5000/api/documents/${documentId}`
        );
        if (quill) {
          console.log("quill fetching document data");
          quill.setContents(response.data.content);
          if (location.state && location.state.image && quill) {
            console.log("CHECKING FOR EXISTING IMAGE");
            const existingImages = quill.root.querySelectorAll(`img[data-diagram-id="${location.state.diagramId}"]`);
            if (existingImages.length > 0) {
              console.log("REPLACING EXISTING IMAGE");
              existingImages.forEach(img => {
                img.src = location.state.image; // Update the src of existing images
              });
            } else {
              console.log("INSERTING IMAGE");
              quill.insertEmbed(0, 'customImage', {src: location.state.image, diagramId: location.state.diagramId});
              const img = quill.root.querySelector(`img[src="${location.state.image}"]`);
              console.log("img", img);
              if (img) {
                img.setAttribute('data-diagram-id', location.state.diagramId);
              }
            }
            // quill.insertEmbed(0, 'image', location.state.image); // Insert the image at the top of the editor
            // quill.setSelection(quill.getLength(), 0); // Move the cursor to the end of the editor
          }
          quill.enable();
        }
        setFileName(response.data.name);
      } catch (error) {
        console.error("Error fetching document:", error);
      }
    };

    fetchDocument();
  }, [location, documentId, quill]);

  useEffect(() => {
    if (quill == null) return;

    const interval = setInterval(() => {
      saveDocument();
    }, SAVE_INTERVAL_MS);

    return () => {
      clearInterval(interval);
      saveDocument(); // Save document one last time on component unmount
    };
  }, [quill, documentId, fileName]);

  const saveDocument = async () => {
    if (!quill) return;
    try {
      //await axios.post(`http://localhost:5000/api/documents/${documentId}`, {
      await axios.post(`http://127.0.0.1:5000/api/documents/${documentId}`, {
        content: quill.getContents(),
        name: fileName,
      });
    } catch (error) {
      console.error("Error saving document:", error);
    }
  };

  const wrapperRef = useCallback((wrapper) => {
    if (wrapper == null) return;

    wrapper.innerHTML = "";
    const editor = document.createElement("div");
    wrapper.append(editor);
    const q = new Quill(editor, {
      theme: "snow",
      modules: {
        toolbar: TOOLBAR_OPTIONS,
        imageResize: {
          modules: ["Resize", "DisplaySize"],

          displayStyles: {
            backgroundColor: "black",
            border: "none",
            color: "white",
            // other camelCase styles for size display
          },
          toolbarStyles: {
            backgroundColor: "black",
            border: "none",
            color: "white",
            // other camelCase styles for size display
          },
          toolbarButtonStyles: {
            // ...
          },
          toolbarButtonSvgStyles: {
            // ...
          },
        },
      },
    });

    q.disable();
    setQuill(q);
  }, []);

  useEffect(() => {
    if (quill == null) return;

    const handleImageRightClick = (event) => {
      event.preventDefault();

      let target = event.target;
      console.log("Target:", target);
      // Directly clicked on an image
      if (target.tagName === 'IMG') {
        console.log("Image right-clicked:", target.src);
        console.log("event.pageX", event.pageX);
        console.log("event.pageY", event.pageY);
        console.log(target);
        console.log("Diagram ID:", target.getAttribute("data-diagram-id"));
        setContextMenu({
          visible: true,
          x: event.pageX,
          y: event.pageY,
          diagramId: target.getAttribute("data-diagram-id"),
        });
      } else {
        // Check if the target is an overlay with a dashed border
        if (target.style.borderStyle.includes('dashed')) {
          const overlayRect = target.getBoundingClientRect();
          const images = document.querySelectorAll('img');
          let closestImage = null;
          let smallestDistance = Infinity;

          images.forEach(img => {
            const imgRect = img.getBoundingClientRect();
            // Calculate the distance between the center points of the overlay and the image
            const distance = Math.sqrt(Math.pow(imgRect.left + imgRect.width / 2 - (overlayRect.left + overlayRect.width / 2), 2) + Math.pow(imgRect.top + imgRect.height / 2 - (overlayRect.top + overlayRect.height / 2), 2));

            if (distance < smallestDistance) {
              closestImage = img;
              smallestDistance = distance;
            }
          });

          if (closestImage) {
            console.log("Image right-clicked:", closestImage.src);
            console.log("event.pageX", event.pageX);
            console.log("event.pageY", event.pageY);
            console.log(closestImage);
            console.log("Diagram ID:", closestImage.getAttribute('data-diagram-id'));
            setContextMenu({
              visible: true,
              x: event.pageX,
              y: event.pageY,
              diagramId: closestImage.getAttribute('data-diagram-id'),
            });
          }
        }
      }
    };

    const handleClickOutside = () => setContextMenu({ visible: false, x: 0, y: 0, diagramId: null });

    const quillContainer = quill.container;
    quillContainer.addEventListener("contextmenu", handleImageRightClick);
    quillContainer.addEventListener('click', handleClickOutside);

    return () => {
      quillContainer.removeEventListener("contextmenu", handleImageRightClick);
      quillContainer.removeEventListener('click', handleClickOutside);
    };
  }, [quill]);

  const handleBackToHome = () => {
    saveDocument(); // Save document before navigating back
    navigate("/home");
  };

  const handleFileNameChange = (e) => {
    setFileName(e.target.value);
  };

  const handleAddDiagram = () => {
    navigate(`/diagrams/${uuidV4()}`, { state: { documentId: documentId } })
  };

  return (
    <div className="cont">
      <div className="flex justify-between top-bar">
        <div>
          <button onClick={handleBackToHome} className="back-button">
            Home
          </button>
          <input
            type="text"
            value={fileName}
            onChange={handleFileNameChange}
            className="file-name-input"
          />
        </div>
        <button onClick={handleAddDiagram} className="bg-blue-500 rounded-md text-white p-2">Add Diagram</button>
      </div>
      <div className="container" ref={wrapperRef}></div>

      {contextMenu.visible && (
        <div
          className="absolute z-50 bg-white shadow-lg rounded-md overflow-hidden"
          style={{ top: `${contextMenu.y}px`, left: `${contextMenu.x}px` }}
        >
          <button
            className="text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full"
            onClick={() => {
              console.log("Edit diagram ID:", contextMenu.diagramId);
              setContextMenu({ visible: false, x: 0, y: 0, diagramId: null }); // Hide context menu
              navigate(`/diagrams/${contextMenu.diagramId}`, { state: { documentId: documentId } }
              );
            }}
          >
            Edit Diagram
          </button>
        </div>
      )}
    </div>
  );
}
