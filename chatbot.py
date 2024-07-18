import sys

def review_code(file_name):
    # Implement your code review logic here
    with open(file_name, 'r') as file:
        code = file.read()
    # Perform code review and return the result
    return f"Code review for {file_name}: \n" + code

if __name__ == "__main__":
    print(f"Arguments received: {sys.argv}")
    
    if len(sys.argv) < 2:
        print("Usage: python chatbot.py <file_name>")
        sys.exit(1)
    
    file_name = sys.argv[1]
    result = review_code(file_name)
    print(result)
    print("yay")
