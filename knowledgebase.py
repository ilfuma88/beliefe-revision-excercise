class KnowledgeBase:
    # basic functions to initiate, add, remove, revise and print beliefs
    def __init__(self):
        self.beliefs = []

    def add_belief(self, belief):
        if belief not in self.beliefs:
            self.beliefs.append(belief)

    def remove_belief(self, belief):
        if belief in self.beliefs:
            self.beliefs.remove(belief)

    def revise_belief(self, belief, new_belief):
        if belief in self.beliefs:
            self.remove_belief(belief)
        self.add_belief(new_belief)

    def print_beliefs(self):
        for belief in self.beliefs:
            print(belief)


# Usage
kb = KnowledgeBase()
kb.add_belief("The sky is blue")
kb.add_belief("Grass is green")
kb.revise_belief("The sky is blue", "The sky is grey")
kb.print_beliefs()  # Outputs: 'Grass is green', 'The sky is grey'
