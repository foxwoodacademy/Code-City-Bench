#!/usr/bin/env python3
# FILE: /storage/emulated/0/code_tool/titan_battle.py
import random

class Fighter:
    def __init__(self, name, hp=100):
        self.name = name
        self.hp = hp
    
    def attack(self, move):
        damage = random.randint(15, 25)
        print(f"{self.name} uses {move}! -{damage} HP")
        return damage

def main():
    print("🤺 TERMINAL TITANS - BATTLE MODE")
    print("Mikey vs Claude")
    print()
    
    mikey = Fighter("MIKEY")
    claude = Fighter("CLAUDE")
    
    moves = ["BASH SLAM", "PYTHON PUNCH", "GIT GRAB", "SPECIAL MOVE"]
    
    while mikey.hp > 0 and claude.hp > 0:
        # Player turn
        print(f"Mikey HP: {mikey.hp} | Claude HP: {claude.hp}")
        print("1. BASH SLAM  2. PYTHON PUNCH  3. GIT GRAB  4. SPECIAL")
        
        try:
            choice = input("Attack: ").strip()
            if choice in ["1", "2", "3", "4"]:
                damage = mikey.attack(moves[int(choice)-1])
                claude.hp -= damage
            else:
                print("Invalid! You hesitate.")
                continue
        except:
            continue
        
        # Claude attacks back if alive
        if claude.hp > 0:
            damage = claude.attack(random.choice(moves))
            mikey.hp -= damage
        
        print()
    
    # Result
    if mikey.hp > 0:
        print("🎉 YOU WIN! Claude defeated!")
        print("Earned: Terminal XP +100")
    else:
        print("💀 You lost. Game over.")

if __name__ == "__main__":
    main()#!/usr/bin/env python3
# FILE: /storage/emulated/0/code_tool/titan_battle.py
import random

class Fighter:
    def __init__(self, name, hp=100):
        self.name = name
        self.hp = hp
    
    def attack(self, move):
        damage = random.randint(15, 25)
        print(f"{self.name} uses {move}! -{damage} HP")
        return damage

def main():
    print("🤺 TERMINAL TITANS - BATTLE MODE")
    print("Mikey vs Claude")
    print()
    
    mikey = Fighter("MIKEY")
    claude = Fighter("CLAUDE")
    
    moves = ["BASH SLAM", "PYTHON PUNCH", "GIT GRAB", "SPECIAL MOVE"]
    
    while mikey.hp > 0 and claude.hp > 0:
        # Player turn
        print(f"Mikey HP: {mikey.hp} | Claude HP: {claude.hp}")
        print("1. BASH SLAM  2. PYTHON PUNCH  3. GIT GRAB  4. SPECIAL")
        
        try:
            choice = input("Attack: ").strip()
            if choice in ["1", "2", "3", "4"]:
                damage = mikey.attack(moves[int(choice)-1])
                claude.hp -= damage
            else:
                print("Invalid! You hesitate.")
                continue
        except:
            continue
        
        # Claude attacks back if alive
        if claude.hp > 0:
            damage = claude.attack(random.choice(moves))
            mikey.hp -= damage
        
        print()
    
    # Result
    if mikey.hp > 0:
        print("🎉 YOU WIN! Claude defeated!")
        print("Earned: Terminal XP +100")
    else:
        print("💀 You lost. Game over.")

if __name__ == "__main__":
    main()