import os
from dotenv import load_dotenv
from litellm import completion
from github import Github

# Load environment variables
load_dotenv()

# Initialize GitHub client
token = os.getenv('GITHUB_TOKEN')
repo_name = os.getenv('GITHUB_REPOSITORY')
pr_number = os.getenv('PR_NUMBER')
commit_sha = os.getenv('COMMIT_SHA')

print(f"GITHUB_TOKEN is set: {'Yes' if token else 'No'}")
print(f"GITHUB_REPOSITORY: {repo_name}")
print(f"PR_NUMBER: {pr_number}")
print(f"COMMIT_SHA: {commit_sha}")

# Check if the environment variables are correctly set
if token is None or repo_name is None or pr_number is None or commit_sha is None:
    raise ValueError("GITHUB_TOKEN, GITHUB_REPOSITORY, PR_NUMBER, or COMMIT_SHA is not set.")

g = Github(token)

# Try to get the repository
try:
    repo = g.get_repo(repo_name)
    print(f"Successfully accessed the repository: {repo.full_name}")
except Exception as e:
    raise ValueError(f"Error getting repository: {repo_name}\n{e}")

# Try to get the pull request
try:
    pr = repo.get_pull(int(pr_number))
    print(f"Successfully accessed the pull request: {pr.title}")
except Exception as e:
    raise ValueError(f"Error getting pull request: {pr_number}\n{e}")

# Try to get the commit object
try:
    commit = repo.get_commit(commit_sha)
    print(f"Successfully accessed the commit: {commit.sha}")
except Exception as e:
    raise ValueError(f"Error getting commit: {commit_sha}\n{e}")

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
    for file in files:
        file_name = file.filename
        code = file.patch
        answer = generate_feedback(code)
        review_results.append((file_name, answer))
    return review_results

def post_review_comments(pr, review_results, commit):
    for file_name, review in review_results:
        # Fetch the file from the PR to get the patch (diff) details
        for file in pr.get_files():
            if file.filename == file_name:
                file_diff = file.patch
                diff_lines = file_diff.splitlines()
                position = 1  # Position in the diff
                for index, diff_line in enumerate(diff_lines):
                    if diff_line.startswith('+') and not diff_line.startswith('+++'):
                        pr.create_review_comment(
                            body=review,
                            commit_id=commit.sha,
                            path=file_name,
                            position=position  # Position in the diff
                        )
                        break
                    position += 1  # Increment position in the diff

if __name__ == "__main__":
    changed_files = list(pr.get_files())
    review_results = review_code(changed_files)
    post_review_comments(pr, review_results, commit)
