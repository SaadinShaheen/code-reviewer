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

# TEST
issues = check_line_length("test_files/sample.py")
for issue in issues:
    print(issue)