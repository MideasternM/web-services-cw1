from app.db.database import Base, SessionLocal, engine
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe
from app.models.recipe_ingredient import RecipeIngredient


def seed_demo_data() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Recipe).count() > 0:
            return

        yogurt = Ingredient(
            name="Greek Yogurt",
            calories_per_100g=65,
            protein_per_100g=11,
            fat_per_100g=0.5,
            carbs_per_100g=4.0,
            contains_allergen=True,
            allergen_notes="milk",
        )
        banana = Ingredient(
            name="Banana",
            calories_per_100g=89,
            protein_per_100g=1.1,
            fat_per_100g=0.3,
            carbs_per_100g=22.8,
            contains_allergen=False,
            allergen_notes="",
        )
        oats = Ingredient(
            name="Rolled Oats",
            calories_per_100g=389,
            protein_per_100g=16.9,
            fat_per_100g=6.9,
            carbs_per_100g=66.3,
            contains_allergen=False,
            allergen_notes="",
        )
        db.add_all([yogurt, banana, oats])
        db.commit()
        db.refresh(yogurt)
        db.refresh(banana)
        db.refresh(oats)

        bowl = Recipe(
            name="Breakfast Bowl",
            description="Yogurt, banana, and oats",
            category="breakfast",
            difficulty="easy",
            servings=2,
            instructions="Combine all ingredients.",
        )
        db.add(bowl)
        db.commit()
        db.refresh(bowl)

        db.add_all(
            [
                RecipeIngredient(recipe_id=bowl.id, ingredient_id=yogurt.id, quantity_g=150),
                RecipeIngredient(recipe_id=bowl.id, ingredient_id=banana.id, quantity_g=100),
                RecipeIngredient(recipe_id=bowl.id, ingredient_id=oats.id, quantity_g=40),
            ]
        )
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_data()
