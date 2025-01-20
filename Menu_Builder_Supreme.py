import streamlit as st
from bedrock_helper import generate_recipe_with_claude_haiku

# Title and App Info
st.title("Menu Builder Supreme")
st.subheader("Plan Your Weekly Menu with Ease")

# Days of the week and default options
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
default_cuisines = ["Italian", "Mexican", "Indian", "American", "Chinese", "Japanese", "Mediterranean"]
default_proteins = ["Chicken", "Beef", "Pork", "Fish", "Tofu", "Lamb", "Vegetarian"]
default_spice_levels = ["Mild", "Medium", "Spicy"]

# Initialize session state for menu data
if "menu_data" not in st.session_state:
    st.session_state.menu_data = {
        day: {
            "lunch": {"cuisine": "", "protein": "", "creativity": 0.7, "title": "", "description": "", "ingredients": [], "instructions": "", "ai_generated": False},
            "dinner": {"cuisine": "", "protein": "", "creativity": 0.7, "title": "", "description": "", "ingredients": [], "instructions": "", "ai_generated": False},
            "eat_out": False,
        }
        for day in days_of_week
    }

# Function to handle menu input
def menu_input(day, meal_type):
    """Handles AI and manual inputs for a meal."""
    meal = st.session_state.menu_data[day][meal_type]

    # AI Assistance Section
    st.subheader(f"AI Assistance for {meal_type.capitalize()} on {day}")
    if st.checkbox(f"Enable AI Assistance for {meal_type.capitalize()} on {day}", key=f"{day}_{meal_type}_ai_enabled"):
        st.write("**Customize AI Parameters**")
        
        # User inputs for AI generation
        ai_food_type = st.selectbox(f"Type of Food for {meal_type.capitalize()}:", default_cuisines, key=f"{day}_{meal_type}_food_type")
        ai_protein = st.selectbox(f"Protein for {meal_type.capitalize()}:", default_proteins, key=f"{day}_{meal_type}_protein")
        ai_spice_level = st.selectbox(f"Spice Level for {meal_type.capitalize()}:", default_spice_levels, key=f"{day}_{meal_type}_spice_level")
        ai_randomness = st.slider(f"Randomness Level (Temperature) for {meal_type.capitalize()}:", 0.1, 1.0, 0.7, 0.1, key=f"{day}_{meal_type}_randomness")
        
        if st.button(f"Generate AI {meal_type.capitalize()} Recipe for {day}", key=f"{day}_{meal_type}_ai_generate"):
            # Generate recipe using Bedrock
            recipe = generate_recipe_with_claude_haiku(
                cuisine=ai_food_type,
                protein=ai_protein,
                spice_level=ai_spice_level,
                temperature=ai_randomness
            )

            # Save the AI-generated recipe to session state
            meal["title"] = recipe["title"]
            meal["description"] = recipe["description"]
            meal["ingredients"] = recipe["ingredients"]
            meal["instructions"] = recipe["instructions"]
            meal["ai_generated"] = True
            st.success(f"AI {meal_type.capitalize()} recipe generated!")

    # Manual Input Section
    st.subheader(f"Manual Input for {meal_type.capitalize()} on {day}")
    meal["title"] = st.text_input(
        f"{meal_type.capitalize()} Title:",
        value=meal["title"],
        placeholder=f"e.g., {'Grilled Chicken Caesar Salad' if meal_type == 'lunch' else 'Spaghetti Bolognese'}",
        key=f"{day}_{meal_type}_title",
    )
    meal["description"] = st.text_area(
        f"{meal_type.capitalize()} Description:",
        value=meal["description"],
        placeholder=f"e.g., {'A light salad with grilled chicken...' if meal_type == 'lunch' else 'A hearty Italian dish...'}",
        key=f"{day}_{meal_type}_description",
    )
    meal["ingredients"] = st.text_area(
        f"{meal_type.capitalize()} Ingredients (one per line):",
        value="\n".join(meal["ingredients"]),
        placeholder="e.g.,\n- 1 lb chicken breast\n- 1 head romaine lettuce\n- Caesar dressing",
        key=f"{day}_{meal_type}_ingredients",
    ).split("\n")
    meal["instructions"] = st.text_area(
        f"{meal_type.capitalize()} Instructions:",
        value=meal["instructions"],
        placeholder="e.g.,\n1. Grill the chicken breast.\n2. Chop the romaine lettuce.\n3. Mix lettuce, chicken, and dressing.",
        key=f"{day}_{meal_type}_instructions",
    )


# Create tabs for each day of the week
tabs = st.tabs(days_of_week)

for day, tab in zip(days_of_week, tabs):
    with tab:
        st.header(f"{day}'s Menu")

        # Eat Out Toggle
        st.session_state.menu_data[day]["eat_out"] = st.checkbox(
            f"Eat Out on {day}",
            value=st.session_state.menu_data[day]["eat_out"],
            key=f"{day}_eat_out",
        )

        if st.session_state.menu_data[day]["eat_out"]:
            st.info(f"{day} is marked as 'Eat Out'. No selections available.")
        else:
            # Lunch Section
            with st.expander("Lunch Section"):
                menu_input(day, "lunch")

            # Dinner Section
            with st.expander("Dinner Section"):
                menu_input(day, "dinner")

# Footer
st.write("---")
st.caption("Powered by Streamlit")
