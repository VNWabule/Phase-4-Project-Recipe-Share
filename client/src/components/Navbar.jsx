import React from "react";
import { Link, useNavigate } from "react-router-dom";
import './Navbar.css';

function Navbar({ user, setUser }) {
  const navigate = useNavigate();

  function handleLogout() {
    fetch("http://localhost:5555/logout", {
      method: "DELETE",
      credentials: "include",
    }).then(() => {
      setUser(null);
      navigate("/");
    });
  }

  return (
    <nav className="navbar">
      <h1 className="navbar-title">RecipeShare</h1>
      <div className="navbar-links">
        <Link to="/">Home</Link>
        {user ? (
          <>
            <Link to="/add-recipe" className="add-recipe-nav-button">
              + Add Recipe
            </Link>
            <Link to="/bookmarks" className="bookmark-nav-button">
              📌 Bookmarks
            </Link>
            <span className="welcome-msg">Welcome, {user.username}</span>
            <button onClick={handleLogout} className="logout-button">
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
