"""
Kimi-Code: Six Thinking Hats for Code Analysis
Edward de Bono's methodology applied to software engineering.
"""
import random
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass

@dataclass
class HatPrompt:
    """Structured prompt for a thinking hat."""
    hat: str
    color: str
    emoji: str
    role: str
    focus: str
    questions: List[str]
    analysis_template: str

class SixHatsEngine:
    """Manages Six Thinking Hats analysis sessions."""

    HATS = {
        "white": HatPrompt(
            hat="white",
            color="#FFFFFF",
            emoji="📊",
            role="The Objective Analyst",
            focus="Facts, data, and objective information about the code",
            questions=[
                "What are the exact inputs and outputs?",
                "What dependencies does this code have?",
                "What is the time/space complexity?",
                "What data structures are used and why?",
                "What are the exact error conditions?",
                "What versions/frameworks does this require?"
            ],
            analysis_template="""
<h2>📊 White Hat: Objective Facts</h2>
<div class="hat-section white-hat">
<h3>Code Statistics</h3>
{stats}

<h3>Dependencies & Requirements</h3>
{dependencies}

<h3>Data Flow</h3>
{data_flow}

<h3>Complexity Metrics</h3>
{complexity}
</div>
"""
        ),
        "red": HatPrompt(
            hat="red",
            color="#FF4444",
            emoji="🔥",
            role="The Intuitive Critic",
            focus="Gut feelings, emotions, and subjective reactions to the code",
            questions=[
                "What's your immediate emotional reaction to this code?",
                "Does this code feel 'right' or 'wrong'?",
                "What makes you nervous about this implementation?",
                "Where does your intuition say the bugs are hiding?",
                "Does the naming and structure feel intuitive?",
                "Would you trust this code in production right now?"
            ],
            analysis_template="""
<h2>🔥 Red Hat: Intuition & Emotion</h2>
<div class="hat-section red-hat">
<h3>Gut Reaction</h3>
{gut_reaction}

<h3>Emotional Red Flags</h3>
{red_flags}

<h3>Trust Assessment</h3>
{trust_level}

<h3>Intuitive Bug Predictions</h3>
{bug_predictions}
</div>
"""
        ),
        "black": HatPrompt(
            hat="black",
            color="#333333",
            emoji="⚠️",
            role="The Devil's Advocate",
            focus="Risks, dangers, problems, and why this code might fail",
            questions=[
                "What could go wrong with this code?",
                "Where are the edge cases not handled?",
                "What security vulnerabilities exist?",
                "How could this fail under load?",
                "What assumptions does this code make?",
                "What's the worst-case scenario if this breaks?",
                "How could this be exploited maliciously?"
            ],
            analysis_template="""
<h2>⚠️ Black Hat: Risks & Cautions</h2>
<div class="hat-section black-hat">
<h3>Failure Modes</h3>
{failure_modes}

<h3>Security Vulnerabilities</h3>
{security_issues}

<h3>Edge Cases Missed</h3>
{edge_cases}

<h3>Assumptions & Dependencies</h3>
{assumptions}

<h3>Worst-Case Scenarios</h3>
{worst_cases}
</div>
"""
        ),
        "yellow": HatPrompt(
            hat="yellow",
            color="#FFD700",
            emoji="✨",
            role="The Optimist",
            focus="Benefits, value, and positive aspects of the code",
            questions=[
                "What does this code do well?",
                "What clever patterns or optimizations exist?",
                "How is this code extensible?",
                "What can we learn from this approach?",
                "How does this solve the problem elegantly?",
                "What would make this code exemplary?"
            ],
            analysis_template="""
<h2>✨ Yellow Hat: Benefits & Value</h2>
<div class="hat-section yellow-hat">
<h3>Strengths & Virtues</h3>
{strengths}

<h3>Clever Patterns</h3>
{patterns}

<h3>Extensibility Points</h3>
{extensibility}

<h3>Learning Opportunities</h3>
{lessons}
</div>
"""
        ),
        "green": HatPrompt(
            hat="green",
            color="#00FF88",
            emoji="🌱",
            role="The Creative Innovator",
            focus="New ideas, alternatives, and creative improvements",
            questions=[
                "How could this be rewritten more elegantly?",
                "What alternative algorithms could work?",
                "What features could be added to enhance this?",
                "How could we make this more maintainable?",
                "What design patterns could improve this?",
                "How would you approach this differently?"
            ],
            analysis_template="""
<h2>🌱 Green Hat: Creativity & Alternatives</h2>
<div class="hat-section green-hat">
<h3>Alternative Approaches</h3>
{alternatives}

<h3>Refactoring Opportunities</h3>
{refactoring}

<h3>Feature Extensions</h3>
{extensions}

<h3>Design Pattern Applications</h3>
{patterns}
</div>
"""
        ),
        "blue": HatPrompt(
            hat="blue",
            color="#0066FF",
            emoji="🧠",
            role="The Meta-Thinker",
            focus="Process, overview, and managing the thinking process itself",
            questions=[
                "What thinking process did we just use?",
                "What conclusions can we draw from all hats?",
                "What's the action plan based on this analysis?",
                "What did we miss in our analysis?",
                "How should we prioritize the findings?",
                "What's the next step for this code?"
            ],
            analysis_template="""
<h2>🧠 Blue Hat: Meta-Analysis & Action Plan</h2>
<div class="hat-section blue-hat">
<h3>Process Summary</h3>
{process_summary}

<h3>Synthesized Conclusions</h3>
{conclusions}

<h3>Priority Action Items</h3>
{action_items}

<h3>Next Steps</h3>
{next_steps}

<h3>Reflection</h3>
{reflection}
</div>
"""
        )
    }

    def __init__(self, state_engine=None):
        self.state = state_engine
        self.current_sequence = []
        self.current_index = 0

    def get_hat(self, hat_name: str) -> HatPrompt:
        """Get a hat configuration."""
        return self.HATS.get(hat_name.lower())

    def get_all_hats(self) -> List[str]:
        """Get all hat names."""
        return list(self.HATS.keys())

    def generate_sequence(self, mode: str = "standard", focus_hats: List[str] = None) -> List[str]:
        """Generate a thinking sequence.

        Modes:
        - standard: white -> red -> black -> yellow -> green -> blue
        - quick: white -> black -> green -> blue
        - deep: Each hat gets extra time, blue at start and end
        - random: Random order (for breaking bias)
        - focus: Focus on specific hats
        """
        all_hats = list(self.HATS.keys())

        if mode == "standard":
            sequence = ["white", "red", "black", "yellow", "green", "blue"]
        elif mode == "quick":
            sequence = ["white", "black", "green", "blue"]
        elif mode == "deep":
            sequence = ["blue", "white", "red", "black", "yellow", "green", "blue"]
        elif mode == "random":
            sequence = all_hats.copy()
            random.shuffle(sequence)
        elif mode == "focus" and focus_hats:
            sequence = [h for h in focus_hats if h in all_hats]
            if "blue" not in sequence:
                sequence.append("blue")  # Always end with blue
        else:
            sequence = ["white", "red", "black", "yellow", "green", "blue"]

        self.current_sequence = sequence
        self.current_index = 0
        return sequence

    def get_current_hat(self) -> Optional[HatPrompt]:
        """Get the current hat in sequence."""
        if self.current_index < len(self.current_sequence):
            return self.get_hat(self.current_sequence[self.current_index])
        return None

    def next_hat(self) -> Optional[HatPrompt]:
        """Move to next hat in sequence."""
        self.current_index += 1
        return self.get_current_hat()

    def generate_prompt_for_hat(self, hat_name: str, code: str, context: Dict = None) -> str:
        """Generate an AI prompt for a specific hat analysis."""
        hat = self.get_hat(hat_name)
        if not hat:
            return ""

        questions_text = "
