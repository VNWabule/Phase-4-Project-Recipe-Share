import React, { useState } from 'react';
import axios from 'axios';
import './FormStyles.css';

function RegisterForm() {
  const [form, setForm] = useState({ username: '', email: '', password: '' });
  const [message, setMessage] = useState('');

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      const res = await axios.post('https://phase-4-project-recipe-share-backend.onrender.com/register', form, {
        withCredentials: true,
      });
      setMessage(res.data.message);
    } catch (err) {
      setMessage(err.response?.data?.error || 'Registration failed.');
    }
  }

  return (
    <div className="form-container">
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            id="username"
            name="username"
            placeholder="Enter username"
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            id="email"
            name="email"
            placeholder="Enter email"
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            placeholder="Enter password"
            onChange={handleChange}
            required
          />
        </div>

        <button className="submit-btn" type="submit">Register</button>
      </form>

      {message && (
        <p style={{ marginTop: '10px', textAlign: 'center', color: message.includes('failed') ? 'red' : 'green' }}>
          {message}
        </p>
      )}
    </div>
  );
}

export default RegisterForm;
