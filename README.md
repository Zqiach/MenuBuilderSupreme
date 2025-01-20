# Menu Builder Supreme

Menu Builder Supreme is a Streamlit-based application that allows users to plan weekly menus, generate recipes using Amazon Bedrock AI models, and create grocery lists from the planned meals. The application is designed to showcase the integration of AI-powered services with a simple, user-friendly interface. This project is a learning tool to demonstrate the art of the possible with Amazon Bedrock.

## Features

- **Weekly Menu Planning**: 
  - Users can plan lunch and dinner for each day of the week.
  - Options to mark days as "Eat Out" for convenience.

- **AI-Powered Recipe Generation**:
  - Leverages Amazon Bedrock for generating recipes based on user-defined parameters like cuisine, protein, spice level, and creativity.
  - Provides both AI-generated and manual input options for recipes.

- **Dynamic Grocery List Creation**:
  - Automatically aggregates ingredients from planned meals.
  - Removes duplicates and combines quantities for similar items.
  - Allows users to download the grocery list as a PDF.

- **Streamlined User Experience**:
  - Persistent data across pages for seamless navigation.
  - Clear separation of AI-generated content and manual inputs.
  - Expandable sections for lunch and dinner to avoid overwhelming users.

## Project Structure

```
MenuBuilderSupreme/
├── .venv/                  # Virtual environment (not included in version control)
├── pages/                  # Streamlit pages for multi-page app
│   ├── 1_View_Menu.py      # Displays planned menu for the week
│   ├── 2_View_Grocery_List.py  # Generates and displays grocery list
├── app.py                  # Main application page for menu planning
├── requirements.txt        # Python dependencies for the project
├── README.md               # Project documentation
└── assets/                 # Assets such as images or logos
```

## How to Run the App

1. **Set Up Environment**:
   - Install Python (version 3.8 or later).
   - Create a virtual environment and activate it:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate  # Windows
     source .venv/bin/activate  # macOS/Linux
     ```

2. **Install Dependencies**:
   - Install the required Python libraries:
     ```bash
     pip install -r requirements.txt
     ```

3. **Run the Application**:
   - Start the Streamlit server:
     ```bash
     streamlit run app.py
     ```
   - Open the application in your browser at `http://localhost:8501`.

## Functionality Overview

### Main Page (`app.py`):
- **Tabs for Days of the Week**: Each day has dedicated sections for lunch and dinner.
- **AI Assistance**:
  - Users can customize parameters (e.g., cuisine, protein, spice level) before generating recipes.
  - Generated recipes include titles, descriptions, ingredients, and instructions.
- **Manual Input**:
  - Users can manually input and edit recipe details.

### View Menu Page (`pages/1_View_Menu.py`):
- Displays the planned menu for the week.
- Includes a button to download the menu as a PDF.

### Grocery List Page (`pages/2_View_Grocery_List.py`):
- Aggregates ingredients from all planned recipes.
- Handles duplicate items and combines quantities.
- Provides an option to download the grocery list as a PDF.

## Future Enhancements
- **Advanced AI Features**:
  - Support for image generation for recipes.
  - Additional Bedrock model integrations.
- **Category-based Grocery Sorting**:
  - Automatically organize items into categories (e.g., Produce, Meats, Pantry).
- **Multi-User Support**:
  - Add user authentication and profiles.
- **Mobile Optimization**:
  - Improve the UI for better mobile responsiveness.

## Technologies Used
- **Streamlit**: For building the web application.
- **Amazon Bedrock**: For AI-powered recipe generation.
- **FPDF**: For generating downloadable PDFs.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- Thanks to Amazon Bedrock for providing AI capabilities.
- Streamlit for their powerful, easy-to-use framework for creating interactive web apps.

---

Enjoy planning your weekly meals with Menu Builder Supreme!
