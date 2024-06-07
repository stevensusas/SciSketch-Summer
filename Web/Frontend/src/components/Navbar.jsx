import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="top-navbar">
      <div className="container">
        <div className="brand">
          <Link to="/">My Brand</Link>
        </div>
        <div className="menu">
          <Link to="/about">About</Link>
          <Link to="/services">Services</Link>
          <Link to="/contact">Contact</Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
