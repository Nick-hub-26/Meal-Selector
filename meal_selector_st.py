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
# Initialize session state
# -----------------------------
if "step" not in st.session_state:
    st.session_state.step = "start"  # start, picking, finished
if "planned_meals" not in st.session_state:
    st.session_state.planned_meals = []
if "current_meal" not in st.session_state:
    st.session_state.current_meal = None
if "total_meals" not in st.session_state:
    st.session_state.total_meals = 0
if "use_preset" not in st.session_state:
    st.session_state.use_preset = True

# -----------------------------
# App Title
# -----------------------------
st.title("🍴 Meal Selector & Planner 🍴")

# -----------------------------
# Step 1: Get number of meals and preset/custom choice
# -----------------------------
if st.session_state.step == "start":
    total_meals_input = st.number_input("How many meals would you like to plan?", min_value=1, step=1)
    use_preset_input = st.radio("Use the preset list of meals?", ("Yes", "No"))

    if st.button("Start Planning"):
        st.session_state.step = "picking"
        st.session_state.use_preset = (use_preset_input == "Yes")
        st.session_state.total_meals = total_meals_input
        st.session_state.planned_meals = []
        st.session_state.current_meal = None

# -----------------------------
# Step 2: Custom meals
# -----------------------------
elif st.session_state.step == "picking":
    if not st.session_state.use_preset:
        user_meals_input = st.text_input("Enter your meals (comma separated):")
        meal_list = [meal.strip().title() for meal in user_meals_input.split(',') if meal.strip()]

        if st.button("Generate Meal Plan"):
            if not meal_list:
                st.warning("You didn't enter any meals.")
            else:
                # Handle fewer meals than required
                if len(meal_list) < st.session_state.total_meals:
                    st.warning("Fewer meals than required; some meals may repeat.")
                    available = meal_list[:]
                    while len(st.session_state.planned_meals) < st.session_state.total_meals:
                        if not available:
                            available = meal_list[:]
                        choice = random.choice(available)
                        if choice not in st.session_state.planned_meals:
                            st.session_state.planned_meals.append(choice)
                            available.remove(choice)
                else:
                    random.shuffle(meal_list)
                    st.session_state.planned_meals = meal_list[:st.session_state.total_meals]

                st.subheader("📅 Your Meal Plan:")
                for i, meal in enumerate(st.session_state.planned_meals, start=1):
                    st.write(f"{i}. {meal}")
                st.success("Thank you for using the Meal Selector & Planner! 🍽️")
                st.session_state.step = "finished"

# -----------------------------
# Step 3: Preset meals with button confirmation
# -----------------------------
    else:
        if len(st.session_state.planned_meals) < st.session_state.total_meals:
            # Placeholder for suspense messages under the current meal
            meal_placeholder = st.empty()

            # pick a meal if current is None
            if st.session_state.current_meal is None:
                st.session_state.current_meal = pick_meal(preset_meals, st.session_state.planned_meals, meal_placeholder)

            st.write(f"Meal {len(st.session_state.planned_meals)+1} of {st.session_state.total_meals}: {st.session_state.current_meal}")

            col1, col2 = st.columns(2)
            add_btn = col1.button("Add to Plan")
            skip_btn = col2.button("Skip")

            if add_btn:
                st.session_state.planned_meals.append(st.session_state.current_meal)
                st.success(f"'{st.session_state.current_meal}' added to your plan.")
                st.session_state.current_meal = None  # pick next meal on next rerun
            elif skip_btn:
                st.info("Skipping this meal...")
                st.session_state.current_meal = None  # pick next meal on next rerun

        else:
            # finished
            st.subheader("📅 Your Meal Plan:")
            for i, meal in enumerate(st.session_state.planned_meals, start=1):
                st.write(f"{i}. {meal}")
            st.success("Thank you for using the Meal Selector & Planner! 🍽️")
            st.session_state.step = "finished"
