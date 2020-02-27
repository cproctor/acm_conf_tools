import re

def parse_submission_number(text):
    return int(re.search("\d+$", text).group())

def parse_title(text):
    return " ".join(text.split())
