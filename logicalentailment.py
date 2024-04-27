from sympy import And, Not, Or, to_cnf,symbols,Equivalent

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
    negated_formula_cnf = to_cnf(Not(formula))
    combined_cnf = And(belief_base_cnf, negated_formula_cnf)
    
    clauses = parse_cnf(combined_cnf)
    return davis_putnam(clauses)

# Example usage:
if __name__ == "__main__":
    # P, Q, R = symbols('P Q R')
    # print("#" + str(Equivalent(P, Or(Q, Not(R)))))

    # belief_base = "Equivalent(P, Q | ~R)"
    belief_base = "Equivalent(A, B | C) & A"
    formula = "~B"
    entails = check_logical_entailment(belief_base, formula)
    print("Belief base entails formula:", entails)
