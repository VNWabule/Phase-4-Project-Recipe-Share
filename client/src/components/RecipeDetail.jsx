import React, { useState, useEffect } from "react";
import CommentSection from "./CommentSection";

function RecipeDetails({ recipe, onBack, user }) {
  const [comments, setComments] = useState(recipe?.comments || []);
  const [newComment, setNewComment] = useState("");
  const [bookmarkMessage, setBookmarkMessage] = useState("");

  useEffect(() => {
    if (recipe?.id) {
      fetch(`http://127.0.0.1:5555/recipes/${recipe.id}/comments`)
        .then((res) => res.json())
        .then((data) => setComments(data))
        .catch((err) => console.error("Failed to fetch comments", err));
    }
  }, [recipe?.id]);

  const handleCommentSubmit = (e) => {
    e.preventDefault();

    if (!newComment.trim()) return;

    const payload = {
      recipe_id: recipe.id,
      content: newComment,
    };

    fetch("http://127.0.0.1:5555/comments", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
      body: JSON.stringify(payload),
    })
      .then((res) => {
        if (!res.ok) throw new Error("Failed to post comment");
        return res.json();
      })
      .then((newCommentObj) => {
        setComments([...comments, newCommentObj]);
        setNewComment("");
      })
      .catch((err) => console.error(err));
  };

  const handleCommentDelete = (commentId) => {
    fetch(`http://127.0.0.1:5555/comments/${commentId}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Failed to delete comment");
        setComments(comments.filter((c) => c.id !== commentId));
      })
      .catch((err) => console.error(err));
  };

  const handleBookmark = () => {
    const accessToken = localStorage.getItem("access_token");
    if (!accessToken || !user) {
      setBookmarkMessage("You must be logged in to bookmark.");
      return;
    }

    fetch("http://127.0.0.1:5555/bookmarks", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
      body: JSON.stringify({ recipe_id: recipe.id }),
    })
      .then((res) => {
        if (!res.ok) throw new Error("Bookmark failed.");
        return res.json();
      })
      .then(() => setBookmarkMessage("✔️ Recipe bookmarked!"))
      .catch(() => setBookmarkMessage("⚠️ You already bookmarked this recipe."));
  };

  if (!recipe) return <p>Loading recipe...</p>;

  return (
    <div className="recipe-details" style={{ maxWidth: "800px", margin: "2rem auto", padding: "1rem" }}>
      <button onClick={onBack} style={{ marginBottom: "1rem", padding: "0.5rem", borderRadius: "4px" }}>
        ← Back to Recipes
      </button>

      {recipe.image_url && (
        <img
          src={recipe.image_url}
          alt={recipe.title}
          style={{ width: "100%", height: "auto", borderRadius: "8px", marginBottom: "1rem" }}
        />
      )}

      <h2>{recipe.title}</h2>
      <p><strong>Created by:</strong> {recipe.user?.username || "Unknown Chef"}</p>

      <p>
        <strong>Rating:</strong>{" "}
        {Array(5).fill("★").map((star, index) => (
          <span key={index} style={{ color: index < Math.round(recipe.average_rating) ? "gold" : "#ccc" }}>
            {star}
          </span>
        ))} ({recipe.average_rating?.toFixed(1)})
      </p>

      {/* 🔖 Bookmark Button */}
      {user && (
        <>
          <button onClick={handleBookmark} style={{ margin: "0.5rem 0", padding: "0.5rem 1rem", borderRadius: "5px" }}>
            📌 Bookmark Recipe
          </button>
          {bookmarkMessage && (
            <p style={{ color: bookmarkMessage.includes("✔️") ? "green" : "red", marginTop: "0.5rem" }}>
              {bookmarkMessage}
            </p>
          )}
        </>
      )}

      <p><strong>Ingredients:</strong> {recipe.ingredients}</p>
      <p><strong>Instructions:</strong> {recipe.instructions}</p>
      <p><strong>Cook time:</strong> {recipe.cook_time} minutes</p>

      <div style={{ marginTop: "2rem" }}>
        <CommentSection
          comments={comments}
          currentUser={user}
          onDelete={handleCommentDelete}
        />

        <form onSubmit={handleCommentSubmit} style={{ marginTop: "1rem" }}>
          <textarea
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            placeholder="Leave a comment..."
            rows="3"
            style={{ width: "100%", padding: "0.5rem", borderRadius: "4px", border: "1px solid #ccc" }}
          />
          <button type="submit" style={{ marginTop: "0.5rem", padding: "0.5rem 1rem" }}>
            Post Comment
          </button>
        </form>
      </div>
    </div>
  );
}

export default RecipeDetails;
