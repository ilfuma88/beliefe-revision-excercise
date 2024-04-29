from belief import Belief
from itertools import combinations


class KnowledgeBase:
    def __init__(self):
        self.beliefs = set()

    def add_belief(self, belief: str):
        self.beliefs.add(Belief(belief.upper()))

    def remove_belief(self, belief: str):
        belief_to_remove_obj = next((b for b in self.beliefs if b.proposition == belief), None)
        if belief_to_remove_obj is not None:
            self.beliefs.remove(belief_to_remove_obj)
        else:
            print(f"Belief '{belief}' not found in the set.")        
    
    def contract_belief(self, belief : str):
        self.beliefs.remove(Belief(belief.upper()))
            
                     
        all_combinations : list = self.generate_all_combinations()
        for combination in all_combinations:
            print("combination:")
            for belief in combination:
                print(belief.proposition)
                
        #check if a combination doesn't entile the belief that has to be removed
        #if it doesn't check if is the non entiling combination with the highest priority 
        
        for combination in all_combinations:
            if not self.entails(combination, belief):
                print("combination that doesn't entail the belief:")
                for belief in combination:
                    print(belief.proposition)
                break
        
        

    def revise_belief(self, new_belief : str):
        self.contract_belief(new_belief) #we need to negate the new belief
        self.add_belief(new_belief)

    def print_beliefs(self):
        for belief in self.beliefs:
            print(belief.proposition)

    def generate_all_combinations(self):
    # Loop through all possible combination sizes including the empty combination
        all_combinations = []
        for r in range(len(self.beliefs) + 1):
            for combo in combinations(self.beliefs, r):
                all_combinations.append(combo)
    
        return all_combinations

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
