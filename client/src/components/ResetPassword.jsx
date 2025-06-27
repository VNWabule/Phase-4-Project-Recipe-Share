// src/components/ResetPassword.jsx
import React, { useState } from "react";

function ResetPassword() {
  const [token, setToken] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  function handleSubmit(e) {
    e.preventDefault();

    fetch("http://localhost:5555/reset_password", {
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
    <div>
      <h2>Reset Your Password</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="token"
          placeholder="Reset token"
          value={token}
          onChange={(e) => setToken(e.target.value)}
          required
        />
        <input
          type="password"
          name="new_password"
          placeholder="New password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          required
        />
        <button type="submit">Reset Password</button>
      </form>

      {message && <p style={{ color: "green" }}>{message}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default ResetPassword;
