from knowledgebase import KnowledgeBase

Kb = KnowledgeBase()

def print_knowledge_base():
    print("Printing Knowledge Base...")
    # loop over the beliefs in the knowledge base and print them
    for belief in Kb.beliefs:
        print(belief.proposition)
    

def generate_knowledge_base():
    print("Generating Knowledge Base...")
    # Add your code here to generate the knowledge base.

def extend_knowledge_base():
    print("Extending Knowledge Base...")
    new_belief = input("Enter a new belief: ")
    if new_belief in Kb.beliefs:
        print(f"Belief '{new_belief}' is already in the Knowledge Base.")
    else:
        try:
            Kb.add_belief(new_belief)
            print(f"Belief '{new_belief}' added successfully.")
        except Exception as e:
            print(f"Error adding belief: {e}")

def revise_knowledge_base():
    print("Revising Knowledge Base...")
    # Add your code here to revise the knowledge base.

def check_entailment_with_knowledge_base():
    print("Checking Entailment with Knowledge Base...")
    # Add your code here to check entailment with the knowledge base.

def main():
    
    Kb.add_belief("q")
    Kb.add_belief("A&B")
    Kb.add_belief("-A&B")
    options = {
        '1': print_knowledge_base,
        '2': generate_knowledge_base,
        '3': extend_knowledge_base,
        '4': revise_knowledge_base,
        '5': check_entailment_with_knowledge_base
    }

    while True:
        print("\nChoose an option:")
        print("1) Print Knowledge Base")
        print("2) Generate Knowledge Base")
        print("3) Extend Knowledge Base")
        print("4) Revise Knowledge Base")
        print("5) Check Entailment with Knowledge Base")
        
        choice = input("Enter option number (1-5): ")
        
        if choice in options:
            options[choice]()
        else:
            print("Invalid option. Please enter a number between 1 and 5.")
            continue

        # Uncomment the following line if you want to exit the menu after one operation.
        # break

if __name__ == "__main__":
    main()
