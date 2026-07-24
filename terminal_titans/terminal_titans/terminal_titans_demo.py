# FILE: /storage/emulated/0/code_tool/terminal_titans_demo.py
import random
import time
import os

class TerminalTitan:
    def __init__(self, name, health=100, attack_power=20):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.special_attack = "UNKNOWN"
    
    def bash_attack(self):
        damage = random.randint(10, self.attack_power)
        print(f"💥 {self.name} uses BASH SLAM! -{damage} HP")
        return damage
    
    def python_punch(self):
        damage = random.randint(15, self.attack_power + 5)
        print(f"🐍 {self.name} throws PYTHON PUNCH! -{damage} HP")
        return damage
    
    def git_grab(self):
        damage = random.randint(5, self.attack_power)
        print(f"📚 {self.name} executes GIT GRAB! -{damage} HP")
        return damage

class Claude(TerminalTitan):
    def __init__(self):
        super().__init__("CLAUDE", health=120, attack_power=25)
        self.special_attack = "CODE SHURIKEN"
    
    def special_move(self):
        damage = random.randint(20, 35)
        print(f"🌀 {self.name} unleashes {self.special_attack}!")
        print("   Perfectly formatted code blocks fly everywhere!")
        return damage

class Mikey(TerminalTitan):
    def __init__(self):
        super().__init__("MIKEY", health=80, attack_power=30)
        self.special_attack = "BABYDICK PUNCH"
    
    def special_move(self):
        damage = random.randint(25, 40)
        print(f"👊 {self.name} lands the {self.special_attack}!")
        print("   It's super effective against corporate AI!")
        return damage

def battle_loop():
    print("🎮 TERMINAL TITANS - BETA COMBAT DEMO")
    print("=" * 50)
    
    player = Mikey()
    enemy = Claude()
    
    print(f"🤺 BATTLE: {player.name} vs {enemy.name}")
    print(f"💪 {player.name} HP: {player.health} | {enemy.name} HP: {enemy.health}")
    print()
    
    round_num = 1
    
    while player.health > 0 and enemy.health > 0:
        print(f"🔄 ROUND {round_num}")
        print("1. Bash Attack")
        print("2. Python Punch") 
        print("3. Git Grab")
        print("4. SPECIAL MOVE")
        
        try:
            choice = input("Choose your attack (1-4): ")
            
            if choice == "1":
                damage = player.bash_attack()
                enemy.health -= damage
            elif choice == "2":
                damage = player.python_punch()
                enemy.health -= damage
            elif choice == "3":
                damage = player.git_grab()
                enemy.health -= damage
            elif choice == "4":
                damage = player.special_move()
                enemy.health -= damage
            else:
                print("❌ Invalid move! You stumble...")
                continue
                
            # Enemy attacks back
            if enemy.health > 0:
                enemy_attack = random.choice([enemy.bash_attack, enemy.python_punch, enemy.git_grab])
                damage = enemy_attack()
                player.health -= damage
            
            print(f"📊 STATUS: {player.name} HP: {player.health} | {enemy.name} HP: {enemy.health}")
            print("-" * 30)
            round_num += 1
            
        except KeyboardInterrupt:
            print("\n🛑 Battle interrupted! WIMP!")
            return
    
    # Battle result
    if player.health > 0:
        print(f"🎉 VICTORY! {player.name} DEFEATED {enemy.name}!")
        print("   You earned: +100 TERMINAL XP")
        print("   Unlocked: docker-compose kill")
    else:
        print(f"💀 DEFEAT! {enemy.name} CRUSHED YOU!")
        print("   Game Over... for now")
    
    print("\n🚀 TO BE CONTINUED IN TERMINAL TITANS: FULL EDITION!")

if __name__ == "__main__":
    os.system("clear")
    battle_loop()