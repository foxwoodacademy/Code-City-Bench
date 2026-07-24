class WhorlCoordinator:
    """
    Manages swarm-like coordination without a central controller.
    """
    def __init__(self):
        self.nodes = []

    def register_node(self, node_id):
        self.nodes.append(node_id)

    def coordinate(self, weaver_signal):
        """Emergent response coordination."""
        return f"Whorl optimized for signal: {weaver_signal}"
