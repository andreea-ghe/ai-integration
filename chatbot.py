import sys
import openai
import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

def generate_feedback(diff):
    """Generate feedback using OpenAI GPT model."""
    system_message = f"""\
        Please review the code changes below and identify any syntax or logical errors, suggest
        ways to refactor and improve code quality, enhance performance, address security
        concerns, and align with best practices. Provide specific examples for each area
        and limit your recommendations to three per category.

        Use the following response format, keeping the section headings as-is, and provide
        your feedback. Use bullet points for each response.

        **Syntax and logical errors**:
        **Code refactoring and quality**:
        **Performance optimization**:
        **Security vulnerabilities**:
        **Best practices**:

        Code changes:
        
{diff}

        Your review:"""

    response = completion(
    model="ollama/llama3",
    messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Please review the following code changes and provide feedback:\n\n{diff}"}
        ],
    api_base="http://localhost:11434"
    )

    return response['choices'][0]['message']['content']

def review_code_diffs(diffs):
    review_results = []
    for file_name, diff in diffs.items():
        answer = generate_feedback(diff)
        review_results.append(f"FILE: {file_name}\nREVIEW: {answer}\nENDREVIEW")
    return "\n".join(review_results)

def get_file_diffs(file_list):
    diffs = {}
    for file_name in file_list.split():
        diff_file = f"diffs/{file_name}.diff"
        if os.path.exists(diff_file):
            with open(diff_file, 'r') as file:
                diff = file.read()
            diffs[file_name] = diff
    return diffs

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chatbot.py <file_names>")
        sys.exit(1)
    
    files = sys.argv[1]
    file_diffs = get_file_diffs(files)
    result = review_code_diffs(file_diffs)
    with open('script_output.txt', 'w') as output_file:
        output_file.write(result)
