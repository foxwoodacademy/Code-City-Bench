import math
import random
from pathlib import Path

class ModMindSigil:
    """
    The ModMind Sigil Engine.
    Generates a procedural SVG talisman based on the system's 'DNA'.
    """
    def __init__(self):
        self.base_color = "#00ff00" # ModMind Green

    def generate(self, revenue=0, crystals=0, safety_score=1.0):
        """
        Generates an SVG string based on system metrics.
        - Revenue -> Complexity and Scale
        - Crystals -> Number of geometric vertices
        - Safety -> Symmetry and Stability
        """
        # Normalize metrics for geometry
        nodes = max(3, min(12, 3 + (crystals // 5))) # 3 to 12 points
        radius = max(20, min(100, 20 + (revenue // 100000))) # Growth based on revenue
        stability = safety_score # 0.0 to 1.0
        
        # Determine color based on state (Green -> Gold -> Purple)
        if revenue > 1000000:
            color = "#bf00ff" # Imperial Purple
        elif revenue > 100000:
            color = "#ffd700" # ModMind Gold
        else:
            color = self.base_color

        # Generate the points of the sigil
        points = []
        for i in range(nodes):
            angle = (2 * math.pi * i) / nodes
            # Add 'jitter' based on instability (1 - safety)
            jitter = (random.random() - 0.5) * (1.0 - stability) * 20
            x = 100 + (radius + jitter) * math.cos(angle)
            y = 100 + (radius + jitter) * math.sin(angle)
            points.append(f"{x},{y}")

        points_str = " ".join(points)
        
        # Construct the SVG
        svg = f'''<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <filter id="glow">
                    <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
                    <feMerge>
                        <feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
            </defs>
            <circle cx="100" cy="100" r="5" fill="{color}" />
            <polygon points="{points_str}" fill="none" stroke="{color}" stroke-width="2" filter="url(#glow)">
                <animate attributeName="stroke-width" values="2;4;2" dur="3s" repeatCount="indefinite" />
            </polygon>
            <circle cx="100" cy="100" r="{radius}" fill="none" stroke="{color}" stroke-width="0.5" stroke-dasharray="5,5" opacity="0.3" />
        </svg>'''
        
        return svg

# Global instance
sigil_engine = ModMindSigil()
