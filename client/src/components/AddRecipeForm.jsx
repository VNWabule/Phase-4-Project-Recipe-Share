import React, { useState } from 'react';
import './FormStyles.css';

function AddRecipeForm({ onAdd }) {
  const [form, setForm] = useState({
    title: '',
    ingredients: '',
    instructions: '',
    cook_time: '',
    image_url: ''
  });

  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState(''); // "success" or "error"

  const accessToken = localStorage.getItem('access_token');

  if (!accessToken) {
    return (
      <div className="form-container">
        <p className="error-message">You must be logged in to add a recipe.</p>
      </div>
    );
  }

  function handleChange(e) {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  }

  async function handleSubmit(e) {
    e.preventDefault();

    setMessage('');
    setMessageType('');

    try {
      const res = await fetch('https://phase-4-project-recipe-share-backend.onrender.com/recipes', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${accessToken}`
        },
        credentials: 'include',
        body: JSON.stringify(form),
      });

      const data = await res.json();

      if (res.ok) {
        setMessage('Recipe added successfully!');
        setMessageType('success');
        setForm({
          title: '',
          ingredients: '',
          instructions: '',
          cook_time: '',
          image_url: ''
        });
        onAdd && onAdd(data); // Optional callback
      } else {
        throw new Error(data.error || 'Failed to add recipe.');
      }
    } catch (err) {
      setMessage(err.message);
      setMessageType('error');
    }
  }

  return (
    <div className="form-container">
      <h2>Add New Recipe</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Title</label>
          <input
            id="title"
            name="title"
            placeholder="Recipe title"
            value={form.title}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="ingredients">Ingredients</label>
          <textarea
            id="ingredients"
            name="ingredients"
            placeholder="List ingredients"
            value={form.ingredients}
            onChange={handleChange}
            required
            rows={4}
          />
        </div>

        <div className="form-group">
          <label htmlFor="instructions">Instructions</label>
          <textarea
            id="instructions"
            name="instructions"
            placeholder="Cooking steps"
            value={form.instructions}
            onChange={handleChange}
            required
            rows={5}
          />
        </div>

        <div className="form-group">
          <label htmlFor="cook_time">Cook Time (minutes)</label>
          <input
            type="number"
            id="cook_time"
            name="cook_time"
            placeholder="e.g., 30"
            value={form.cook_time}
            onChange={handleChange}
            min="0"
          />
        </div>

        <div className="form-group">
          <label htmlFor="image_url">Image URL</label>
          <input
            id="image_url"
            name="image_url"
            placeholder="Optional image URL"
            value={form.image_url}
            onChange={handleChange}
          />
        </div>

        <button className="submit-btn" type="submit">Add Recipe</button>
      </form>

      {message && (
        <p className={messageType === 'success' ? 'success-message' : 'error-message'}>
          {message}
        </p>
      )}
    </div>
  );
}

export default AddRecipeForm;
