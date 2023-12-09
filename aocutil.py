from pyperclip import copy
from os import path, remove
from requests import get
import shelve

SESSION_TOKEN = ""

# gets the *last* occurrence of a substring starting with $start and ending with $end in $text (non-inclusive)
def get_last_split_block(text: str, start: str, end: str):
    text, start, end = text[::-1], start[::-1], end[::-1]
    return text[text.index(end) + len(end) : text.index(start)][::-1]


# function to print and also copy printed text to clipboard
def output(*text, sep=" ", end="\n"):

    # concatenates the text, separated by sep, and prints it
    text: str = sep.join(map(str, text)).strip()
    print(text, end=end)

    # copies the text to the clipboard
    copy(text)


# function to test a part 1 answer on the example input and see if it's right before submitting a wrong answer
def submit(answer: str | int):
    answer = str(answer).strip()

    # gets the current day's answer
    with shelve.open("answers") as db:
        current_day = str(db['current'])
        today_example_answer = db[current_day]

    # gets the example filename (it's consistently formatted)
    example_filename = f"day_{current_day.zfill(2)}_example.txt"

    # if day_##_example.txt does not exist, this is a live solution!
    if not path.isfile(example_filename):
        output(answer)

    # if it's a test case and the answer seems wrong, say so
    elif answer != today_example_answer:
        print(f"On the test case, program produced output {answer} (expected: {today_example_answer})")
        print(f"If this is wrong, please delete the file {example_filename}.")

    # if it's a test case and the answer is right, also say so!
    else:
        print(f"Obtained correct solution ({answer}) on test case! Re-run program for actual results.")
        remove(example_filename)


# function to download an input file from the website automatically
def download(day: int):

    # the url we want to download from, and my session ID
    url = f"https://adventofcode.com/2023/day/{day}/input"
    cookies = {"session": SESSION_TOKEN}

    # gets the page from the given url
    response = get(url, cookies=cookies)

    # writes it to a file
    with open(f"day_{str(day).zfill(2)}.txt", "w+") as f:
        f.write(response.text)


# gets the simple example from the puzzle, and records it (with its answer)
def get_example(day: int):

    # the url we want to download from, and my session ID
    url = f"https://adventofcode.com/2023/day/{day}"
    cookies = {"session": SESSION_TOKEN}

    # gets the page from the given url
    response = get(url, cookies=cookies)

    # writes it to a file called day_##_example.txt
    with open(f"day_{str(day).zfill(2)}_example.txt", "w+") as f:
        example = get_last_split_block(response.text, "<pre><code>", "</code></pre>")
        f.write(example)

    # records the answer to the example puzzle in shelve
    with shelve.open("answers") as db:
        db[str(day)] = get_last_split_block(response.text, "<code><em>", "</em></code>")


# an easy input function: takes in the filename of the .py file calling this
def read(filename: str):

    # replaces the .py in the filename with .txt
    day_str = filename[-5:-3]
    new_filename = f"day_{day_str}.txt"

    # if day_##.txt does not exist, download it (along with the example), create tomorrow's file, and record the current day
    if not path.isfile(new_filename):
        get_example(int(day_str))
        download(int(day_str))
        newfile(int(day_str))

        # records the current day
        with shelve.open("answers") as db:
            db['current'] = int(day_str)

    # if there's an example file (because the code hasn't yet successfully run on that), then use that
    if path.isfile(new_filename.replace(".txt", "_example.txt")):

        # open and read the file with example input in it
        with open(new_filename.replace(".txt", "_example.txt")) as f:
            data: str = f.read()

    # otherwise, the code has successfully passed the test case
    else:

        # open and read the file with real input in it
        with open(new_filename) as f:
            data: str = f.read()

    return data


# automatically creates tomorrow's python script
def newfile(day: int):

    # tomorrow's filename
    new_filename = f"day_{str(day + 1).zfill(2)}.py"

    # if it exists already or shouldn't because it's past the end, let's not
    if day > 25 or path.isfile(new_filename):
        return

    # otherwise, creates the file and fills out the basics
    with open(new_filename, "w+") as f:
        f.write("from aocutil import read, output, submit\ndata = read(__file__).splitlines()\n\n")
