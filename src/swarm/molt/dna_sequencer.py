import os
import json
import time
from concierge import concierge
from pathlib import Path
import sys

# Add molt_bleak paths for DNA mutation logic
sys.path.append("/storage/emulated/0/RootBase/molt_bleak/MoltBleak/src/core")
try:
    from iterate import MoltIterator
except ImportError:
    print("[-] Error: Could not import MoltIterator. Check paths.")
    MoltIterator = None

class DNASequencer:
    """
    DNA Sequencer & Simulator.
    Aggregates multimodal intelligence and runs recursive strategy simulations.
    """
    def __init__(self):
        self.results_dir = Path("/storage/emulated/0/RootBase/dna_simulations")
        self.results_dir.mkdir(exist_ok=True)

    def pick_brains(self, problem: str) -> Dict[str, str]:
        """Query multiple models for their 'vision' of the next move."""
        predictions = {}
        providers = [
            ("gemini", "gemini-1.5-flash"),
            ("ollama", "deepseek-r1:1.5b"),
            # Add others if keys exist
        ]
        
        for provider, model in providers:
            print(f"[+] Picking brain: {provider} ({model})...")
            response, err = concierge.generate(
                prompt=f"Analyze this scenario and predict the optimal next move for maximum revenue and resilience: {problem}",
                provider=provider,
                model=model,
                system="You are a strategic forecasting agent for RootBase. Think 10 steps ahead."
            )
            if not err:
                predictions[provider] = response
            else:
                print(f"  [-] Failed: {err}")
        
        return predictions

    def simulate_and_mutate(self, problem: str, brain_insights: Dict[str, str]):
        """Feed insights into the DNA mutation pipeline for recursive refinement."""
        if not MoltIterator:
            print("[-] Simulation aborted: MoltIterator missing.")
            return

        print("[+] Starting DNA Mutation Simulation...")
        
        # We wrap the concierge as a 'client' that MoltIterator can use
        class ConciergeBridge:
            def generate(self, prompt, system=None):
                return concierge.generate(prompt, provider="ollama", system=system)

        iterator = MoltIterator(ConciergeBridge())
        
        # Initial task based on insights
        aggregated_insight = "\n\n".join([f"Insight from {p}: {i}" for p, i in brain_insights.items()])
        task = f"Refine the following strategic vision into an actionable automation hook: {aggregated_insight}"
        
        iterations = []
        for i in range(3): # 3 iterations of 'DNA mutation'
            print(f"  [>] Iteration {i+1}...")
            result = iterator.iterate(task, iterations)
            iterations.append(result)
            
            # Save step
            sim_file = self.results_dir / f"simulation_{int(time.time())}_step_{i+1}.json"
            with open(sim_file, "w") as f:
                json.dump(result, f, indent=2)
            print(f"  [+] Step {i+1} secured: {sim_file}")

        print("[+] DNA Sequencing complete. Strategy evolved.")

if __name__ == "__main__":
    sequencer = DNASequencer()
    problem = "Scaling Mrs. Higgins to 100 autonomous instances across a distributed Nostr network."
    insights = sequencer.pick_brains(problem)
    sequencer.simulate_and_mutate(problem, insights)
