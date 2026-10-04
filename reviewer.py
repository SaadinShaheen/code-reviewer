import os
folder = "test_files"
files = [f for f in os.listdir(folder) if f.endswith(".py")] # Get all .py files from the folder

for filename in files:
    path = os.path.join(folder, filename) # os.path.join() is used to combine folder and filename to make a valid file path
    
    
    
def check_line_length(filepath, max_length=79):
    issues = []
    with open(filepath, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines, start=1):
            clean_line = line.rstrip("\n") # rstrip() removes characters from the right of a string
            if len(clean_line) > max_length:
                issues.append({
                    "line": i,
                    "type": "long_line",
                    "message": f"Line exceeds {max_length} characters",
                    "code" : clean_line
                })
        return issues

def check_missing_docstring(filepath):
    issues = []
    with open(filepath, "r") as f:
        lines = f.readlines() # reads the entire file and gives a list of lines

        for i, line in enumerate(lines, start=1): # Loop through every line and track line number along with the line
            clean_line = line.strip() 
            if clean_line.startswith("def "):
                    if i < len(lines): # Checks if the function definition is not the last line of the file
                        next_line = lines[i].strip() # Get the line after "def" and remove the extra whitespaces (i is 1 based, so lines[i] points to the following line)
                        if not next_line.startswith('"""'):
                            issues.append({"line": i,
                                           "type": "missing_docstring",
                                           "message": f"Docstring is missing for the function in line {i}",
                                           "code": clean_line
                            })
        return issues

# TEST
issues = check_missing_docstring("test_files/sample.py")
for issue in issues:
    print(issue)