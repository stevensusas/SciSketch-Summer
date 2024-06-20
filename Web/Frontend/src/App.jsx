import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import EditDiagram from './pages/EditDiagram';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/edit-diagram" element={<EditDiagram />} />
      </Routes>
    </Router>
  );
}

export default App;
