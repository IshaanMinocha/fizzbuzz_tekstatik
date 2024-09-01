import pathlib
import textwrap
import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()

GOOGLE_API_KEY = os.getenv('API_KEY')

# Replace with your API key

# Configure the API key
genai.configure(api_key=GOOGLE_API_KEY)

# Define a function to format text as Markdown-like output
def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# Initialize the GenerativeModel
model = genai.GenerativeModel('gemini-pro')

# Generate content based on the prompt
response = model.generate_content("What is wfuzz software?")

# Format and print the response as Markdown-like text
formatted_text = to_markdown(response.text)
print(formatted_text)
