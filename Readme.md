# 🍽️ Recipe Share

A full-stack recipe sharing application built with a **Flask REST API backend** and a **React frontend**. Users can browse and try recipes, with support for authentication.

---

## 📁 Project Structure

- **Backend**: Flask, SQLAlchemy, JWT
- **Frontend**: React, React Router

---

## 🔧 Setup Instructions

### ✅ Prerequisites

- Python 3.8+
- PostgreSQL
- Flask
- React

---

## ⚙️ Backend Setup (Flask)

1. **Clone the repo**
    ```bash
    git clone git@github.com:VNWabule/Phase-4-Project-Recipe-Share.git
    cd Phase-4-Project-Recipe-Share

2. **Create a virtual environment**
    ```bash
    pipenv install
    pipenv shell

3. **Install dependencies**
    ```bash
    pipenv install flask flask-sqlalchemy flask-migrate flask-cors
    flask-bycryt flask-restful sqlalchemy-serializer pyjwt psycopg2-binary

4. **Create PostgreSQL database:**
    ```bash
    createdb recipe_share_db

5. **Run migrations**
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade

6. **Seed data**
    ```bash
    python -m server.seed

7. **Run the Server**
    ```bash
    python -m server.app

---

## 🎨 Frontend Setup (React)

1. **Navigate to the client/ directory**
    ```bash
    cd client

2. **Install dependencies:**
    ```bash
    npm install

3. **Run the Frontend**
    ```bash
    npm run dev

---

## 🧠 Features

- User authentication with JWT
- Recipe creation and viewing
- Bookmark recipes 
- Responsive design with client-side routing

---

## 🧩 Models Overview

**User:**
- One-to-many: Recipes, Bookmarks

**Recipe:**
- One-to-many: Owned by a User, Bookmarked by many Users

**Bookmark (association table)**
- Many-to-many: Users ↔ Recipes

--- 

## 🔁 Routes Overview

### Backend

- POST /login
- POST /signup
- GET /recipes
- POST /recipes
- DELETE /recipes/:id
- GET /bookmarks
- POST /bookmarks
- DELETE /bookmarks/:id

### Frontend

- / – Home / Recipe list
- /login – Login form
- /register – Signup form
- /recipes/:id – Recipe detail
- /bookmarks – Bookmarked recipes

---

## 🔐 Security

- Passwords are hashed with werkzeug.security
- JWT is used for auth with access & refresh tokens
- Secure cookie settings for production-ready deployment

---

## 🚀 Future Improvements

- Recipe image uploads
- User profiles
- Recipe categories or tags
- Advanced search and filters
- bookmark notes
