import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

import Navbar from "./components/Navbar";
import LoginForm from "./components/LoginForm";
import RegisterForm from "./components/RegisterForm";
import RecipePage from "./components/RecipePage";
import RecipeDetail from "./components/RecipeDetail";
import ResetPassword from "./components/ResetPassword";
import ForgotPassword from "./components/ForgotPassword";
import AddRecipeForm from "./components/AddRecipeForm";
import BookmarkList from "./components/BookmarkList";

import { checkSession } from "./api/axios";
import "./App.css";

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const accessToken = localStorage.getItem("access_token");

    if (accessToken) {
      fetch("http://localhost:5555/check_session", {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        credentials: "include",
      })
        .then((r) => {
          if (r.ok) return r.json();
          throw new Error("Invalid token");
        })
        .then((data) => setUser(data.user))
        .catch(() => {
          fetch("http://localhost:5555/refresh", {
            method: "POST",
            credentials: "include",
          })
            .then((res) => res.json())
            .then((data) => {
              if (data.access_token) {
                localStorage.setItem("access_token", data.access_token);
                return fetch("http://localhost:5555/check_session", {
                  headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${data.access_token}`,
                  },
                  credentials: "include",
                });
              }
              throw new Error("Unable to refresh");
            })
            .then((res) => res.json())
            .then((data) => setUser(data.user))
            .catch(() => setUser(null));
        });
    } else {
      setUser(null);
    }
  }, []);

  return (
    <Router>
      <div className="App">
        <Navbar user={user} setUser={setUser} />

        <Routes>
          <Route path="/" element={<RecipePage />} />
          <Route
            path="/login"
            element={!user ? <LoginForm setUser={setUser} /> : <Navigate to="/" />}
          />
          <Route
            path="/register"
            element={!user ? <RegisterForm setUser={setUser} /> : <Navigate to="/" />}
          />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/recipes/:id" element={<RecipeDetail user={user} />} />

          
          <Route
            path="/bookmarks"
            element={user ? <BookmarkList /> : <Navigate to="/login" />}
          />
          <Route
            path="/add-recipe"
            element={user ? <AddRecipeForm /> : <Navigate to="/login" />}
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
