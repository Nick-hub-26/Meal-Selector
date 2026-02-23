import time
import random
preset_meals = [
    "jacket potato", "hot dog", "chilli con carne", "mac and cheese", "shepherds pie",
    "pasta bake", "bangers and mash", "spag bol", "yellow pasta", "pitta breads",
    "fajitas", "tacos", "fish and chips", "fish fingers", "soup", "batata aburro",
    "pizza", "stir fry noodles", "picadinho", "curry", "steak with eggs & chips",
    "cous cous", "lasagna"
]


def suspense():
    print("\nSelecting a meal from your list...")
    time.sleep(3)
    print("\nI got it!")
    time.sleep(1.5)
    
    
def pick_meal(meal_list):
    result = random.choice(meal_list).title()
    suspense()
    print(f"\nYou should have {result}")
    return result
    

#user side
print("Meal Selector")


while True:
    question = input("\nWould you like to use the preset list of meals? (y/n): ").strip().lower()
    if question != "y":
        user_meals = input("\nPlease enter the meals (seperated by commas): ")
        meal_list = [meal.strip() for meal in user_meals.split(',') if meal.strip()]
        
        if not meal_list:
            print("You didn't enter any meals. Try again!")
            continue
        pick_meal(meal_list)
    else:
        pick_meal(preset_meals)

        
        
        again = input("\nDo you want to pick another meal? (y/n): ").strip().lower()
        if again != "y":
            time.sleep(0.5)
            print("\nThank you for using the Meal Selector")
            time.sleep(0.5)
            print("Goodbye!")
            break
