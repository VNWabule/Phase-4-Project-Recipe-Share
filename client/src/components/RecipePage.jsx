// src/components/RecipesPage.jsx
import React, { useEffect, useState } from "react";
import RecipeList from "./RecipeList";
import RecipeDetails from "./RecipeDetail";

function RecipesPage() {
  const [recipes, setRecipes] = useState([]);
  const [selectedRecipe, setSelectedRecipe] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5555/recipes") // adjust if your backend route is different
      .then((res) => res.json())
      .then(setRecipes)
      .catch((err) => console.error("Failed to fetch recipes:", err));
  }, []);

  return (
    <div className="recipes-page">
      <h2>Browse Recipes</h2>

      {selectedRecipe ? (
        <RecipeDetails recipe={selectedRecipe} onBack={() => setSelectedRecipe(null)} />
      ) : (
        <RecipeList recipes={recipes} onRecipeClick={setSelectedRecipe} />
      )}
    </div>
  );
}

export default RecipesPage;
