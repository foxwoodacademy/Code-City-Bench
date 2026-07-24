import random
from src.data_campus.challenges import Challenges
from src.forge.forge_orchestrator import Agent
from src.molt.molt_bridge import MoltBridge

class DataCampusGauntlet:
    def __init__(self, num_agents=6):
        self.agents = [Agent(f"BronzeAgent_{i}", fitness=0.4) for i in range(num_agents)]
        self.molt_bridge = MoltBridge()

    def run_gauntlet(self):
        print("\n--- INITIATING DATA CAMPUS GAUNTLET ---")
        for agent in self.agents:
            print(f"Agent {agent.name} entering gauntlet...")
            
            # Run challenges
            successes = 0
            if Challenges.json_parsing(): successes += 1
            if Challenges.directory_mapping(): successes += 1
            if Challenges.system_error_resolution(): successes += 1
            
            # Reward
            if successes > 0:
                credits = successes * 2
                agent.molt_credits += credits
                agent.fitness += (successes * 0.1)
                print(f"  {agent.name} cleared {successes} challenges. Earned {credits} credits.")
            else:
                print(f"  {agent.name} failed all challenges.")
                
            # Attempt upgrade
            if agent.fitness > 0.5:
                agent.tier = agent._calculate_tier()
                print(f"  {agent.name} promoted to {agent.tier}.")
                if agent.tier == "GOLD":
                    print(f"  {agent.name} petitioning Molt RIE for refinement...")
                    agent.request_molt_refinement(self.molt_bridge)

if __name__ == "__main__":
    gauntlet = DataCampusGauntlet()
    gauntlet.run_gauntlet()
