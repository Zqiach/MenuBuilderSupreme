import boto3
import json
from botocore.exceptions import ClientError

def get_bedrock_client(region="us-east-1"):
    """
    Creates and returns a Bedrock Runtime client.
    Parameters:
        - region (str): AWS region where Bedrock is enabled.
    Returns:
        - boto3 client: Bedrock Runtime client.
    """
    boto3.setup_default_session(profile_name='MealGenerator')
    return boto3.client("bedrock-runtime", region_name=region)

def generate_recipe_with_claude_haiku(cuisine, protein, spice_level, temperature=0.7, max_tokens=4096):
    """
    Generates a recipe using Claude 3 Haiku with a structured format.
    Parameters:
        - cuisine (str): Type of cuisine (e.g., Italian, Mexican).
        - protein (str): Main protein (e.g., Chicken, Beef).
        - spice_level (str): Spice level (e.g., Mild, Medium, Spicy).
        - temperature (float): Randomness level for AI generation.
        - max_tokens (int): Maximum number of tokens for the response.
    Returns:
        - dict: A structured recipe with title, description, ingredients, and instructions.
    """
    client = get_bedrock_client()
    model_id = "anthropic.claude-3-haiku-20240307-v1:0"  # Replace with the correct model ID.

    # Construct the structured prompt
    prompt = (
        f"Generate a structured recipe in the following format:\n\n"
        f"Title: <Recipe Title>\n"
        f"Description: <Brief description>\n"
        f"Ingredients:\n- <Ingredient 1>\n- <Ingredient 2>\n- <Ingredient 3>\n"
        f"Instructions:\n1. <Step 1>\n2. <Step 2>\n3. <Step 3>\n\n"
        f"Create a {spice_level} {cuisine} dish featuring {protein}. Be concise and clear."
    )

    # Prepare the native request for Claude 3 Haiku
    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ],
    }

    # Convert the request to JSON
    request_body = json.dumps(native_request)

    try:
        # Send the request to the Bedrock model
        response = client.invoke_model(modelId=model_id, body=request_body)
        model_response = json.loads(response["body"].read())  # Parse the response body

        # Extract the generated recipe
        response_text = model_response["content"][0]["text"]
        print(response_text)
        return parse_recipe_output(response_text)

    except (ClientError, Exception) as e:
        print(f"ERROR: Unable to invoke Claude 3 Haiku. Reason: {e}")
        return {
            "title": "Error",
            "description": "Could not generate recipe.",
            "ingredients": [],
            "instructions": "Please try again."
        }

def parse_recipe_output(raw_output):
    """
    Parses the structured output from Claude into a dictionary format.
    Parameters:
        - raw_output (str): AI-generated text in structured format.
    Returns:
        - dict: Parsed recipe components.
    """
    try:
        # Split the output into lines and strip whitespace
        lines = [line.strip() for line in raw_output.split("\n") if line.strip()]

        # Initialize parsed fields
        title = ""
        description = ""
        ingredients = []
        instructions = []

        # Parse line by line
        for line in lines:
            if line.startswith("Title:"):
                title = line.replace("Title:", "").strip()
            elif line.startswith("Description:"):
                description = line.replace("Description:", "").strip()
            elif line.startswith("-"):
                ingredients.append(line.replace("- ", "").strip())
            elif line[0].isdigit():  # Assuming instructions start with numbers
                instructions.append(line)

        # Join instructions into a single string
        instructions_text = "\n".join(instructions)

        # Return parsed data
        return {
            "title": title or "Untitled Recipe",
            "description": description or "No description provided.",
            "ingredients": ingredients or ["No ingredients listed."],
            "instructions": instructions_text or "No instructions provided."
        }

    except Exception as e:
        print(f"Error parsing recipe output: {e}")
        return {
            "title": "Error",
            "description": "Could not parse recipe.",
            "ingredients": [],
            "instructions": "Please try again."
        }