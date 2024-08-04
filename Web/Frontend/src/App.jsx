import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";
import { v4 as uuidV4 } from "uuid";
import Home from "./pages/Home";
import EditDiagram from "./pages/EditDiagram";
import EditFile from "./pages/EditFile";
import Landing from "./pages/Landing";
import LoginSignUp from "./pages/LoginSignUp";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<LoginSignUp />} />
        <Route path="/home" element={<Home />} />
        <Route
          path="/documents"
          element={<Navigate to={`/documents/${uuidV4()}`} />}
        />
        <Route path="/diagrams/:id" element={<EditDiagram />} />
        <Route path="/documents/:id" element={<EditFile />} />
        {/* Add other routes as needed */}
      </Routes>
    </Router>
  );
}

export default App;
