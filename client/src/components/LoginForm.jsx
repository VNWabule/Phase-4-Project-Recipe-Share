import React, { useState } from "react";
import './FormStyles.css';

function LoginForm({ setUser }) {
  const [formData, setFormData] = useState({
    username: "",
    password: ""
  });
  const [error, setError] = useState(null);

  function handleChange(e) {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  }

  function handleSubmit(e) {
    e.preventDefault();
    fetch("https://phase-4-project-recipe-share-backend.onrender.com/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(formData)
    })
      .then(res => {
        if (!res.ok) throw new Error("Login failed");
        return res.json();
      })
      .then(data => {
        if (data.user && data.token) {
          localStorage.setItem("access_token", data.token);
          setUser(data.user);
        } else {
          setError(data.error || "Login failed");
        }
      })
      .catch(err => {
        console.error("Login error:", err);
        setError("Login failed: " + err.message);
      });
  }

  return (
    <div className="form-container">
      <h2>Login</h2>
      {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            type="text"
            name="username"
            id="username"
            placeholder="Enter username"
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            name="password"
            id="password"
            placeholder="Enter password"
            onChange={handleChange}
            required
          />
        </div>

        <button className="submit-btn" type="submit">Login</button>
      </form>

      <p style={{ marginTop: "10px", textAlign: "center" }}>
        <a href="/forgot-password">Forgot your password?</a>
      </p>
    </div>
  );
}

export default LoginForm;
