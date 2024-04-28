from sympy import And, Not, Or,symbols,Equivalent,Implies,to_cnf

def parse_cnf(cnf_expression):
    """Parse a sympy CNF expression into a set of clauses where each clause is a set of literals."""
    if isinstance(cnf_expression, And):
        return [set(clause.args) if isinstance(clause, Or) else {clause} for clause in cnf_expression.args]
    elif isinstance(cnf_expression, Or):
        return [{clause} for clause in cnf_expression.args]
    return [{cnf_expression}]

def negate_literal(literal):
    """Return the negation of a sympy literal."""
    return Not(literal) if not isinstance(literal, Not) else literal.args[0]

def davis_putnam(clauses):
    """Recursively apply the Davis-Putnam algorithm to check for unsatisfiability of CNF clauses."""
    print("Current Clauses:", clauses)  # Debugging output
    if not clauses:
        return False
    if any(not clause for clause in clauses):
        return True

    unit_clauses = {next(iter(clause)) for clause in clauses if len(clause) == 1}
    assignments = set()

    while unit_clauses:
        literal = unit_clauses.pop()
        assignments.add(literal)
        new_clauses = []
        for clause in clauses:
            if literal not in clause:
                new_clause = clause - {negate_literal(literal)}
                if len(new_clause) == 0:
                    return True  # Contradiction found
                elif len(new_clause) == 1:
                    unit_clauses.add(next(iter(new_clause)))
                new_clauses.append(new_clause)
        clauses = new_clauses
        print("After Unit Propagation:", clauses)  # Debugging output

    if clauses:
        literal = next(iter(clauses[0]))
        print("Splitting on:", literal)  # Debugging output
        return davis_putnam([clause - {literal} for clause in clauses if literal not in clause]) and \
               davis_putnam([clause - {negate_literal(literal)} for clause in clauses if negate_literal(literal) not in clause])

    return False

def entails(belief_base, formula):
    belief_base_cnf = to_cnf(belief_base)
    print(belief_base_cnf)
    negated_formula_cnf = to_cnf(Not(formula))
    combined_cnf = And(belief_base_cnf, negated_formula_cnf)
    
    clauses = parse_cnf(combined_cnf)
    return davis_putnam(clauses)

from sympy import symbols, Or, And, Not, Implies, sympify

def remove_implications_and_equivalences(expr):
    """Recursively eliminate implications and equivalences in the expression."""
    if expr.func == Implies:
        A, B = expr.args
        return Or(Not(remove_implications_and_equivalences(A)), remove_implications_and_equivalences(B))
    elif expr.func == Equivalent:
        A, B = expr.args
        # Equivalent A <-> B is (A -> B) & (B -> A)
        return And(Or(Not(remove_implications_and_equivalences(A)), remove_implications_and_equivalences(B)),
                   Or(Not(remove_implications_and_equivalences(B)), remove_implications_and_equivalences(A)))
    elif expr.func in (And, Or):
        return expr.func(*(remove_implications_and_equivalences(arg) for arg in expr.args))
    elif expr.func == Not:
        return Not(remove_implications_and_equivalences(expr.args[0]))
    return expr

def push_negations_inward(expr):
    """Use De Morgan's laws to push negations inward."""
    if expr.func == Not:
        arg = expr.args[0]
        if arg.func == And:
            return Or(*[push_negations_inward(Not(a)) for a in arg.args])
        elif arg.func == Or:
            return And(*[push_negations_inward(Not(a)) for a in arg.args])
        return expr
    elif expr.func in (And, Or):
        return expr.func(*(push_negations_inward(a) for a in expr.args))
    return expr

def distribute_and_over_or(expr):
    """Refined distribution and simplification of logical expressions."""
    if expr.func == And:
        simplified_expr = simplify_and(list(expr.args))
        return simplified_expr if simplified_expr else expr
    elif expr.func == Or:
        return Or(*[distribute_and_over_or(arg) for arg in expr.args]).simplify()
    return expr

def simplify_and(args):
    """Handle distributing ANDs over ORs while minimizing redundancy."""
    while len(args) > 1:
        first, second = args[0], args[1]
        combined = combine_and_simplify(first, second)
        args = [combined] + args[2:]
    return args[0]

def combine_and_simplify(left, right):
    """Combine two expressions under AND and simplify, checking for redundancies."""
    if left.func == Or and right.func == Or:
        return Or(*[And(l, r).simplify() for l in left.args for r in right.args if Not(l).simplify() != r and Not(r).simplify() != l])
    elif left.func == Or:
        return Or(*[And(l, right).simplify() for l in left.args])
    elif right.func == Or:
        return Or(*[And(left, r).simplify() for r in right.args])
    return And(left, right).simplify()


def to_cnf(expr):
    """Convert expression to CNF."""
    expr = sympify(expr)  # Ensure the expression is a Sympy expression
    expr_no_imp = remove_implications_and_equivalences(expr)
    expr_neg_in = push_negations_inward(expr_no_imp)
    cnf_expr = distribute_and_over_or(expr_neg_in)
    return cnf_expr



# Example usage:
if __name__ == "__main__":
    belief_base = "(A >>) B & ~C"
    formula = "~B"
    entails = entails(belief_base, formula)
    print("Belief base entails formula:", entails)
