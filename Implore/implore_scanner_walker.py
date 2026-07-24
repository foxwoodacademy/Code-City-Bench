import os
from pathlib import Path

class RepoWalker:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)

    def walk(self):
        """Walk the directory and return all files"""
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                yield Path(root) / file
