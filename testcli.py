import unittest
from unittest.mock import patch
from cli import Cli
from sympy import symbols, And, Or, Implies


class TestCli(unittest.TestCase):
    def setUp(self):
        self.cli = Cli()

    @patch("builtins.input", side_effect=["p", "0.5", "exit"])
    def test_success_postulates(self, input):
        self.cli.run()
        belief = symbols("p")
        self.assertIn(belief, self.cli.belief_revision.beliefs)

    @patch("builtins.input", side_effect=["p", "0.5", "q", "0.6", "~q", "0.7", "exit"])
    def test_inclusion(self, input):
        self.cli.run()
        belief_p = symbols("p")
        belief_q = symbols("q")
        belief_q_negated = ~belief_q
        initial_beliefs = {belief_p, belief_q, belief_q_negated}
        for belief in self.cli.belief_revision.beliefs:
            self.assertIn(belief, initial_beliefs)

    @patch("builtins.input", side_effect=["p", "0.5", "q", "0.6", "exit"])
    def test_vacuity(self, input):
        self.cli.run()
        belief_p = symbols("p")
        belief_q = symbols("q")
        initial_beliefs = {belief_p, belief_q}
        self.assertEqual(set(self.cli.belief_revision.beliefs.keys()), initial_beliefs)

        # Try to add a new belief that doesn't conflict with the existing beliefs
        belief_r = symbols("r")
        self.assertFalse(
            self.cli.belief_revision.has_contradiction_with_belief_base(belief_r)
        )

        with patch("builtins.input", side_effect=["r", "0.7", "exit"]):
            self.cli.run()
            # Check that the new belief is in the belief base
            self.assertIn(belief_r, self.cli.belief_revision.beliefs.keys())
            # Check that the belief base still contains the initial beliefs
        self.assertTrue(
            initial_beliefs.issubset(set(self.cli.belief_revision.beliefs.keys()))
        )

    @patch("builtins.input", side_effect=["p", "0.5", "q", "0.6", "~p", "0.7", "exit"])
    def test_consistency(self, input):
        self.cli.run()
        for belief in self.cli.belief_revision.beliefs.keys():
            negated_belief = ~belief
            self.assertNotIn(negated_belief, self.cli.belief_revision.beliefs.keys())

    @patch("builtins.input", side_effect=["p", "0.5", "q", "0.6", "exit"])
    def test_extensionality(self, input):
        self.cli.run()
        belief_p = symbols("p")
        belief_q = symbols("q")
        initial_beliefs = {belief_p, belief_q}
        self.assertEqual(set(self.cli.belief_revision.beliefs.keys()), initial_beliefs)

        # Try to add a tautology
        with patch("builtins.input", side_effect=["p & p", "0.7", "exit"]):
            self.cli.run()
            # Check that the tautology is not in the belief base
            tautology = symbols("p & p")
            self.assertNotIn(tautology, self.cli.belief_revision.beliefs.keys())

        # Try to add a contradiction
        with patch("builtins.input", side_effect=["p & ~p", "0.7", "exit"]):
            self.cli.run()
            # Check that the contradiction is not in the belief base
            contradiction = symbols("p & ~p")
            self.assertNotIn(contradiction, self.cli.belief_revision.beliefs.keys())

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


if __name__ == "__main__":
    unittest.main()
