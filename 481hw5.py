def github() -> str:
    """
    Returns:
        str: github link
    """

    return "https://github.com/qiguangyan/481hw/blob/main/481hw5.py"

import requests
from bs4 import BeautifulSoup

def scrape_code(url: str) -> str:
    """
    Takes a lecture’s URL on the course website and returns a string containing all the python code 
    in the lecture formatted so that it could save it as a python file and run it without syntax issues
    
    Parameters:
    url (str): The URL of slids on the course website

    Returns:
    str: A string containing all Python code
    """

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <code> tags
    code_elements = soup.find_all('code', class_='sourceCode python')

    code_snippets = []

    # Process each code element found
    for element in code_elements:
        # separate different lines of code
        lines = {}
        for span in element.find_all('span', id=True):
            span_id = span['id']
            lines[span_id] = lines.get(span_id, '') + span.get_text()

        # Combine lines, filter out magic commands
        code_text = '\n'.join(lines[id] for id in sorted(lines) if not lines[id].strip().startswith('%'))
        if code_text:
            code_snippets.append(code_text)
    return '\n'.join(code_snippets)

