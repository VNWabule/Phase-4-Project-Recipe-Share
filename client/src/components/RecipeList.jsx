// src/components/RecipeList.jsx
import React from "react";
import RecipeCard from "./RecipeCard";

function RecipeList({ recipes, onRecipeClick }) {
  return (
    <div className="recipe-list">
      {recipes.map((recipe) => (
        <RecipeCard key={recipe.id} recipe={recipe} onClick={onRecipeClick} />
      ))}
    </div>
  );
}

export default RecipeList;
