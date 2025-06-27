// src/components/ForgotPassword.jsx
import React, { useState } from "react";

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
    <div>
      <h2>Forgot Your Password?</h2>
      <p>Enter your email to receive password reset instructions.</p>

      <form onSubmit={handleSubmit}>
        <input
          type="email"
          name="email"
          placeholder="Your email address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <button type="submit">Send Reset Link</button>
      </form>

      {message && <p style={{ color: "green" }}>{message}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default ForgotPassword;
