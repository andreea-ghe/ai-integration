import os
import openai
from dotenv import load_dotenv
from litellm import completion
from github import Github

# Load environment variables
load_dotenv()

# Initialize GitHub client
token = os.getenv('GITHUB_TOKEN')
g = Github(token)
repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))

# Extract pull request number from GITHUB_REF
ref = os.getenv('GITHUB_REF')
if ref.startswith('refs/pull/'):
    pr_number = ref.split('/')[2]
else:
    raise ValueError(f"Unexpected GITHUB_REF format: {ref}")

pr = repo.get_pull(int(pr_number))

def generate_feedback(code):
    """Generate feedback using OpenAI GPT model."""
    system_message = f"""\
Please review the code below and identify any syntax or logical errors, suggest
ways to refactor and improve code quality, enhance performance, address security
concerns, and align with best practices. Provide specific examples for each area
and limit your recommendations to three per category.

Use the following response format, keeping the section headings as-is, and provide
your feedback. Use bullet points for each response. The provided examples are for
illustration purposes only and should not be repeated.

**Syntax and logical errors (example)**:
- Incorrect indentation on line 12
- Missing closing parenthesis on line 23

**Code refactoring and quality (example)**:
- Replace multiple if-else statements with a switch case for readability
- Extract repetitive code into separate functions

**Performance optimization (example)**:
- Use a more efficient sorting algorithm to reduce time complexity
- Cache results of expensive operations for reuse

**Security vulnerabilities (example)**:
- Sanitize user input to prevent SQL injection attacks
- Use prepared statements for database queries

**Best practices (example)**:
- Add meaningful comments and documentation to explain the code
- Follow consistent naming conventions for variables and functions

Code:
{code}
    
Your review:"""

    response = completion(
        model="ollama/llama3",
        # model="gpt-4",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Please review the following code and provide feedback:\n\n{code}"}
        ],
        api_base="http://localhost:11434"
    )

    return response['choices'][0]['message']['content']

def review_code(files):
    review_results = []
    for file_name in files:
        with open(file_name, 'r') as file:
            code = file.read()
        answer = generate_feedback(code)
        review_results.append((file_name, answer))
    return review_results

def post_review_comments(review_results):
    for file_name, review in review_results:
        # Fetch the file from the PR to get the patch (diff) details
        file_diff = pr.get_files().get(filename=file_name).patch
        diff_lines = file_diff.splitlines()
        for diff_line in diff_lines:
            if diff_line.startswith('+') and not diff_line.startswith('+++'):
                line_number = diff_lines.index(diff_line)
                pr.create_review_comment(body=review, path=file_name, position=line_number)
                break

if __name__ == "__main__":
    changed_files = [f.filename for f in pr.get_files()]
    review_results = review_code(changed_files)
    post_review_comments(review_results)
