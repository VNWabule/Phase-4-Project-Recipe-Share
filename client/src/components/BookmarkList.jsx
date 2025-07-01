// src/components/BookmarkList.jsx
import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function BookmarkList() {
  const [bookmarks, setBookmarks] = useState([]);
  const [error, setError] = useState("");

  const token = localStorage.getItem("access_token");

  useEffect(() => {
    fetch("http://localhost:5555/bookmarks", {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      credentials: "include",
    })
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch bookmarks.");
        return res.json();
      })
      .then((data) => setBookmarks(data))
      .catch((err) => setError(err.message));
  }, []);

  function handleRemove(bookmarkId) {
    fetch(`https://phase-4-project-recipe-share-backend.onrender.com/bookmarks/${bookmarkId}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      credentials: "include",
    })
      .then((res) => {
        if (!res.ok) throw new Error("Failed to remove bookmark.");
        setBookmarks((prev) => prev.filter((b) => b.id !== bookmarkId));
      })
      .catch((err) => setError(err.message));
  }

  return (
    <div className="bookmark-list">
      <h2>Bookmarked Recipes</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}

      {bookmarks.length === 0 ? (
        <p>You have no bookmarks yet.</p>
      ) : (
        <ul style={{ listStyle: "none", padding: 0 }}>
          {bookmarks.map((bookmark) => (
            <li key={bookmark.id} style={{ marginBottom: "1.5rem" }}>
              <Link to={`/recipes/${bookmark.recipe?.id}`}>
                <h3>{bookmark.recipe?.title || "Untitled Recipe"}</h3>
              </Link>

              {bookmark.recipe?.image_url && (
                <img
                  src={bookmark.recipe.image_url}
                  alt={bookmark.recipe.title}
                  style={{ width: "150px", borderRadius: "8px" }}
                />
              )}

              {bookmark.notes && (
                <p>
                  <strong>Notes:</strong> {bookmark.notes}
                </p>
              )}

              <button
                onClick={() => handleRemove(bookmark.id)}
                className="remove-btn"
                style={{
                  background: "#cc0000",
                  color: "white",
                  border: "none",
                  padding: "6px 12px",
                  cursor: "pointer",
                  marginTop: "0.5rem",
                }}
              >
                ✖ Remove
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default BookmarkList;
