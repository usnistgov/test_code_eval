def is_palindrome(string: str) -> bool:
    """ Test if given string is a palindrome """
    return string == string[::-1]


def make_palindrome(st: str) -> str:
    if not st:
        return ''

    beginning_of_suffix = 0

    while not is_palindrome(st[beginning_of_suffix:]):
        beginning_of_suffix += 1

    return st + st[:beginning_of_suffix][::-1]
