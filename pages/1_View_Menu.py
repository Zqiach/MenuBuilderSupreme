import io
from fpdf import FPDF
import re
import streamlit as st


# Function to sanitize text for FPDF
def sanitize_text(text):
    """Remove or replace unsupported characters for FPDF."""
    # Remove all characters that can't be encoded in Latin-1
    sanitized = re.sub(r'[^\x00-\xFF]', '', text)
    return sanitized


# Updated function to generate the PDF
def generate_pdf(menu_data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=16)

    # Title
    pdf.cell(200, 10, txt="Weekly Menu", ln=True, align="C")
    pdf.ln(10)

    # Add menu details
    for day, meals in menu_data.items():
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(200, 10, txt=sanitize_text(day), ln=True)

        # Lunch
        pdf.set_font("Arial", size=12)
        if meals.get("eat_out"):
            pdf.cell(200, 10, txt=sanitize_text("Lunch: Eat Out"), ln=True)
            pdf.cell(200, 10, txt=sanitize_text("Dinner: Eat Out"), ln=True)
        else:
            lunch_title = meals.get("lunch", {}).get("title", "No Recipe Selected")
            pdf.cell(200, 10, txt=sanitize_text(f"Lunch: {lunch_title}"), ln=True)

            dinner_title = meals.get("dinner", {}).get("title", "No Recipe Selected")
            pdf.cell(200, 10, txt=sanitize_text(f"Dinner: {dinner_title}"), ln=True)

        pdf.ln(5)

    # Save the PDF to a BytesIO buffer
    pdf_output = io.BytesIO()
    pdf_content = pdf.output(dest="S").encode("latin1")  # Get PDF as binary string
    pdf_output.write(pdf_content)
    pdf_output.seek(0)  # Reset buffer pointer to the beginning
    return pdf_output


# Streamlit Page
st.title("View Weekly Menu")
st.subheader("Here’s what you’ve planned for the week!")

# Check if menu data exists
if "menu_data" in st.session_state:
    menu_data = st.session_state.menu_data

    # Display the menu
    for day, meals in menu_data.items():
        st.header(day)

        # Display "Eat Out" status or menu items
        if meals.get("eat_out"):
            st.write("### Lunch: 🍴 Eat Out")
            st.write("### Dinner: 🍴 Eat Out")
        else:
            lunch_title = meals.get("lunch", {}).get("title", "No Recipe Selected")
            st.write(f"### Lunch: {lunch_title}")
            dinner_title = meals.get("dinner", {}).get("title", "No Recipe Selected")
            st.write(f"### Dinner: {dinner_title}")

        st.write("---")

    # Button to download menu as a PDF
    pdf_file = generate_pdf(menu_data)
    st.download_button(
        label="Download Menu as PDF",
        data=pdf_file,
        file_name="weekly_menu.pdf",
        mime="application/pdf"
    )
else:
    st.warning("No menu data available. Please return to the main page and plan your menu.")
