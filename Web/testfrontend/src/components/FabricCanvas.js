import React, { useEffect, useRef, useState } from 'react';
import { Canvas, Circle, Text, loadSVGFromURL, Group } from 'fabric';

const FabricCanvas = () => {
  const canvasRef = useRef(null);
  const [canvas, setCanvas] = useState(null);
  const [inputText, setInputText] = useState('');

  useEffect(() => {
    const fabricCanvas = new Canvas(canvasRef.current, {
      width: window.innerWidth,
      height: window.innerHeight - 200, // Adjust height to start below the input area
      backgroundColor: '#f9f9f9'
    });

    setCanvas(fabricCanvas);

    // Handle window resize to adjust canvas size
    const handleResize = () => {
      fabricCanvas.setWidth(window.innerWidth);
      fabricCanvas.setHeight(window.innerHeight - 200); // Adjust height again on resize
      fabricCanvas.renderAll();
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      fabricCanvas.dispose();
    };
  }, []);

  const callFlaskInference = async (inputData) => {
    const url = 'http://127.0.0.1:5000/inference';
    const headers = { 'Content-Type': 'application/json' };

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(inputData)
      });

      if (response.status === 200) {
        const result = await response.json();
        console.log("Success:");
        console.log(result);
        return result;
      } else {
        console.error(`Failed with status code: ${response.status}`);
        const errorData = await response.json();
        console.error(errorData);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const fetchAndRenderData = async () => {
    // Clear the canvas before rendering new content
    canvas.clear();

    // Add the prefix to the input text
    const prefixedInputText = `generate key phrases: ${inputText}`;

    const inputData = {
      inputs: prefixedInputText // Use the prefixed text input from the user
    };

    const data = await callFlaskInference(inputData);

    if (data && data.results) {
      // Find the minimum x and y values
      let minX = Infinity;
      let minY = Infinity;

      data.results.forEach(result => {
        if (result.x < minX) minX = result.x;
        if (result.y < minY) minY = result.y;
      });

      // Adjust by the minimum negative value to ensure all coordinates are positive
      const xOffset = Math.abs(minX < 0 ? minX : 0);
      const yOffset = Math.abs(minY < 0 ? minY : 0);

      data.results.forEach(result => {
        const adjustedX = result.x + xOffset;
        const adjustedY = result.y + yOffset;

        if (result.icon_url) {
          // Load and add SVG to the canvas
          loadSVGFromURL(result.icon_url, (objects, options) => {
            const svgGroup = new Group(objects);
            svgGroup.set({
              left: adjustedX,
              top: adjustedY,
              scaleX: 5, // Adjust the scale factor as needed
              scaleY: 5,
              selectable: true
            });
            canvas.add(svgGroup);
            canvas.renderAll();  // Ensure the image is rendered after adding
          });
        } else {
          // If no icon, draw a circle as a placeholder
          const circle = new Circle({
            radius: 20,
            fill: '#007bff',
            left: adjustedX,
            top: adjustedY,
            selectable: true  // Make the circle selectable and movable
          });
          canvas.add(circle);
        }

        // Add phrase as text on the canvas
        const text = new Text(result.phrase, {
          left: adjustedX + 10, // Offset the text slightly to the right of the icon
          top: adjustedY + 20,  // Offset the text slightly below the icon
          fontSize: 18,
          fill: '#333',
          selectable: true // Make the text selectable and movable
        });
        canvas.add(text);
      });

      canvas.renderAll();
    }
  };

  const handleTextInputChange = (event) => {
    setInputText(event.target.value);
  };

  return (
    <div style={{ width: '100vw', height: '100vh', display: 'flex', flexDirection: 'column', fontFamily: 'Arial, sans-serif' }}>
      <div style={{ padding: '15px 20px', backgroundColor: '#343a40', color: '#fff', fontSize: '24px', fontWeight: 'bold', textAlign: 'center' }}>
        SciSketch Test Diagram
      </div>
      <div style={{ padding: '20px', backgroundColor: '#f8f9fa', boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)', zIndex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <textarea 
          value={inputText} 
          onChange={handleTextInputChange} 
          placeholder="Enter text here..." 
          style={{ width: '100%', height: '150px', padding: '20px', fontSize: '18px', borderRadius: '5px', border: '1px solid #ced4da', marginBottom: '15px', boxShadow: 'inset 0px 1px 2px rgba(0, 0, 0, 0.1)' }}
        />
        <button 
          onClick={fetchAndRenderData} 
          style={{ width: '100%', padding: '20px', fontSize: '24px', borderRadius: '5px', backgroundColor: '#007bff', color: '#fff', border: 'none', cursor: 'pointer', boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)' }}
        >
          Generate
        </button>
      </div>
      <div style={{ flex: 1 }}>
        <canvas ref={canvasRef} style={{ width: '100%', height: '100%' }} />
      </div>
    </div>
  );
};

export default FabricCanvas;
