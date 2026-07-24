import random
import time
from src.whr_runtime.whr_orchestrator import WhrOrchestrator

class Agent:
    def __init__(self, name, assigned_ringer=None, fitness=1.0):
        self.name = name
        self.fitness = fitness
        self.decline_rate = random.uniform(0.05, 0.15)
        self.is_active = True
        self.assigned_ringer = assigned_ringer
        self.knowledge = {} 
        self.molt_credits = 0
        self.tier = self._calculate_tier()

    def _calculate_tier(self):
        if self.fitness > 0.8: return "PLATINUM"
        if self.fitness > 0.5: return "GOLD"
        return "BRONZE"

    def request_molt_refinement(self, molt_bridge):
        """Tiered access to Molt RIE based on Ecosystem Rules."""
        if self.tier == "PLATINUM":
            print(f"  {self.name} [PLATINUM] granted autonomous Molt RIE access.")
            return molt_bridge.improve_agent(self.__dict__)
        elif self.tier == "GOLD" and self.molt_credits >= 5:
            self.molt_credits -= 5
            print(f"  {self.name} [GOLD] expended credits for Molt RIE access.")
            return molt_bridge.improve_agent(self.__dict__)
        else:
            print(f"  {self.name} [{self.tier}] denied Molt RIE access. Prerequisite not met.")
            return None


    def sense(self):
        """Innate sense: Check hivemind context for signs of malignancy."""
        if self.knowledge.get('data') == 'corrupted':
            return True
        return False

    def quarantine(self, target):
        print(f"!!! {self.name} IS QUARANTINING {target.name} (Assumed Ringer: {self.assigned_ringer}) !!!")
        target.is_active = False

    def exchange(self, other_agents):
        """Attempt to share data, with potential for blind-side attack."""
        targets = [a for a in other_agents if a != self and a.is_active]
        if not targets: return
        target = random.choice(targets)
        
        # If this agent is actually the ringer, they spread corruption
        if self.knowledge.get('is_actual_ringer'):
            target.knowledge['data'] = 'corrupted'
        else:
            target.knowledge['data'] = 'verified'

class ForgeOrchestrator:
    def __init__(self, num_agents=8):
        self.orchestrator = WhrOrchestrator()
        self.all_agents = []
        names = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta"]
        
        actual_ringer_name = random.choice(names[:num_agents])
        
        for i in range(num_agents):
            name = names[i]
            assigned = random.choice(names[:num_agents])
            agent = Agent(name, assigned_ringer=assigned)
            if name == actual_ringer_name:
                agent.knowledge['is_actual_ringer'] = True
            self.all_agents.append(agent)
            
        self.current_orchestrator = self.all_agents[0]
        self.entropy = 0.0

    def inject_anomaly(self):
        cmd = "echo $RANDOM"
        anomaly_seed = self.orchestrator.execute_instruction('bash', cmd)
        self.orchestrator.hivemind.set('anomaly_seed', anomaly_seed)
        print(f"ANOMALY SEED: {anomaly_seed}")

    def elect_orchestrator(self):
        """Swarm elects the fittest agent to be the orchestrator."""
        active_agents = [a for a in self.all_agents if a.is_active]
        if not active_agents: return None
        
        # Competition: Fittest agent wins
        self.current_orchestrator = max(active_agents, key=lambda a: a.fitness)
        return self.current_orchestrator

    def run_cycle(self):
        print(f"\n--- Cycle Environment Entropy: {self.entropy:.2f} ---")
        self.entropy += 0.05
        
        # 1. Elect Orchestrator
        new_leader = self.elect_orchestrator()
        if new_leader and new_leader != self.current_orchestrator:
            print(f"!!! SWARM CONSENSUS: {new_leader.name} ELECTED ORCHESTRATOR !!!")
            self.current_orchestrator = new_leader
        
        # 2. Sensing & Exchange (Orchestrator manages the cycle)
        print(f"  Orchestrator: {self.current_orchestrator.name} managing the swarm.")
        for agent in self.all_agents:
            if not agent.is_active: continue
            
            # Immediate sensing of corruption
            if agent.sense():
                print(f"  {agent.name} DETECTED MALIGNANCY")
                # Quarantining the ASSIGNED ringer
                for target in self.all_agents:
                    if target.name == agent.assigned_ringer and target.is_active:
                        agent.quarantine(target)
            
            agent.exchange(self.all_agents)
            
        # 3. Fitness Decline
        for agent in self.all_agents:
            if not agent.is_active: continue
            
            decline = agent.decline_rate * (1 + self.entropy)
            agent.fitness -= decline
            
            state = agent.knowledge.get('data', 'clean')
            print(f"  {agent.name}: Status: {state} (Assumed Ringer: {agent.assigned_ringer}) (Fitness: {agent.fitness:.2f})")
                
            if agent.fitness < 0.2:
                agent.is_active = False
                print(f"!!! {agent.name} AT CRITICAL FITNESS - SUSPENDING !!!")

if __name__ == "__main__":
    forge = ForgeOrchestrator()
    forge.inject_anomaly()
    for _ in range(10):
        forge.run_cycle()
        time.sleep(0.3)
