from decimal import Decimal
import sympy
from logicalentailment import entails, to_cnf

class KnowledgeBase:
    # basic functions to initiate, add, remove, revise and print beliefs
    def __init__(self):
        self.beliefs = {}

    def add_belief(self, belief, priority):
        if belief not in self.beliefs:
            self.beliefs[belief] = priority

    def remove_belief(self, belief):
        if belief in self.beliefs:
            del self.beliefs[belief]

    def revise_belief(self, belief, priority):
        # Incorporates a new belief ensuring consistency
        if not entails(None, belief):
            # Temporarily contract potential contradictions
            # Placeholder for contradiction handling
             ##contradiction = "not " + belief  # Simplistic contradiction handling
            self.contract(belief, priority)
            self.expand(belief, priority)

    def degree(self, formula):
        """
        Find maximum order j such that taking all beliefs in base
        with order >= j results in a belief set that entails formula.
        """
        formula = to_cnf(formula)
        if entails(None, formula):
            # Tautologies have degree = 1
            return Decimal(1)

        base = []
        for order, group in self.iter_by_order():
            # Get formulas from beliefs
            base += [b.formula for b in group]
            if entails(base, formula):
                return order
        return Decimal(0)
    
    def iter_by_order(self):
        """
        Generator that groups beliefs in belief base by decreasing order.

        Yields:
            Tuples of type (order, list of beliefs with that order).

        Example:
            >>> bb = BeliefBase()
            >>> bb.add('a', 0.7)
            >>> bb.add('a|b', 0.7)
            >>> bb.add('b', 0.5)
            >>> bb.add('a&f', 0.1)
            >>> for it in bb.iter_by_order():
            ...     print(it)
            (0.7, [Belief(a, order=0.7), Belief(a | b, order=0.7)])
            (0.5, [Belief(b, order=0.5)])
            (0.1, [Belief(a & f, order=0.1)])
        """

        result = []
        last_order = None

        for belief in self.beliefs:
            # If it is the first belief we examine, add it and set last_order
            if last_order is None:
                result.append(belief)
                last_order = belief.order
                continue

            # If the order of this belief is equal to the previous, add it to the group
            if belief.order == last_order:
                result.append(belief)
            # Otherwise, yield the group and reset
            else:
                yield last_order, result
                result = []
                result.append(belief)
                last_order = belief.order

        # Yield last result
        yield last_order, result

    def contract(self, formula, order):
        """
        Contract the belief base by reducing the order of beliefs that are less entrenched than the given order and that contradict the formula.
        """
        x = to_cnf(formula)
        order = Decimal(order)

        # Find the entrenchment degree of the new formula
        new_belief_degree = self.degree(x)

        # Temporary list to store beliefs to be modified
        to_adjust = []

        for belief in self.beliefs:
            y = belief.formula
            current_degree = self.degree(y)

            # Check if the existing belief's degree is less than the new belief's degree and contradicts it
            if current_degree < new_belief_degree:
                # This belief needs adjustment; determine the new order
                new_order = min(current_degree, order)  # Adjust the belief order to the lower of the two
                to_adjust.append((belief, new_order))

        # Change the order of the beliefs
        for belief, new_order in to_adjust:
            self.beliefs[belief] = new_order

    def expand(self, formula, order):
        """
        Expand the belief base by adding the formula with the given order.
        """
        self.add_belief(formula, order)


    def print_belief_base(self):
        for belief, priority in self.beliefs.items():
            print(f"Belief: {belief}, Priority: {priority:.2f}")
