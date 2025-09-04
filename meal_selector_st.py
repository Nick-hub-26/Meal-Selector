import streamlit as st
import random
import time

# -----------------------------
# Preset meals
# -----------------------------
preset_meals = [
    "jacket potato", "hot dogs", "chilli con carne", "mac and cheese", "shepherds pie",
    "pasta bake", "bangers and mash", "spag bol", "yellow pasta", "pitta breads",
    "fajitas", "tacos", "fish and chips", "fish fingers", "soup", "batata aburro",
    "pizza", "stir fry noodles", "picadinho", "curry", "steak with eggs & chips",
    "cous cous", "lasagna"
]

# -----------------------------
# Suspense function
# -----------------------------
def suspense(placeholder, message="Selecting a meal..."):
    placeholder.text(message)
    time.sleep(1.5)
    placeholder.text("I got it!")
    time.sleep(1)

# -----------------------------
# Pick a random meal
# -----------------------------
def pick_meal(meal_list, used_meals, placeholder):
    available = [m for m in meal_list if m.title() not in used_meals]
    if not available:
        available = meal_list
    result = random.choice(available).title()
    suspense(placeholder)
    return result

# -----------------------------
# Streamlit App
# -----------------------------
st.title("🍴 Meal Selector & Planner 🍴")

# Step 1: Number of meals
total_meals = st.number_input("How many meals would you like to plan?", min_value=1, step=1)

# Step 2: Preset or custom
use_preset = st.radio("Use the preset list of meals?", ("Yes", "No"))

planned_meals = []
placeholder = st.empty()

if st.button("Generate Meal Plan"):
    if use_preset == "No":
        # Custom meals
        user_meals_input = st.text_input("Enter your meals (comma separated):")
        meal_list = [meal.strip().title() for meal in user_meals_input.split(',') if meal.strip()]

        if not meal_list:
            st.warning("You didn't enter any meals.")
        else:
            if len(meal_list) < total_meals:
                st.warning("Fewer meals than required; some meals may repeat.")
                available = meal_list[:]
                while len(planned_meals) < total_meals:
                    if not available:
                        available = meal_list[:]
                    choice = random.choice(available)
                    if choice not in planned_meals:
                        planned_meals.append(choice)
                        available.remove(choice)
            else:
                random.shuffle(meal_list)
                planned_meals = meal_list[:total_meals]
    else:
        # Preset meals mode
        while len(planned_meals) < total_meals:
            st.write(f"Meal {len(planned_meals)+1} of {total_meals}")
            meal = pick_meal(preset_meals, planned_meals, placeholder)
            confirm = st.radio(f"Do you want to add '{meal}' to your meal plan?", ("Yes", "No"), key=len(planned_meals))
            if confirm == "Yes":
                if meal not in planned_meals:
                    planned_meals.append(meal)
                    st.success(f"'{meal}' added to your plan.")
            else:
                st.info("Trying another meal...")

    # Show final plan
    st.subheader("📅 Your Meal Plan:")
    for i, meal in enumerate(planned_meals, start=1):
        st.write(f"{i}. {meal}")

    st.write("Thank you for using the Meal Selector & Planner! 🍽️")
