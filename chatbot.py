import sys

def review_code(files):
    review_results = []
    for file_name in files.split():
        with open(file_name, 'r') as file:
            code = file.read()
        # Perform code review and return the result
        review_results.append(f"Code review for {file_name}: \n{code}\n")
    return "\n".join(review_results)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chatbot.py <file_names>")
        sys.exit(1)
    
    files = sys.argv[1]
    result = review_code(files)
    print(result)

