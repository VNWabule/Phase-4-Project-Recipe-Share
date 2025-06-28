from .app import app
from .models import db, User, Recipe, Comment, Bookmark

with app.app_context():
    print("🔄 Dropping and recreating all tables...")
    db.drop_all()
    db.create_all()

    # Sample users
    user1 = User(username='chefemma', email='emma@example.com')
    user1.password = "securepassword123"

    user2 = User(username='foodiejoe', email='joe@example.com')
    user2.password = "ilovefood456"

    user3 = User(username='bakerlisa', email='lisa@example.com')
    user3.password = "sweettooth789"

    db.session.add_all([user1, user2, user3])
    db.session.commit()

    # Sample recipes
    recipes = [
        Recipe(
            title="Spaghetti Carbonara",
            ingredients="Spaghetti, eggs, pancetta, pecorino cheese, pepper",
            instructions="Boil pasta. Fry pancetta. Mix eggs and cheese. Combine all.",
            cook_time=20,
            image_url="https://www.shutterstock.com/image-photo/spaghetti-alla-carbonara-sauce-classic-600nw-2570098411.jpg",
            average_rating=4.5,
            user=user1
        ),
        Recipe(
            title="Classic Margherita Pizza",
            ingredients="Pizza dough, tomatoes, mozzarella, basil, olive oil",
            instructions="Roll dough. Spread tomato sauce. Add cheese and basil. Bake.",
            cook_time=30,
            image_url="https://media.istockphoto.com/id/1280329631/photo/italian-pizza-margherita-with-tomatoes-and-mozzarella-cheese-on-wooden-cutting-board-close-up.jpg?s=612x612&w=0&k=20&c=CFDDjavIC5l8Zska16UZRZDXDwd47fwmRsUNzY0Ym6o=",
            average_rating=4.8,
            user=user2
        ),
        Recipe(
            title="Blueberry Pancakes",
            ingredients="Flour, eggs, milk, baking powder, blueberries, butter",
            instructions="Mix ingredients. Pour on griddle. Flip. Serve warm with syrup.",
            cook_time=15,
            image_url="https://media.istockphoto.com/id/925701856/photo/stack-of-freshly-prepared-blueberry-ricotta-pancakes.jpg?s=612x612&w=0&k=20&c=vVqS5xUIJiQQsmNTuOI0N_tfwglVwZVYzDZdEADy5o8=",
            average_rating=4.2,
            user=user3
        ),
        Recipe(
            title="Chicken Tikka Masala",
            ingredients="Chicken, yogurt, spices, tomatoes, cream, garlic, ginger",
            instructions="Marinate chicken. Grill. Simmer in sauce. Serve with rice or naan.",
            cook_time=40,
            image_url="https://www.shutterstock.com/image-photo/indian-curry-tikka-masala-chicken-600nw-2444442353.jpg",
            average_rating=4.9,
            user=user1
        ),
        Recipe(
            title="Avocado Toast with Egg",
            ingredients="Bread, avocado, egg, lemon juice, chili flakes",
            instructions="Toast bread. Mash avocado. Fry egg. Assemble and season.",
            cook_time=10,
            image_url="https://media.istockphoto.com/id/1990163130/photo/healthy-homemade-rustic-breakfast-toast-with-avocado-and-boiled-egg.jpg?s=612x612&w=0&k=20&c=JclSvvLXJZejizsrBg3kuA-uyUdMCojO-I4dxPcbiL0=",
            average_rating=4.0,
            user=user2
        )
    ]

    db.session.add_all(recipes)
    db.session.commit()

    # sample comments
    comments = [
        Comment(content="Looks delicious!", user=user2, recipe=recipes[0]),
        Comment(content="Tried it—came out perfect.", user=user3, recipe=recipes[0]),
        Comment(content="My kids loved this one!", user=user1, recipe=recipes[2]),
        Comment(content="Nice and easy breakfast recipe!", user=user3, recipe=recipes[4]),
        Comment(content="This tikka masala is amazing!", user=user2, recipe=recipes[3]),
    ]

    db.session.add_all(comments)

    # bookmarks (users saving recipes)
    bookmarks = [
        Bookmark(user=user1, recipe=recipes[1]),
        Bookmark(user=user2, recipe=recipes[0]),
        Bookmark(user=user3, recipe=recipes[3]),
        Bookmark(user=user3, recipe=recipes[2]),
    ]

    db.session.add_all(bookmarks)
    db.session.commit()

    print("✅ Database seeded with users, recipes, comments, images, ratings, and bookmarks.")
