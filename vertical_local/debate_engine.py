import random
import time
from typing import List, Dict, Any, Optional
from scout_sandbox import scout_respond

# Optional real-world connectors: Thoth and swarm scouts. Fall back to scout_sandbox when unavailable.
try:
    import thoth_client
except Exception:
    thoth_client = None
try:
    import swarm_client
except Exception:
    swarm_client = None


class DebateOrchestrator:
    """
    Orchestrates a debate between multiple personas using real or simulated intelligence.
    """
    def __init__(
        self, 
        case_text: str, 
        personas: List[Dict], 
        turns: int = 3, 
        sims: int = 25, 
        seed: Optional[int] = None, 
        use_thoth: bool = False, 
        use_scouts: bool = False
    ):
        self.case_text = case_text
        self.personas = personas
        self.turns = turns
        self.sims = sims
        self.rng = random.Random(seed or int(time.time()))
        self.use_thoth = use_thoth
        self.use_scouts = use_scouts

        # State management
        self.debate_log: List[Dict] = []
        self.positions: Dict[str, str] = {p['id']: p.get('bio', '') for p in personas}

    def _get_persona_reply(self, persona: Dict, turn: int) -> str:
        """Handles the logic of fetching a response from the appropriate provider."""
        prompt = f"CASE: {self.case_text}\nTURN: {turn+1}\nPREVIOUS: {self.positions.get(persona['id'], '')}"

        # 1. Attempt Thoth (if requested and available)
        if self.use_thoth and thoth_client is not None:
            try:
                return thoth_client.respond(persona=persona, prompt=prompt)
            except Exception as e:
                # Fallback to sandbox on failure, but log or handle specifically if needed
                pass

        # 2. Attempt Swarm Scouts (if requested and available)
        if self.use_scouts and swarm_client is not None:
            try:
                return swarm_client.scout_respond(persona=persona, prompt=prompt)
            except Exception:
                pass

        # 3. Default to Scout Sandbox
        return scout_respond(persona=persona, prompt=prompt, rng=self.rng)

    def _run_turn(self, turn_idx: int) -> Dict:
        """Executes a single turn of the debate for all personas."""
        turn_entries = []
        for p in self.personas:
            reply = self._get_persona_reply(p, turn_idx)

            # Update position summary (limit to 2000 chars to prevent bloat)
            new_pos = (self.positions.get(p['id'], '') + '\n' + reply)[:2000]
            self.positions[p['id']] = new_pos

            turn_entries.append({
                'persona_id': p['id'], 
                'name': p['name'], 
                'reply': reply
            })

        return {'turn': turn_idx + 1, 'entries': turn_entries}

    def _run_market_simulations(self) -> List[Dict[str, float]]:
        """Runs stochastic simulations to determine persona influence/scores."""
        sim_results = []
        for _ in range(self.sims):
            scores = {}
            for p in self.personas:
                # persona influence based on strategy length + randomness
                base = self.rng.random()
                strategy_bonus = (len(p.get('strategy') or '') % 10) * 0.01
                scores[p['id']] = base + strategy_bonus

            # Normalize scores to sum to 1.0
            total = sum(scores.values()) or 1.0
            normalized = {pid: round(val/total, 4) for pid, val in scores.items()}
            sim_results.append(normalized)

        return sim_results

    def _aggregate_results(self, sim_results: List[Dict[str, float]]) -> Dict[str, float]:
        """Computes mean scores across all simulations."""
        agg = {}
        for p in self.personas:
            pid = p['id']
            vals = [r[pid] for r in sim_results]
            agg[pid] = round(sum(vals)/len(vals), 4)
        return agg

    def _build_report(self, sim_results: List[Dict[str, float]], agg_scores: Dict[str, float]) -> Dict[str, Any]:
        """Constructs the final structured report."""
        return {
            'case': self.case_text,
            'turns': self.debate_log,
            'simulations': {
                'count': self.sims, 
                'raw': sim_results[:10] # Return sample for brevity
            },
            'scores': agg_scores,
            'personas': {p['id']: p for p in self.personas},
        }

    def orchestrate(self) -> Dict[str, Any]:
        """Main execution loop."""
        # 1. Execute Debate Turns
        for turn_idx in range(self.turns):
            turn_data = self._run_turn(turn_idx)
            self.debate_log.append(turn_data)

        # 2. Run Simulations
        sim_results = self._run_market_simulations()

        # 3. Aggregate and Report
        agg_scores = self._aggregate_results(sim_results)
        return self._build_report(sim_results, agg_scores)


def run_debate(case_text: str, personas: List[Dict], turns: int = 3, sims: int = 25, seed: int | None = None, use_thoth: bool = False, use_scouts: bool = False) -> Dict[str, Any]:
    """
    Orchestrate a debate between multiple personas using the scout_sandbox.
    Returns a report dict with turns and simulated market scores.
    """
    orchestrator = DebateOrchestrator(
        case_text=case_text,
        personas=personas,
        turns=turns,
        sims=sims,
        seed=seed,
        use_thoth=use_thoth,
        use_scouts=use_scouts
    )
    return orchestrator.orchestrate()