from sympy.logic.boolalg import to_cnf
from sympy.abc import A, B, C  # Import symbolic representations
from sympy import symbols, sympify
import sympy
import re

class Belief:
    def __init__(self, proposition: str, importance : int = 1):
        self.proposition :str = proposition.upper()
        self.importance :int = importance
        valid, message = self.is_valid_proposition(proposition)
        if not valid:
            raise ValueError("Invalid proposition syntax: " + message)

    def is_valid_proposition(self, proposition: str) -> tuple:
        """
        Validates the proposition string based on enhanced propositional logic rules:
        - Propositions must be single alphabetic characters (A-Z, a-z).
        - Allowed operators are & (AND), | (OR), > (IMPLIES), and - (NEGATION).
        - Brackets () are allowed for grouping.
        - The string may start with a negation symbol (~).
        - Negation (~) can follow & or |, or precede (.
        - No consecutive operators are allowed, except for the specific placement of ~.
        - The number of opening and closing brackets must match.
        - Returns a tuple (bool, str) where bool indicates if the proposition is valid, and str provides a message.
        """
        # Remove spaces for easier pattern matching
        proposition = proposition.replace(' ', '')

        # Check for balanced brackets
        if not self.brackets_balanced(proposition):
            return False, "Unbalanced brackets"

        # Regex to check for valid proposition syntax
        # Pattern allows:
        # - Optionally starting with a negation
        # - Starting with letters or opening bracket
        # - Valid combinations of operators with letters and brackets
        pattern = r'^~?[a-zA-Z()]+(?:[&|>~]?~?[a-zA-Z()]+)*$'
        if not re.match(pattern, proposition):
            return False, "Invalid characters or sequence detected"

        return True, "Valid proposition"

    def brackets_balanced(self, proposition: str) -> bool:
        """
        Checks if the brackets in the proposition are balanced.
        """
        balance = 0
        for char in proposition:
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
            if balance < 0:
                return False  # More closing brackets than opening
        return balance == 0  # Must be zero for perfectly balanced brackets

    def convert_to_cnf(self):
        # Define your symbols
        # Example: if your string uses variables like A, B, C, define them here.
        A, B, C = symbols('A B C')
        
        #iterate over the proposition string and replace the '>' character with the '>>' character
        #to represent the implication operator
        self.proposition = self.proposition.replace(">", ">>")

        # Parse the string into a sympy expression
        # 'sympify' tries to convert a string into a valid sympy expression.
        expr = sympify(self.proposition)

        # Convert the expression to CNF
        cnf_expr = to_cnf(expr, simplify=True)

        return cnf_expr

    
    def __eq__(self, other: 'Belief'):
        return self.proposition.upper() == other.proposition.upper()
    
    def __hash__(self):
        return hash(self.proposition)
    
    def __str__(self):
        return self.proposition
    
def main():
# Example usage
    try:
        belief1 = Belief("~A&(B|C)>D")
        print("Belief1 proposition:", belief1.proposition)
    except ValueError as e:
        print(e)

    try:
        belief2 = Belief("-(A&&B)|C")
        print("Belief2 proposition:", belief2.proposition)
    except ValueError as e:
        print(e)

    try:
        belief3 = Belief("-A&-B|C)")
        print("Belief3 proposition:", belief3.proposition)
    except ValueError as e:
        print(e)

    try:
        belief4 = Belief("~A&~(B|C)")
        print("Belief4 proposition:", belief4.proposition)
    except ValueError as e:
        print(e)
        
    print("testing convert_to_cnf:")
    # Example usage
    cnf_expression = belief4.convert_to_cnf()
    print("CNF Form:", cnf_expression)

    cnf_expression = belief1.convert_to_cnf()
    print("CNF Form:", cnf_expression)


if __name__ == "__main__":
    main()