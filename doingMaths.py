import re, inflect
from sympy import parse_expr, simplify

def isEquation(message: str) -> bool:

    # remove parts of the message that we are not interested in 
    pattern = r'\d+|[+/*-]'
    expression = ' '.join(re.findall(pattern, message)).replace(" ", "")
    if expression != '':

        # Split the string into tokens
        tokens = re.split(r'(\W)', expression)

        if len(tokens) == 1:
            return False

        # Iterate through the tokens
        for token in tokens:
            # Check if the token is a number
            if token.isdigit():
                continue
            # Check if the token is an operator
            elif token in ['+', '-', '*', '/', '%']:
               continue
            # If the token is none of the above, it is invalid
            else:
                return False

        # If all tokens are valid, return True
        return True



def doMaths(message: str):
    pattern = r'\d+|[+/*-]'
    expression = ' '.join(re.findall(pattern, message)).strip()

    expr = parse_expr(expression)
    return simplify(expr)

