# Code Reviewer

An interactive command-line tool that reads a Python file, finds common style problems, and walks you through them one by one so you decide what to do with each. When you finish, it prints a summary and saves a report of your decisions. Afterwards it can optionally ask an LLM to look for logic errors that simple rules can't catch.

It is a learning project: the checks, the review loop and the report are plain Python, and the AI layer uses Groq's free API.

## How it works

1. Takes the file to review from the command line, and exits with a clear message if you forgot it or the file does not exist
2. Runs three separate checks on the file, each returning a list of issues (line number, type, message and offending line of code)
3. Merges the lists and sorts issues by line number
4. Shows each issue in turn and asks what you want to do with it
5. If you ignore a type of issue, remembers that type in a set and silently skips every later issue of the same type
6. Prints a summary, and saves a report of every decision
7. Asks whether you want an AI review. If you say yes, it sends the file to an LLM and prints its suggestions

## What it checks

| Check | Rule |
| ------- | ------ |
| `long_line` | A line is longer than 79 characters |
| `missing_docstring` | A `def` line is not followed by a `"""` docstring |
| `long_function` | A function body is longer than 30 lines (found by indentation, ignoring blank lines) |

The optional AI review looks for a different kind of problem: logic errors such as wrong conditions, off-by-one mistakes and unhandled edge cases.

## Usage

1. Clone the repo and install the two dependencies. You need Python 3.12 or newer:
```
git clone https://github.com/SaadinShaheen/code-reviewer.git
cd code-reviewer
python -m pip install -r requirements.txt
```
2. (Only for the AI review) Get a free API key from [console.groq.com](https://console.groq.com) and create a `.env` file next to `reviewer.py`:
```
GROQ_API_KEY=your_key_here
```
3. Run it on any Python file:
```
python reviewer.py <file to review>
```
4. For each issue, choose:
- `m` marks the issue as fixed
- `s` skips it for now
- `i` ignores this *type* of issue: every later issue of that type is hidden automatically

Anything else is rejected and you are asked again. Input is not case-sensitive. Note that "marked fixed" only records that you fixed it yourself. The tool never edits your file.

5. Read the summary, then check the `reports/` folder for the saved report
6. When asked `Run AI review? [y/n]`, answer `y` to get AI suggestions or `n` to finish

## Example

A run on a small file with three logic bugs, answering `i` to the first issue and `y` to the AI review:
```
python reviewer.py test_files/sample.py
Issue 1 of 3 [missing_docstring] line 1
  Function has no docstring
    def calculate_total(numbers):

Enter Choice [m]- Marked fixed, [s]- Skip, [i]- Ignore this type : i
You chose: i

--------- SUMMARY ---------
Issues found: 3
   Marked fixed: 0
   Skipped: 0
   Ignored (by type): 1
---------------------------
Report saved to reports\sample_report.txt

Run AI review? [y/n]: y

AI suggestions (not guaranteed correct)
------------------------------
line: 4
severity: definite
problem: The loop overwrites total with each number instead of accumulating, so the function returns only the last element.
fix: Change the assignment to total += number

line: 8
severity: definite
problem: The even test checks for remainder 1, which identifies odd numbers as even.
fix: Return number % 2 == 0

line: 13
severity: definite
problem: The comparison uses '<' causing the function to keep the smallest value instead of the largest.
fix: Use if number > largest: to update when a larger value is found

line: 11
severity: potential
problem: Accessing numbers[0] without checking if the list is empty will raise IndexError for an empty input list.
fix: Add a guard at the start, e.g., if not numbers: raise ValueError('list is empty')

Summary: The functions contain definite logic errors in summing, even checking, and finding the largest value, and find_largest may fail on empty lists.
```
The rule-based checks only found missing docstrings here. The three logic bugs, and the empty list risk, were found only by the AI layer. I checked each of the four suggestions against the file by hand, and all were correct. AI answers can differ from run to run, so another run may word things differently.

## The report

After each session a report is saved to `reports/<name>_report.txt`, named after the file you reviewed. Each line has the line number, the issue type and your decision. Issues hidden by an ignore are not listed, and if the checks find nothing, no report is saved. Running the tool again on the same file replaces the old report. The AI suggestions are printed only and are not saved. The `reports/` folder is created automatically and is not tracked by git.

## AI review: things to know

- **Your code is sent to a third party.** If you answer `y`, the full text of the code goes to Groq's API. Don't use it on code you can't share.
- **Treat the answers as suggestions, not facts.** A model can be confidently wrong or miss a bug, so check every claim against the code.
- **Size limit.** Files over about 12,000 characters (counting the line numbers the tool adds) are not sent. This is a conservative limit chosen to keep requests manageable.
- **Failures are handled.** A missing or wrong API key, no internet connection and rate limits each print a short message and end the AI step without crashing the tool.
- **The model is fixed in the code** (`openai/gpt-oss-120b`, hosted free on Groq).

## Project structure

```
code-reviewer/
├── reviewer.py
├── requirements.txt
├── test_files/        (small files with known issues for trying the tool)
├── reports/           (generated output, not tracked)
├── .env               (not tracked, holds your API key)
├── .gitignore
└── README.md
```

## Bugs I ran into (and what I learned from them)

- **The wrong line number in the report**: I stored the loop counter as the line number, so the report said "line 6" for an issue on line 15. The real line number lives in the issue itself.
- **A path that was three folders deep**: I passed three pieces to `os.path.join`, so Windows treated `sample.py` as a folder and `open()` raised a `FileNotFoundError`. Building the file name as a single piece first fixed it.
- **Printing the whole API response**: my first AI call printed a huge response object instead of the answer. The text I wanted was nested inside it, at `choices[0].message.content`.

## Known limitations

- Only lines starting with `def` are checked, and only a `"""` docstring on the very next line counts. Single-quoted docstrings and function signatures that span several lines are not handled.
- The rule checks are simple text rules, not a full Python parser.
- `groq` and `python-dotenv` are imported when the program starts, so they must be installed even if you only want rule-based checks.
- The rate-limit message has not been tested against a real rate-limit error.

## Ideas for later

- Save AI suggestions in the report as well
- Let the user pick the AI model instead of hardcoding one
- More rule-based checks, such as unused variables or a bare `except:`
- A simple web interface instead of command-line prompts

## Built with

Python standard library (`os`, `sys`, `json`), plus `groq` and `python-dotenv` for the AI review.