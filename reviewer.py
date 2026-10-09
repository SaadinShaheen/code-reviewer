def run_all_checks(filepath):
    all_issues = []
    
    all_issues += check_line_length(filepath)
    all_issues += check_missing_docstring(filepath)
    all_issues += check_long_functions(filepath)

    all_issues.sort(key=lambda issue: issue["line"])
    return all_issues

def check_line_length(filepath, max_length=79):
    issues = []
    with open(filepath, "r", encoding="utf-8") as f:
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
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines() # reads the entire file and gives a list of lines

        for i, line in enumerate(lines, start=1): # Loop through every line and track line number along with the line
            clean_line = line.strip() 
            if clean_line.startswith("def "):
                    if i < len(lines): # Checks if the function definition is not the last line of the file
                        next_line = lines[i].strip() # Get the line after "def" and remove the extra whitespaces (i is 1 based, so lines[i] points to the following line)
                        if not next_line.startswith('"""'):
                            issues.append({"line": i,
                                           "type": "missing_docstring",
                                           "message": f"Function has no docstring",
                                           "code": clean_line
                            })
    return issues

def check_long_functions(filepath, max_lines=30):
    issues = []
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines, start=1):
        clean_line = line.strip()
        if clean_line.startswith("def "):
            def_indent = len(line) - len(line.lstrip()) # Find how much the function definition is indented
            function_line_count = 0

            j = i # j will track our position as we look ahead
            while j <len(lines):
                next_line = lines[j]
                if next_line.strip() == "":
                    j += 1
                    continue

                next_indent = len(next_line) - len(next_line.lstrip())
                if next_indent <= def_indent:
                    break # function has ended

                function_line_count +=1
                j += 1

            if function_line_count > max_lines:
                issues.append({
                    "line": i,
                    "type": "long_function",
                    "message": f"Function is {function_line_count} lines long (over {max_lines})",
                    "code": clean_line
                })  
    return issues  
      
def review(filepath):
    issues = run_all_checks(filepath)

    if not issues:
        print("Code is Clean!")
        return
    total = len(issues)

    skipped = 0
    fixed = 0  
    ignored = 0
    ignored_types = set()
    for i, issue in enumerate(issues, start=1):
        if issue['type'] in ignored_types:
            continue
        print(f"Issue {i} of {total} [{issue['type']}] line {issue['line']}")
        print(f"  {issue['message']}")
        print(f"    {issue['code']}")
        print()

        while True:
            choice = input("Enter Choice [m]- Mark fixed, [s]- Skip, [i]- Ignore this type : ")
            choice = choice.lower().strip()
            if choice in ('m', 's', 'i'):
                break
            print("Invalid Input!\nPlease enter valid choice")

        print(f"You chose: {choice}")
        if choice == 'm':
            fixed += 1
        elif choice == 's':
            skipped += 1
        elif choice == 'i':
            ignored += 1
            ignored_types.add(issue['type'])
    print_summary(total, fixed, skipped, ignored)

def print_summary(total, fixed, skipped, ignored):
    print("--------- SUMMARY ---------")
    print(f"Issues found: {total}")
    print(f"   Marked fixed: {fixed}")
    print(f"   Skipped: {skipped}")
    print(f"   Ignored (by type): {ignored}")
    print("---------------------------")
# TEST
issues = review("test_files/sample.py")