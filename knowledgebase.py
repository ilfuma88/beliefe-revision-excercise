class KnowledgeBase:
    # basic functions to initiate, add, remove, revise and print beliefs
    def __init__(self):
        self.beliefs = {}

    def add_belief(self, belief,priority):
        if belief not in self.beliefs:
            self.beliefs[belief] = priority

    def remove_belief(self, belief):
        if belief in self.beliefs:
            self.beliefs.remove(belief)

    def revise_belief(self, belief, order):
        # if belief in self.beliefs:
            # self.remove_belief(belief)
        self.add_belief(belief,order)

    def print_belief_base(self):
        for belief, priority in self.beliefs.items():
            print(f"Belief: {belief}, Priority: {priority:.2f}")
