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
            user_input = input(
                "Enter a belief, type 'empty' to empty the belief base, or type 'exit' to quit: "
            )
            if user_input.lower() == "exit":
                break
            elif user_input.lower() == "empty":
                self.belief_revision.empty_belief_base()
                print("Belief base has been emptied.")
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
