from decimal import Decimal
import sympy
from sympy import And
from sympy import Not
from sympy import Symbol
from logicalentailment import entails, to_cnf
from copy import deepcopy


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

    def empty_belief_base(self):
        self.beliefs.clear()

    def revise_belief(self, belief, priority):
        # Incorporates a new belief ensuring consistency
        if belief is None:
            return
        if not self.beliefs:
            self.add_belief(belief, priority)
        else:
            if self.has_contradiction_with_belief_base(belief):
                self.contract(belief, priority)
            else:
                self.add_belief(belief, priority)

    def has_contradiction_with_belief_base(
        self, new_belief, local_copy_of_belief_base=None
    ):
        """
        Check if a new belief contradicts with any existing beliefs.
        A contradiction occurs if an existing belief entails the negation of the new belief.
        """
        belief_base = deepcopy(self.beliefs)

        if local_copy_of_belief_base is not None:
            belief_base = deepcopy(local_copy_of_belief_base)

        for existing_belief in belief_base:
            if entails(existing_belief, Not(new_belief)):
                return True
            if entails(And(existing_belief, new_belief), sympy.false):
                return True
        return False

    def contract(self, formula, priority):
        # Create a local copy of the belief base

        local_copy_of_belief_base = {}

        # Iterate over each belief in the belief base
        for belief, belief_priority in list(self.beliefs.items()):
            # Check if there is a contradiction
            # If the belief's priority is greater or equal to the formula's priority
            local_copy_of_belief_base[belief] = belief_priority
            print(
                f"Checking belief: {formula} with {belief} and {local_copy_of_belief_base}"
            )
            if self.has_contradiction_with_belief_base(
                formula, local_copy_of_belief_base
            ):
                print(f"Contradiction found with belief: {belief} blah blh")
                if belief_priority >= priority:
                    # Do nothing and return
                    return
                else:
                    print(f"Removing belief: {belief}")
                    # Remove the belief from the local copy
                    del local_copy_of_belief_base[belief]

        # Update the belief base with the local copy
        self.beliefs = local_copy_of_belief_base

        # Expand the belief base with the new formula and priority
        self.expand(formula, priority)

    def expand(self, formula, order):
        """
        Expand the belief base by adding the formula with the given order.
        """
        self.add_belief(formula, order)

    def print_belief_base(self):
        for belief, priority in self.beliefs.items():
            print(f"Belief: {belief}, Priority: {priority:.2f}")
