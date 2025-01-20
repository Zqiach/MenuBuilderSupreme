import streamlit as st
from fpdf import FPDF
from collections import defaultdict
import io


# Helper function to aggregate ingredients
def aggregate_ingredients(menu_data):
    grocery_list = defaultdict(float)  # Default values are floats to handle quantities
    unmatched_items = []  # For items without quantities or units

    for day, meals in menu_data.items():
        if meals.get("eat_out"):
            continue  # Skip days marked as "Eat Out"

        for meal_type in ["lunch", "dinner"]:
            meal = meals.get(meal_type, {})
            ingredients = meal.get("ingredients", [])

            for item in ingredients:
                if not item.strip():  # Skip empty lines
                    continue

                # Attempt to parse quantity and item
                try:
                    parts = item.split(maxsplit=1)
                    quantity = float(parts[0])  # Extract quantity
                    ingredient = parts[1].strip().lower()  # Normalize ingredient name
                    grocery_list[ingredient] += quantity
                except (IndexError, ValueError):
                    # If parsing fails, add the item to unmatched items
                    unmatched_items.append(item.strip().lower())

    return grocery_list, unmatched_items


# Helper function to generate the grocery list PDF
def generate_grocery_pdf(grocery_list, unmatched_items):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=16)

    # Title
    pdf.cell(200, 10, txt="Grocery List", ln=True, align="C")
    pdf.ln(10)

    # Add aggregated items
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Consolidated Items:", ln=True)
    for ingredient, quantity in grocery_list.items():
        pdf.cell(200, 10, txt=f"- {quantity} {ingredient}", ln=True)

    pdf.ln(10)

    # Add unmatched items
    if unmatched_items:
        pdf.cell(200, 10, txt="Unmatched Items:", ln=True)
        for item in unmatched_items:
            pdf.cell(200, 10, txt=f"- {item}", ln=True)

    # Save to a BytesIO buffer
    pdf_output = io.BytesIO()
    pdf_content = pdf.output(dest="S").encode("latin1")  # Get PDF as binary string
    pdf_output.write(pdf_content)
    pdf_output.seek(0)  # Reset buffer pointer to the beginning
    return pdf_output


# Streamlit Page
st.title("Grocery List")
st.subheader("Here’s your consolidated grocery list!")

# Check if menu data exists
if "menu_data" in st.session_state:
    menu_data = st.session_state.menu_data

    # Aggregate ingredients
    grocery_list, unmatched_items = aggregate_ingredients(menu_data)

    # Display the grocery list
    st.header("Consolidated Grocery List")
    if grocery_list:
        for ingredient, quantity in grocery_list.items():
            st.write(f"- {quantity} {ingredient}")
    else:
        st.write("No ingredients found in the menu.")

    # Display unmatched items
    if unmatched_items:
        st.header("Unmatched Items")
        st.write("These items could not be aggregated:")
        for item in unmatched_items:
            st.write(f"- {item}")

    # Add a download button for the grocery list PDF
    pdf_file = generate_grocery_pdf(grocery_list, unmatched_items)
    st.download_button(
        label="Download Grocery List as PDF",
        data=pdf_file,
        file_name="grocery_list.pdf",
        mime="application/pdf"
    )
else:
    st.warning("No menu data available. Please return to the main page and plan your menu.")
