import openai
import git
import os
import shutil
import stat
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


# Path where the repository will be cloned
repo_path = 'C:\\Users\\Computacenter\\vs\\coderv_experiment\\repo'  

def get_code_files(repo_path):
    """Get a list of all code files in the repository."""
    code_files = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.cpp') or file.endswith('.h') or file.endswith('.py'):  # Adjust this to the types of files you want to review
                code_files.append(os.path.join(root, file))
    return code_files

def read_file(file_path):
    """Read the content of a file."""
    with open(file_path, 'r') as file:
        return file.read()

def generate_feedback(code):
    """Generate feedback using OpenAI GPT model."""
    response = openai.chat.completions.create(
        model="gpt-4",  # You can use other models as well
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Please review the following code and provide feedback:\n\n{code}"}
        ],
    )
    return response.choices[0].message.content.strip()

def remove_readonly(func, path, excinfo):
    """Handle read-only file deletion."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def delete_repo(repo_path):
    """Delete the repository directory."""
    if os.path.exists(repo_path) and os.listdir(repo_path):
        print(f"Deleting the directory: {repo_path}...")
        shutil.rmtree(repo_path, onerror=remove_readonly)
        print(f"Deleted directory: {repo_path}")

def create_directory(dir_path):
    """Create a directory."""
    if not os.path.exists(dir_path):
        print(f"Creating directory: {dir_path}...")
        os.makedirs(dir_path)
        print(f"Created directory: {dir_path}")

def clone_repo(repo_url, repo_path):
    """Clone the repository."""
    print(f"Cloning repository from {repo_url} to {repo_path}...")
    git.Repo.clone_from(repo_url, repo_path)
    print("Repository cloned successfully.")

def main():
    # URL of the GitHub repository to clone
    repo_url = 'https://github.com/andreea-ghe/Image-classification-library'

    # Delete the repository if it exists
    delete_repo(repo_path)
    
    # Create the directory
    create_directory(repo_path)
    
    # Clone the repository
    clone_repo(repo_url, repo_path)
    
    # Get a list of code files in the repository
    code_files = get_code_files(repo_path)

    # Generate feedback for each code file
    for file_path in code_files:
        print(f"Reading file: {file_path}")
        code = read_file(file_path)
        feedback = generate_feedback(code)
        print(f"Feedback for {file_path}:\n{feedback}\n{'-'*80}\n")

if __name__ == "__main__":
    main()
