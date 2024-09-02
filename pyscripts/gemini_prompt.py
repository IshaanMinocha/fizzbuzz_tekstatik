import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv('API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

def get_user_input():
    return input("Enter your message: ")

# Hard-coded prompt
hard_coded_prompt = "Suggest some ways to get rid of the vulnerabilities and provide a code solution to fix vulnerability. Please format the response as follows:\n\nSolution:\n[Your solution here]\n\nCode:\n[Your code here]"

def clean_text(text):
    text = text.replace("**", "").strip()
    return text

def json_format(user_message, clean_text):
    solution_part = clean_text.split("Solution:")[1].split("Code:")[0].strip()
    code_part = clean_text.split("Code:")[1].strip()

    return {
        "user_message": user_message,
        "solution": solution_part,
        "code": code_part
    }


if __name__ == "__main__":
    user_message = get_user_input()
    model = genai.GenerativeModel('gemini-pro')

    combined_prompt = f"{user_message}\n\n{hard_coded_prompt}"

    try:
        response = model.generate_content(
            f'{combined_prompt}',
            # generation_config = genai.types.GenerationConfig(
            #                       candidate_count = 1,
            #                       stop_sequences = ['.'],
            #                       top_p = 0.6,
            #                       top_k = 5,
            #                       temperature = 0.8)
                                )
        #print("LLM Response:", response.text)
        response_json = json_format(user_message, clean_text)
        print(json.dumps(response_json, indent=4))

    except Exception as e:
        print(f"An error occurred: {e}")

    