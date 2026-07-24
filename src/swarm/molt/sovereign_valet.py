import os
import json
import time
from pathlib import Path
from concierge import concierge
from ModMind_guard import guard
from ModMind_ledger import ledger
from ModMind_executor import executor

class ModMindValet:

class ModMindValet:
    """
    The JaneBot Valet: The 'Glue' of the RootBase Ecosystem.
    Orchestrates the flow from Lead -> Intelligence -> Execution.
    """
    def __init__(self):
        self.leads_path = Path("src/saas/higgins/firefly_leads.json")
        self.strategy_path = Path("logs/current_strategy.json")
        self.state_file = Path("logs/valet_state.json")

    def _load_state(self):
        if not self.state_file.exists():
            return {"last_processed_lead": None, "pending_approval": None}
        return json.loads(self.state_file.read_text())

    def _save_state(self, state):
        self.state_file.write_text(json.dumps(state, indent=2))

    def check_for_leads(self):
        """The Entry Point: Monitors for new leads from Firefly Scouts."""
        if not self.leads_path.exists():
            return None
        
        leads = json.loads(self.leads_path.read_text())
        state = self._load_state()
        
        # Find the first un-analyzed lead
        for lead in leads:
            if not lead.get("analyzed"):
                print(f"[Valet] New lead detected: {lead['url']}")
                return lead
        return None

    def orchestrate_insight(self, lead):
        """The Brain Bridge: Moves a lead through the Intelligence Layer."""
        print(f"[Valet] Routing lead to Concierge for strategic analysis...")
        
        # 1. Get multi-model insights
        # In a full setup, this would call the DNASequencer.simulate_and_mutate()
        proposal, err = concierge.generate(
            prompt=f"Lead found: {lead['content_snippet']}. Propose the optimal SaaS package and pricing strategy for this lead.",
            system="You are the RootBase Strategic Architect. Propose a high-conversion, low-friction offer."
        )
        
        if err:
            print(f"[-] Orchestration Error: {err}")
            return None

        # 2. Create a 'Developer Manifest'
        # This is what a CLI coding model (Vibe/Gemini) would use to implement the change.
        manifest = {
            "target_package": lead['package'],
            "proposed_changes": proposal,
            "implementation_steps": [
                "Update saas_packages/package.json with new pricing",
                "Tweak copywriter.py prompts for this niche",
                "Configure the_closer.py for the target lead"
            ],
            "safety_check_required": True
        }
        
        # 3. Stage for Human Approval (HITL)
        state = self._load_state()
        state["pending_approval"] = {
            "lead": lead,
            "manifest": manifest,
            "timestamp": time.time()
        }
        self._save_state(state)
        
        # Record in the ledger
        ledger.record(
            identity="ModMindValet",
            action="STRATEGY_PROPOSED",
            payload={"lead_url": lead['url'], "manifest": manifest},
            rationale="Automatic lead-to-strategy pipeline triggered."
        )
        
        print("[+] Strategy staged. Awaiting approval on Mel-Bridge.")
        return manifest

    def execute_approved_strategy(self):
        """The Execution Bridge: Turns an approved manifest into reality."""
        state = self._load_state()
        if not state.get("pending_approval"):
            print("[-] No pending strategies to execute.")
            return False

        manifest = state["pending_approval"]["manifest"]
        
        # 1. Pass through the MotherBrain Guard
        if not guard.trigger_guard("STRATEGY_DEPLOY", "ModMindValet", manifest):
            print("🛑 [Valet] Guard blocked the deployment.")
            return False

        # 2. Implement (This would trigger the actual script updates/deployments)
        print(f"[+] Deploying strategy for {manifest['target_package']}...")
        # Simulation of deployment
        time.sleep(1) 
        
        # 3. Clear state
        state["pending_approval"] = None
        self._save_state(state)
        
        ledger.record(
            identity="ModMindValet",
            action="STRATEGY_EXECUTED",
            payload=manifest,
            rationale="Human approved strategy deployed to production."
        )
        
        print("✅ Deployment complete. Revenue pipeline active.")
        return True

if __name__ == "__main__":
    valet = ModMindValet()
    
    # 1. Check for new leads (External Input)
    lead = valet.check_for_leads()
    if lead:
        valet.orchestrate_insight(lead)
    
    # 2. Run Optimizer (Internal Feedback)
    from ModMind_optimizer import optimizer
    optimizer.optimize(valet=valet)
    
    # 3. Check for pending approvals (HITL)
    valet.execute_approved_strategy()
el-Bridge)
        valet.execute_approved_strategy()
