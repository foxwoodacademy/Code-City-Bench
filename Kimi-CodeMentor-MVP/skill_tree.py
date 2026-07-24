
# Skill Tree - visual progression system
skill_tree_py = '''"""
Kimi-Code: Skill Tree
Visual progression system with unlockable nodes and dependencies.
"""
import json
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict

@dataclass
class SkillNode:
    """Represents a skill in the tree."""
    id: str
    name: str
    description: str
    category: str
    level: int
    max_level: int
    xp_cost: int
    prerequisites: List[str]
    unlocks: List[str]
    icon: str
    color: str
    effects: Dict[str, float]
    unlocked: bool = False
    completed: bool = False

class SkillTree:
    """Manages the skill progression tree."""
    
    # Predefined skill tree structure
    NODES = {
        # Root nodes (no prerequisites)
        "code_reading": SkillNode(
            id="code_reading", name="Code Reading", 
            description="Ability to understand and parse code quickly",
            category="fundamentals", level=1, max_level=10, xp_cost=100,
            prerequisites=[], unlocks=["debugging", "refactoring"],
            icon="👁️", color="#4ade80",
            effects={"comprehension_speed": 1.1, "pattern_recognition": 1.05}
        ),
        "syntax_mastery": SkillNode(
            id="syntax_mastery", name="Syntax Mastery",
            description="Deep understanding of language syntax and semantics",
            category="fundamentals", level=1, max_level=10, xp_cost=100,
            prerequisites=[], unlocks=["metaprogramming", "code_generation"],
            icon="📝", color="#60a5fa",
            effects={"error_detection": 1.1, "code_confidence": 1.05}
        ),
        "problem_decomposition": SkillNode(
            id="problem_decomposition", name="Problem Decomposition",
            description="Break complex problems into manageable pieces",
            category="fundamentals", level=1, max_level=10, xp_cost=100,
            prerequisites=[], unlocks=["algorithm_design", "system_design"],
            icon="🧩", color="#fbbf24",
            effects={"planning_speed": 1.1, "solution_clarity": 1.05}
        ),
        
        # Tier 2 (requires fundamentals)
        "debugging": SkillNode(
            id="debugging", name="Debugging",
            description="Systematic bug finding and fixing",
            category="execution", level=0, max_level=10, xp_cost=200,
            prerequisites=["code_reading"], unlocks=["testing", "profiling"],
            icon="🐛", color="#f87171",
            effects={"bug_detection": 1.15, "fix_speed": 1.1}
        ),
        "refactoring": SkillNode(
            id="refactoring", name="Refactoring",
            description="Improve code without changing behavior",
            category="execution", level=0, max_level=10, xp_cost=200,
            prerequisites=["code_reading"], unlocks=["optimization", "clean_code"],
            icon="♻️", color="#34d399",
            effects={"code_quality": 1.15, "maintainability": 1.1}
        ),
        "algorithm_design": SkillNode(
            id="algorithm_design", name="Algorithm Design",
            description="Create efficient algorithms for problems",
            category="design", level=0, max_level=10, xp_cost=250,
            prerequisites=["problem_decomposition"], unlocks=["complexity_analysis", "parallel_algorithms"],
            icon="⚡", color="#fbbf24",
            effects={"efficiency": 1.15, "solution_diversity": 1.1}
        ),
        "system_design": SkillNode(
            id="system_design", name="System Design",
            description="Design scalable software architectures",
            category="design", level=0, max_level=10, xp_cost=300,
            prerequisites=["problem_decomposition"], unlocks=["distributed_systems", "microservices"],
            icon="🏗️", color="#a78bfa",
            effects={"scalability_awareness": 1.2, "architecture_quality": 1.15}
        ),
        
        # Tier 3 (advanced)
        "testing": SkillNode(
            id="testing", name="Testing",
            description="Comprehensive test strategy and implementation",
            category="quality", level=0, max_level=10, xp_cost=300,
            prerequisites=["debugging"], unlocks=["tdd", "fuzzing"],
            icon="🧪", color="#f472b6",
            effects={"coverage": 1.2, "confidence": 1.15}
        ),
        "security_awareness": SkillNode(
            id="security_awareness", name="Security Awareness",
            description="Identify and mitigate security risks",
            category="quality", level=0, max_level=10, xp_cost=350,
            prerequisites=["debugging", "refactoring"], unlocks=["penetration_testing", "cryptography"],
            icon="🔒", color="#ef4444",
            effects={"vulnerability_detection": 1.25, "secure_coding": 1.2}
        ),
        "optimization": SkillNode(
            id="optimization", name="Optimization",
            description="Maximize performance and resource efficiency",
            category="advanced", level=0, max_level=10, xp_cost=350,
            prerequisites=["refactoring", "algorithm_design"], unlocks=["compiler_optimization", "gpu_programming"],
            icon="🚀", color="#f97316",
            effects={"performance": 1.2, "resource_efficiency": 1.15}
        ),
        
        # Six Thinking Hats specialization
        "white_hat_mastery": SkillNode(
            id="white_hat_mastery", name="White Hat Mastery",
            description="Objective data analysis and fact-based reasoning",
            category="hats", level=0, max_level=10, xp_cost=150,
            prerequisites=["code_reading"], unlocks=["data_driven_decisions"],
            icon="📊", color="#ffffff",
            effects={"fact_accuracy": 1.2, "metric_awareness": 1.15}
        ),
        "red_hat_mastery": SkillNode(
            id="red_hat_mastery", name="Red Hat Mastery",
            description="Intuitive understanding and emotional intelligence",
            category="hats", level=0, max_level=10, xp_cost=150,
            prerequisites=["code_reading"], unlocks=["intuitive_debugging"],
            icon="🔥", color="#ff4444",
            effects={"intuition": 1.2, "gut_accuracy": 1.15}
        ),
        "black_hat_mastery": SkillNode(
            id="black_hat_mastery", name="Black Hat Mastery",
            description="Risk assessment and critical analysis",
            category="hats", level=0, max_level=10, xp_cost=150,
            prerequisites=["debugging"], unlocks=[["security_awareness"]],
            icon="⚠️", color="#333333",
            effects={"risk_detection": 1.25, "critical_thinking": 1.2}
        ),
        "yellow_hat_mastery": SkillNode(
            id="yellow_hat_mastery", name="Yellow Hat Mastery",
            description="Optimistic design and value identification",
            category="hats", level=0, max_level=10, xp_cost=150,
            prerequisites=["refactoring"], unlocks=["opportunity_detection"],
            icon="✨", color="#ffd700",
            effects={"value_spotting": 1.2, "optimism": 1.15}
        ),
        "green_hat_mastery": SkillNode(
            id="green_hat_mastery", name="Green Hat Mastery",
            description="Creative problem solving and innovation",
            category="hats", level=0, max_level=10, xp_cost=150,
            prerequisites=["algorithm_design"], unlocks=["innovation"],
            icon="🌱", color="#00ff88",
            effects={"creativity": 1.25, "solution_diversity": 1.2}
        ),
        "blue_hat_mastery": SkillNode(
            id="blue_hat_mastery", name="Blue Hat Mastery",
            description="Meta-cognition and process management",
            category="hats", level=0, max_level=10, xp_cost=150,
            prerequisites=["system_design"], unlocks=["leadership"],
            icon="🧠", color="#0066ff",
            effects={"process_control": 1.2, "synthesis": 1.25}
        ),
        
        # Master tier
        "fullstack_mastery": SkillNode(
            id="fullstack_mastery", name="Fullstack Mastery",
            description="Complete end-to-end development expertise",
            category="master", level=0, max_level=5, xp_cost=1000,
            prerequisites=["system_design", "testing", "optimization"],
            unlocks=["architect"],
            icon="🎯", color="#ec4899",
            effects={"versatility": 1.3, "delivery_speed": 1.2}
        ),
        "architect": SkillNode(
            id="architect", name="Software Architect",
            description="Design and lead complex software systems",
            category="master", level=0, max_level=5, xp_cost=2000,
            prerequisites=["fullstack_mastery", "blue_hat_mastery"],
            unlocks=[],
            icon="👑", color="#fbbf24",
            effects={"leadership": 1.3, "vision": 1.25, "impact": 1.2}
        )
    }
    
    def __init__(self, state_engine=None):
        self.state = state_engine
        self.user_nodes = {}
        self._load_progress()
    
    def _load_progress(self):
        """Load user's skill tree progress."""
        if self.state and "skill_tree_nodes" in self.state.state:
            saved = self.state.state["skill_tree_nodes"]
            for node_id, data in saved.items():
                if node_id in self.NODES:
                    self.user_nodes[node_id] = {**asdict(self.NODES[node_id]), **data}
        
        # Initialize any missing nodes
        for node_id, node in self.NODES.items():
            if node_id not in self.user_nodes:
                self.user_nodes[node_id] = asdict(node)
    
    def save_progress(self):
        """Save skill tree progress."""
        if self.state:
            self.state.state["skill_tree_nodes"] = self.user_nodes
            self.state.save()
    
    def get_available_nodes(self) -> List[Dict]:
        """Get nodes that can be unlocked."""
        available = []
        for node_id, node in self.user_nodes.items():
            if not node["unlocked"]:
                # Check prerequisites
                prereqs_met = all(
                    self.user_nodes.get(p, {}).get("completed", False)
                    for p in node["prerequisites"]
                )
                if prereqs_met:
                    available.append(node)
        return available
    
    def get_unlocked_nodes(self) -> List[Dict]:
        """Get currently unlocked nodes."""
        return [n for n in self.user_nodes.values() if n["unlocked"]]
    
    def get_completed_nodes(self) -> List[Dict]:
        """Get completed nodes."""
        return [n for n in self.user_nodes.values() if n["completed"]]
    
    def unlock_node(self, node_id: str) -> bool:
        """Unlock a node if prerequisites are met."""
        if node_id not in self.user_nodes:
            return False
        
        node = self.user_nodes[node_id]
        if node["unlocked"]:
            return True
        
        # Check prerequisites
        for prereq in node["prerequisites"]:
            prereq_node = self.user_nodes.get(prereq)
            if not prereq_node or not prereq_node["completed"]:
                return False
        
        # Check XP cost
        if self.state and self.state.state["global_xp"] < node["xp_cost"]:
            return False
        
        # Unlock
        node["unlocked"] = True
        if self.state:
            self.state.state["global_xp"] -= node["xp_cost"]
        
        self.save_progress()
        return True
    
    def level_up_node(self, node_id: str) -> bool:
        """Level up an unlocked node."""
        if node_id not in self.user_nodes:
            return False
        
        node = self.user_nodes[node_id]
        if not node["unlocked"]:
            return False
        
        if node["level"] >= node["max_level"]:
            node["completed"] = True
            self.save_progress()
            return True
        
        # Calculate XP cost for next level (increases with level)
        next_level_cost = node["xp_cost"] * (1 + node["level"] * 0.5)
        
        if self.state and self.state.state["global_xp"] < next_level_cost:
            return False
        
        node["level"] += 1
        if self.state:
            self.state.state["global_xp"] -= next_level_cost
        
        if node["level"] >= node["max_level"]:
            node["completed"] = True
        
        self.save_progress()
        return True
    
    def get_tree_visualization(self) -> Dict:
        """Generate data for visual tree representation."""
        nodes = []
        edges = []
        
        for node_id, node in self.user_nodes.items():
            nodes.append({
                "id": node_id,
                "label": node["name"],
                "category": node["category"],
                "level": node["level"],
                "max_level": node["max_level"],
                "unlocked": node["unlocked"],
                "completed": node["completed"],
                "icon": node["icon"],
                "color": node["color"],
                "xp_cost": node["xp_cost"]
            })
            
            for prereq in node["prerequisites"]:
                edges.append({
                    "from": prereq,
                    "to": node_id,
                    "active": node["unlocked"]
                })
        
        return {"nodes": nodes, "edges": edges}
    
    def get_active_effects(self) -> Dict[str, float]:
        """Get cumulative effects from unlocked nodes."""
        effects = {}
        
        for node in self.user_nodes.values():
            if node["unlocked"]:
                for effect, value in node.get("effects", {}).items():
                    # Apply level scaling
                    scaled_value = 1 + (value - 1) * (node["level"] / node["max_level"])
                    effects[effect] = effects.get(effect, 1.0) * scaled_value
        
        return effects
    
    def get_category_summary(self) -> Dict:
        """Get summary by category."""
        categories = {}
        
        for node in self.user_nodes.values():
            cat = node["category"]
            if cat not in categories:
                categories[cat] = {"total": 0, "unlocked": 0, "completed": 0, "total_levels": 0}
            
            categories[cat]["total"] += 1
            categories[cat]["total_levels"] += node["max_level"]
            
            if node["unlocked"]:
                categories[cat]["unlocked"] += 1
            if node["completed"]:
                categories[cat]["completed"] += 1
        
        return categories
'''

with open(f"{base_dir}/core/skill_tree.py", 'w') as f:
    f.write(skill_tree_py)

print("✅ skill_tree.py written")