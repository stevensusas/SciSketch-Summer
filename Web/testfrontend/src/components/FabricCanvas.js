import React, { useEffect, useRef, useState } from 'react';
import { Canvas, Rect, Circle } from 'fabric';

const FabricCanvas = () => {
  const canvasRef = useRef(null);
  const [canvas, setCanvas] = useState(null);

  useEffect(() => {
    const fabricCanvas = new Canvas(canvasRef.current, {
      width: 500,
      height: 500,
      backgroundColor: '#f0f0f0'
    });

    const rect = new Rect({
      left: 100,
      top: 100,
      fill: 'red',
      width: 100,
      height: 100
    });

    fabricCanvas.add(rect);
    setCanvas(fabricCanvas);

    return () => {
      fabricCanvas.dispose();
    };
  }, []);

  const addCircle = () => {
    if (canvas) {
      const circle = new Circle({
        radius: 50,
        fill: 'green',
        left: 200,
        top: 200
      });
      canvas.add(circle);
      canvas.renderAll();
    }
  };

  const deleteSelected = () => {
    if (canvas) {
      const activeObject = canvas.getActiveObject();
      if (activeObject) {
        canvas.remove(activeObject);
        canvas.renderAll();
      } else {
        alert('Please select an object to delete');
      }
    }
  };

  return (
    <div>
      <canvas ref={canvasRef} />
      <div>
        <button onClick={addCircle}>Add Circle</button>
        <button onClick={deleteSelected}>Delete Selected</button>
      </div>
    </div>
  );
};

export default FabricCanvas;