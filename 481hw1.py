def github() -> str:
    """
    This function takes no arguments and returns a link to the solutions on GitHub.
    """

    return "https://github.com/<user>/<repo>/blob/main/<filename.py>"

def evens_and_odds(n: int) -> dict:
    """
    This function takes a natural number n and returns a dictionary with two keys, “evens” and “odds”, 
    where “evens” is the sum of all the even natural numbers less than n, 
    and “odds” the sum of all natural numbers less than n.
    """
    e = 0
    o = 0
    t = False
    for i in range(n):
        if t:
            o = o + i
        else:
            e = e + i
        t = not t
    return {'evens': e, 'odds': o}

from typing import Union
from datetime import datetime, date, time, timedelta
def time_diff(date_1: str, date_2: str, out: str) -> Union[str,float]:
    """
    takes as arguments two strings in the format ‘YYYY-MM-DD’ and a keyword out dictating the output. 
    If the keyword is “float”, return the time between the two dates (in absolute value) in days.
    """
    date_obj_1 = datetime.strptime(date_1, '%Y-%m-%d')
    date_obj_2 = datetime.strptime(date_2, '%Y-%m-%d')
    diff = abs((date_obj_2 - date_obj_1).days)
    if out == 'string':
        return f"There are {diff} days between the two dates"
    else:  # default to 'float'
        return diff

def reverse(in_list: list) -> list:
    """
    takes a list and returns a list of the arguments in reverse order
    """
    reversed_list = []
    n = len(in_list)
    for i in range(n):
        reversed_list.append(in_list[n - 1 - i])
    return reversed_list

def factorial(n: int) -> int:
    """
    takes a natural number n and return the factorial.
    """
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result
    
def prob_k_heads(n: int, k: int) -> float:
    """
    takes natural numbers n and k with n>k and returns the probability of getting k heads from n flips.
    """
    return factorial(n) / (factorial(k) * factorial(n - k)) * 0.5**n