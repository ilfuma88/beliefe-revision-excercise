import unittest
from unittest.mock import patch
from cli import Cli
from sympy import symbols, And, Or, Implies


class TestRationalityPostulatesContraction(unittest.TestCase):
    def setUp(self):
        self.cli = Cli()

    # 2. Success
    @patch("builtins.input", side_effect=["p", "0.5", "exit"])
    def test_success_postulates(self, input):
        # self.cli.run()
        belief = symbols("p")
        self.cli.belief_revision.contract(belief, 0.5)
        self.assertNotIn(belief, self.cli.belief_revision.beliefs)

    # 3. Inclusion
    @patch("builtins.input", side_effect=["p", "0.5", "q", "0.6", "~q", "0.7", "exit"])
    def test_inclusion(self, input):
        self.cli.run()
        belief_p = symbols("p")
        belief_q = symbols("q")
        belief_q_negated = ~belief_q
        initial_beliefs = {belief_p, belief_q, belief_q_negated}
        for belief in self.cli.belief_revision.beliefs:
            self.assertIn(belief, initial_beliefs)

    # 4. Vacuity
    @patch("builtins.input", side_effect=["p", "0.5", "q", "0.6", "exit"])
    def test_vacuity(self, input):
        self.cli.run()
        belief_p = symbols("p")
        belief_q = symbols("q")
        initial_beliefs = {belief_p, belief_q}
        self.assertEqual(set(self.cli.belief_revision.beliefs.keys()), initial_beliefs)

    # 5. Extensionality
    @patch("builtins.input", side_effect=["p", "0.5", "q", "0.6", "exit"])
    def test_extensionality(self, input):
        self.cli.run()
        belief_p = symbols("p")
        belief_q = symbols("q")
        initial_beliefs = {belief_p, belief_q}
        self.assertEqual(set(self.cli.belief_revision.beliefs.keys()), initial_beliefs)

    # 1. Closure
    def test_closure(self):
        belief_p = symbols("p")
        belief_q = symbols("q")
        initial_beliefs = {belief_p: 0.5, belief_q: 0.6}
        self.cli.belief_revision.beliefs = (
            initial_beliefs.copy()
        )  # Set the initial beliefs

        # Call revise_belief with None as the new belief
        self.cli.belief_revision.revise_belief(None, None)

        # Check that the belief base remains the same
        self.assertEqual(self.cli.belief_revision.beliefs, initial_beliefs)

    # 6. Recovery
    @patch("builtins.input", side_effect=["p", "0.5", "q", "0.6", "exit"])
    def test_recovery(self, input):
        self.cli.run()
        belief_p = symbols("p")
        belief_q = symbols("q")
        initial_beliefs = {belief_p, belief_q}
        self.assertTrue(
            initial_beliefs.issubset(set(self.cli.belief_revision.beliefs.keys()))
        )


if __name__ == "__main__":
    unittest.main()
