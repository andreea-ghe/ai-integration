import sys
import openai
import os
from dotenv import load_dotenv
from litellm import completion

def generate_feedback(code):
    """Generate feedback using OpenAI GPT model."""
    response = completion(
    model="ollama/llama3",
    # model="gpt-4"  
    messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Please review the following code and provide feedback:\n\n{code}"}
        ]
    )

    return response['choices'][0]['message']['content']

 
def review_code(files):
    review_results = []
    for file_name in files.split():
        with open(file_name, 'r') as file:
            code = file.read()

        # Perform code review and return the result
        answer = generate_feedback(code)
        review_results.append(f"Code review for {file_name}: \n{answer}\n")
    return "\n".join(review_results)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chatbot.py <file_names>")
        sys.exit(1)
    
    files = sys.argv[1]
    result = review_code(files)
    print(result)

