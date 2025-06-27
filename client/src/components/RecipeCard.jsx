// src/components/RecipeCard.jsx
import React from "react";
import "./RecipeCard.css";

function RecipeCard({ recipe, onClick }) {
  return (
    <div className="recipe-card" onClick={() => onClick(recipe)}>
      <img src={recipe.image_url} alt={recipe.title} className="recipe-card-image" />
      <h3 className="recipe-card-title">{recipe.title}</h3>
      <p className="recipe-card-avg-rating">
        ⭐ {recipe.average_rating ? recipe.average_rating.toFixed(1) : "No rating yet"}
      </p>

    </div>
  );
}

export default RecipeCard;
