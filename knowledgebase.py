from belief import Belief


class KnowledgeBase:
    def __init__(self):
        self.beliefs = set()

    def add_belief(self, belief):
        self.beliefs.add(Belief(belief.upper()))

    def remove_belief(self, belief):
        self.beliefs.discard(Belief(belief))

    def revise_belief(self, old_belief, new_belief):
        self.remove_belief(old_belief)
        self.add_belief(new_belief)

    def print_beliefs(self):
        for belief in self.beliefs:
            print(belief.proposition)


def main():
    # Usage
    kb = KnowledgeBase()
    kb.add_belief("q")
    kb.add_belief("A&B")
    kb.add_belief("-A&B")
    kb.add_belief("-(A&B)")
    # kb.revise_belief("")
    kb.print_beliefs()  # Outputs: ''



if __name__ == "__main__":
    main()
