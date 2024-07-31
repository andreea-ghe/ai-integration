import sys
import os
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

def generate_feedback(diff, code_content):
    """Generate feedback using OpenAI GPT model."""
    server_url = os.getenv('SERVER_URL', 'http://localhost:11434')  # Default to localhost if SERVER_URL not set
    system_message = f"""\
I will provide for you the differences extracted with a github function between
the initial and the final code and also the initial code. Please review these 
differences in the context of the initial code and identify any syntax or logical
errors, suggest ways to refactor and improve code quality, enhance performance, 
address security concerns, and align with best practices. Provide specific examples 
for each area and limit your recommendations to three per category.

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

Code changes:
        
{diff}

Full code:

{code_content}

Your review:"""

    try:
        response = completion(
            model="ollama/llama3.1-70b",
            messages=[
                {"role": "system", "content": system_message},
            ],
            server_url=f"{server_url
