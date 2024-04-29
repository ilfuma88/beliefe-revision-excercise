Belief Revision CLI

Introduction

This project offers a command line interface (CLI) for managing beliefs using a belief revision system. Belief revision is the process of updating beliefs based on new information, and this CLI helps users perform operations like adding, revising, and checking beliefs.
Getting Started

To begin using the CLI, follow these steps:

    Start the CLI: Run the cli.py script. This will open a command prompt where you can enter commands.

    Adding a Belief: To add a belief, type it at the prompt and press enter. You'll then be asked to specify a priority for the belief. Priorities range from 0 to 1, where 0 means low priority and 1 means high priority.

    Checking Entailment: To check if a belief logically follows from the current set of beliefs, type entails at the prompt. Then, enter the belief you want to check.

    Emptying the Belief Base: To clear all beliefs from the current belief base, type empty at the prompt.

    Exiting the CLI: To close the CLI, type exit at the prompt.

Commands

    	Add a belief: Type the belief and its priority (0 to 1).
    	Example:
    		> p
    		Priority: 0.3

    	Check entailment: Type entails and the belief to check.
    	Example:
    		> entails
    		Enter belief: p

    	Empty the belief base: Type empty to clear all beliefs.

    	Exit the CLI: Type exit to close the CLI.

Error Handling

    If you enter an invalid mathematical expression or priority, the CLI will display an error message and prompt you to try again.

Tests

To run tests for the Rationality Postulates of Revision, execute the testcli.py script.
Logical Operators

    negation: "~" (Example: ~p)
    implication: ">>" (Example: p >> q)
    and: "&" (Example: p & q)
    or: "|" (Example: p | q)
    equivalent: "Equivalent()" (Example: Equivalent(p | q))
