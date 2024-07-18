import sys
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
def generate_feedback(code):
    """Generate feedback using OpenAI GPT model."""
    response = openai.chat.completions.create(
        model="gpt-4",  
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Please review the following code and provide feedback:\n\n{code}"}
        ],
    )
    return response.choices[0].message.content.strip()
def review_code(files):
    review_results = []
    for file_name in files.split():
        with open(file_name, 'r') as file:
            code = file.read()
        # Perform code review and return the result
        review_results.append(f"Code review for {file_name}: \n{generate_feedback(code)}\n")
    return "\n".join(review_results)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chatbot.py <file_names>")
        sys.exit(1)
    
    files = sys.argv[1]
    result = review_code(files)
    print(result)
