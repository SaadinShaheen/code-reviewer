# Code Reviewer

An interactive command-line tool that reads a Python file, finds common style problems, and walks you through them one by one so you decide what to do with each. When you finish, it prints a summary and saves a report of your decisions.

It is a learning project: written in plain Python with no third-party packages.

## How it works

1. Takes the file to review from the command-line, and exits with a clear message if you forgot it or the file does not exist
2. Runs three separate checks on the file, each returning a list of issues (line number, type, message and the offending line of code)
3. Merges the lists and sorts the issues
4. Shows each issue in turn and asks what you want to do with it
5. If you ignore a type of issue, remembers that type in a set and silently skips every later issue of the same type
6. Prints a summary, and saves a report of every decision you made

## What it checks

| Check | Rule |
|-------|------|
| `long_line` | A line is longer than 79 characters |
| `missing_docstring` | A `def` line is not followed by a `"""` docstring |
| `long_function` | A function body is longer than 30 lines (found by indentation, ignoring blank lines) |

## Usage

1. Clone the repo. There is nothing to install, you just need Python 3.6 or newer:
```
git clone https://github.com/SaadinShaheen/code-reviewer.git
cd code-reviewer
```
2. Run it on any Python file:
```
python reviewer.py <file to review>
```
3. For each issue, choose:
- `m` marks the issue as fixed
- `s` skips it for now
- `i` ignores this *type* of issue: every later issue of that type is hidden automatically

Anything else is rejected and you are asked again. Input is not case-sensitive. Note that "marked fixed" only records that you fixed it yourself. The tool never edits your file.
4. Read the summary, then check the `reports/` folder for the saved report

## Example

```
Issue 1 of 6 [missing_docstring] line 1
    Function has no docstring
        def add_numbers(a, b):

Enter Choice [m]- Marked fixed, [s]- Skip, [i]- Ignore this type: i
You chose: i
Issue 2 of 6 [long_line] line 4
  Line exceeds 79 characters
    def this_is_a_really_loong_function_name_that_does_a_lot_of_stuff_and_has_a_line_way_too_long(x, y, z):

Enter Choice [m]- Mark fixed, [s]- Skip, [i]- Ignore this type : i
You chose: i
Issue 6 of 6 [long_function] line 15
  Function is 35 lines long (over 30)
    def long_function():

Enter Choice [m]- Mark fixed, [s]- Skip, [i]- Ignore this type : i
You chose: i
--------- SUMMARY ---------
Issues found: 6
   Marked fixed: 0
   Skipped: 0
   Ignored (by type): 3
---------------------------
Report saved to reports\sample_report.txt
```
In this run, ignoring `missing_docstring` on issue 1 hid issues 3, 4 and 5, which is why the numbering jumps from 2 to 6.

## The report

After each session a report is saved to `reports/<name>_report.txt`, named after the file you reviewed. It lists each issue you answered, with its line number, its type and your decision. Issues hidden by an ignore are not listed. Running the tool again on the same file replaces the old report. The `reports/` folder is created automatically and is not tracked by git.

## Project structure

```
code-reviewer/
├── reviewer.py
├── test_files/     (sample.py, a file with known issues for testing)
├── reports/        (generated output, not tracked)
├── .gitignore
└── README.md
```

## Bugs I ran into (and what I learned from them)

- **The wrong line number in the report**: I stored the loop counter as the line number, so the report said "line 6" for an issue on line 15. the real line number lives in the issue itself.
- **A path that was three folders deep**: I passed three pieces to `os.path.join`, so Windows treated `sample.py` as a folder and `open()` raised `FileNotFoundError`. Building the file name as a single piece first fixed it.

## Known limitations

- Only lines starting with `def` are checked, and only a `"""` docstring on the very next line counts. Single-quoted docstrings and function signatures that span several lines are not handled.
- The checks are simple text rules, not a full Python parser.

## Ideas for later

- An AI layer that send the code to an LLM and returns suggestions about logic problems that rules can't catch, shown as suggestions rather than facts
- More rule-based checks, such as unused variables or a bare `except:`
- A simple web interface instead of command-line prompts

## Built with

Python standard library (`os` and `sys`).