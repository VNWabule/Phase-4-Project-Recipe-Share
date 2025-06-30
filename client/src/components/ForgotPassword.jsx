// src/components/ForgotPassword.jsx
import React, { useState } from "react";
import "./FormStyles.css"; // Adjust path if needed

function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  function handleSubmit(e) {
    e.preventDefault();

    fetch("http://localhost:5555/request_password_reset", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email })
    })
      .then((res) => {
        if (!res.ok) throw new Error("Reset request failed.");
        return res.json();
      })
      .then((data) => {
        setMessage(data.message || "Check your email for reset instructions.");
        setError(null);
      })
      .catch((err) => {
        setError(err.message || "Something went wrong.");
        setMessage(null);
      });
  }

  return (
    <div className="form-container">
      <h2>Forgot Your Password?</h2>
      <p style={{ textAlign: "center", marginBottom: "1.5rem" }}>
        Enter your email to receive password reset instructions.
      </p>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="email">Email Address</label>
          <input
            type="email"
            id="email"
            name="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <button type="submit" className="submit-btn">
          Send Reset Link
        </button>
      </form>

      {message && <p className="success-message">{message}</p>}
      {error && <p className="error-message">{error}</p>}
    </div>
  );
}

export default ForgotPassword;
