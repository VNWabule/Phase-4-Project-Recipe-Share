// src/components/ResetPassword.jsx
import React, { useState } from "react";
import "./FormStyles.css"; // Make sure path is correct

function ResetPassword() {
  const [token, setToken] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  function handleSubmit(e) {
    e.preventDefault();

    fetch("https://phase-4-project-recipe-share-backend.onrender.com/reset_password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token, new_password: newPassword })
    })
      .then((res) => {
        if (!res.ok) throw new Error("Password reset failed.");
        return res.json();
      })
      .then((data) => {
        setMessage(data.message || "Password reset successful.");
        setError(null);
      })
      .catch((err) => {
        setError(err.message || "Something went wrong.");
        setMessage(null);
      });
  }

  return (
    <div className="form-container">
      <h2>Reset Your Password</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="token">Reset Token</label>
          <input
            type="text"
            id="token"
            name="token"
            value={token}
            onChange={(e) => setToken(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="new_password">New Password</label>
          <input
            type="password"
            id="new_password"
            name="new_password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            required
          />
        </div>

        <button type="submit" className="submit-btn">
          Reset Password
        </button>
      </form>

      {message && <p className="success-message">{message}</p>}
      {error && <p className="error-message">{error}</p>}
    </div>
  );
}

export default ResetPassword;
