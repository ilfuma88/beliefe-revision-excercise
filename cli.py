import sympy
from sympy import SympifyError
from knowledgebase import KnowledgeBase


class Cli:
    def __init__(self):
        self.belief_revision = KnowledgeBase()

    def safe_sympify(self, expression):
        try:
            return sympy.sympify(expression)
        except SympifyError:
            print("Invalid mathematical expression. Please try again.")
            return None

    def run(self):
        while True:
            print("\nCommands:")
            print("1. Enter a belief to add it to the belief base.")
            print(
                "2. Type 'entails' to check entailment for a belief with the current belief base."
            )
            print("3. Type 'empty' to empty the belief base.")
            print("4. Type 'exit' to quit.\n")

            user_input = input("Enter a command: ")
            if user_input.lower() == "exit":
                break
            elif user_input.lower() == "empty":
                self.belief_revision.empty_belief_base()
                print("Belief base has been emptied.")
                continue
            elif user_input.lower() == "entails":
                input_formula = input("Enter the formula to check for entailment: ")
                belief = self.safe_sympify(input_formula)
                print(f"Checking entailment for belief: {belief}")
                if not self.belief_revision.has_contradiction_with_belief_base(belief):
                    print("The formula is entailed by the belief base")
                else:
                    print("The formula is not entailed by the belief base")
                    continue
            priority_input = input("Enter the priority for this belief (0 to 1): ")
            try:
                priority = float(priority_input)
                if not (0 <= priority <= 1):
                    raise ValueError("Priority must be between 0 and 1.")
            except ValueError:
                print("Invalid priority. Please enter a decimal value between 0 and 1.")
                continue

            belief = self.safe_sympify(user_input)
            if belief is not None:
                self.belief_revision.revise_belief(belief, priority)

            print("Final Belief Base:")
            self.belief_revision.print_belief_base()


if __name__ == "__main__":
    manager = Cli()
    manager.run()