".join([f"{i+1}. {q}" for i, q in enumerate(hat.questions)])

        prompt = f"""You are wearing the {hat.emoji} {hat.role} ({hat.hat.title()} Hat).

ROLE: {hat.focus}

Analyze this code through the lens of the {hat.hat.title()} Hat:

```
{code}
```

Answer these questions:
{questions_text}

Provide your analysis in HTML format using the following structure:
{hat.analysis_template}

Replace each placeholder ({{stats}}, {{gut_reaction}}, etc.) with actual content.
Keep it concise but insightful. Use specific examples from the code.
"""
        return prompt

    def generate_full_analysis_prompt(self, code: str, sequence: List[str] = None) -> str:
        """Generate a prompt for full six-hats analysis."""
        seq = sequence or self.generate_sequence("standard")

        hats_section = "

".join([
            f"### {self.HATS[h].emoji} {h.title()} Hat: {self.HATS[h].focus}
" +
            f"Key questions: {', '.join(self.HATS[h].questions[:3])}"
            for h in seq
        ])

        prompt = f"""Perform a complete Six Thinking Hats analysis on this code:

```
{code}
```

ANALYSIS SEQUENCE: {' → '.join([h.title() for h in seq])}

{hats_section}

For each hat, provide:
1. A brief summary (2-3 sentences)
2. Key findings as bullet points
3. A specific recommendation

Format the entire response as HTML with styled sections for each hat.
Use these colors for sections:
- White: #FFFFFF background, #333 text
- Red: #FF4444 accent
- Black: #333333 background, #FF6B6B accents
- Yellow: #FFD700 accent
- Green: #00FF88 accent  
- Blue: #0066FF accent

End with a Blue Hat synthesis that prioritizes all findings into an action plan.
"""
        return prompt

    def get_challenge_for_hat(self, hat_name: str, difficulty: int, language: str) -> Dict:
        """Generate a challenge focused on a specific hat."""
        hat = self.get_hat(hat_name)

        challenge_types = {
            "white": ["analyze_complexity", "trace_data_flow", "map_dependencies", "document_api"],
            "red": ["intuitive_debug", "smell_detection", "trust_audit", "gut_review"],
            "black": ["find_vulnerabilities", "edge_case_hunt", "failure_mode_analysis", "security_audit"],
            "yellow": ["identify_patterns", "extensibility_review", "optimization_spotting", "elegance_analysis"],
            "green": ["refactor_proposal", "alternative_design", "feature_extension", "pattern_application"],
            "blue": ["synthesis_exercise", "prioritization_task", "process_review", "action_planning"]
        }

        types = challenge_types.get(hat_name, ["general_analysis"])
        selected = random.choice(types)

        return {
            "hat": hat_name,
            "type": selected,
            "difficulty": difficulty,
            "language": language,
            "focus": hat.focus,
            "description": f"Apply the {hat.emoji} {hat.hat.title()} Hat to analyze code",
            "success_criteria": self._get_success_criteria(hat_name, difficulty),
            "time_limit": difficulty * 60,  # seconds
            "xp_reward": difficulty * 20
        }

    def _get_success_criteria(self, hat_name: str, difficulty: int) -> List[str]:
        """Get success criteria for a hat challenge."""
        criteria = {
            "white": [
                "Identified all inputs and outputs",
                "Correctly mapped dependencies",
                "Accurate complexity assessment",
                "Complete data structure inventory"
            ],
            "red": [
                "Articulated gut reaction clearly",
                "Identified intuitive red flags",
                "Assessed trust level honestly",
                "Predicted potential bug locations"
            ],
            "black": [
                "Found at least {n} security issues".format(n=max(1, difficulty-2)),
                "Identified edge cases",
                "Listed failure modes",
                "Assessed worst-case scenarios"
            ],
            "yellow": [
                "Identified code strengths",
                "Found clever patterns",
                "Noted extensibility points",
                "Extracted learning value"
            ],
            "green": [
                "Proposed alternative approach",
                "Suggested refactoring",
                "Identified extension opportunities",
                "Applied design patterns"
            ],
            "blue": [
                "Synthesized all perspectives",
                "Created prioritized action plan",
                "Identified process improvements",
                "Defined clear next steps"
            ]
        }
        return criteria.get(hat_name, ["Complete analysis provided"])

    def get_hat_balance_report(self, hat_stats: Dict) -> Dict:
        """Analyze hat usage balance and recommend focus areas."""
        levels = {h: stats["level"] for h, stats in hat_stats.items()}
        avg_level = sum(levels.values()) / len(levels)

        weak_hats = [h for h, lvl in levels.items() if lvl < avg_level - 1]
        strong_hats = [h for h, lvl in levels.items() if lvl > avg_level + 1]

        return {
            "average_level": round(avg_level, 1),
            "weakest_hats": weak_hats,
            "strongest_hats": strong_hats,
            "balance_score": 1 - (max(levels.values()) - min(levels.values())) / 20,
            "recommendation": f"Focus on: {', '.join(weak_hats)}" if weak_hats else "Well balanced!",
            "suggested_sequence": self._generate_balanced_sequence(weak_hats)
        }

    def _generate_balanced_sequence(self, weak_hats: List[str]) -> List[str]:
        """Generate a sequence that emphasizes weak hats."""
        all_hats = ["white", "red", "black", "yellow", "green", "blue"]

        # Put weak hats first, then standard order for rest
        sequence = weak_hats.copy()
        for h in all_hats:
            if h not in sequence:
                sequence.append(h)

        return sequence
