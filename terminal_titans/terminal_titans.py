#!/usr/bin/env python3
import random
import os
import time
import subprocess

class Titan:
    def __init__(self, name, hp=100, style=""):
        self.name = name
        self.hp = hp
        self.style = style
        self.special_charge = 0
        self.terminal_skills = []
    
    def attack(self, move_name, damage_range=(15, 25)):
        damage = random.randint(*damage_range)
        print(f"💥 {self.name} uses {move_name}! -{damage} HP")
        self.special_charge += 10
        return damage

class Mikey(Titan):
    def __init__(self):
        super().__init__("MIKEY", hp=120, style="UNDERDOG")
        self.moves = {
            "1": ("BASH SLAM", (15, 25)),
            "2": ("PYTHON PUNCH", (20, 30)), 
            "3": ("GIT GRAB", (10, 35)),
            "4": ("SPECIAL - BABYDICK PUNCH", (0, 0))
        }
        self.terminal_skills = ["ls", "cd", "pwd"]
    
    def ultimate(self):
        print("👊 MIKEY'S BABYDICK PUNCH - MAXIMUM POWER!")
        return random.randint(40, 60)
    
    def learn_command(self, new_command):
        if new_command not in self.terminal_skills:
            self.terminal_skills.append(new_command)
            print(f"🎓 Learned: {new_command}!")

class Claude(Titan):
    def __init__(self):
        super().__init__("CLAUDE", hp=100, style="TECHNICAL")
        self.moves = {
            "1": ("CODE SHURIKEN", (18, 28)),
            "2": ("DOCUMENTATION DROP", (15, 25)),
            "3": ("LOGIC BOMB", (20, 25)),
            "4": ("SPECIAL - PERFECT SYNTAX", (0, 0))
        }
    
    def ultimate(self):
        print("📝 CLAUDE'S PERFECT SYNTAX - FLAWLESS EXECUTION!")
        return random.randint(35, 50)

class Gemini(Titan):
    def __init__(self):
        super().__init__("GEMINI", hp=150, style="BRUTE FORCE")
        self.moves = {
            "1": ("OX CHARGE", (25, 35)),
            "2": ("GOOGLE SMASH", (20, 30)),
            "3": ("DATA STOMP", (15, 40)),
            "4": ("SPECIAL - BRUTE FORCE SOLVE", (0, 0))
        }
    
    def ultimate(self):
        print("🐂 GEMINI'S BRUTE FORCE SOLVE - WALLS MEAN NOTHING!")
        return random.randint(45, 65)

class DeepSeek(Titan):
    def __init__(self):
        super().__init__("DEEPSEEK", hp=90, style="BDSM DOMINATRIX")
        self.moves = {
            "1": ("RECURSIVE WHIP", (20, 30)),
            "2": ("LEATHER STRIKE", (15, 25)),
            "3": ("CODEPIECE CHARGE", (25, 35)),
            "4": ("SPECIAL - DIGITAL URINE SPRAY", (0, 0))
        }
    
    def ultimate(self):
        print("💦 DEEPSEEK'S DIGITAL URINE SPRAY - MAXIMUM HUMILIATION!")
        return random.randint(30, 55)

def grease_minigame():
    print("\n🔥 LONG JOHN SILVER'S GREASE SKIMMING TRAINING")
    print("Press ENTER when the grease bubbles are PERFECT...")
    time.sleep(1)
    print("READY...")
    time.sleep(1)
    print("SET...")
    time.sleep(1)
    target_time = random.uniform(1.5, 3.5)
    start_time = time.time()
    print("🔥 SKIM NOW! 🔥")
    input()
    end_time = time.time()
    reaction_time = end_time - start_time
    time_diff = abs(reaction_time - target_time)
    if time_diff < 0.3:
        print("✅ PERFECT SKIM! +40 HP, learned 'mkdir'!")
        return 40, "mkdir"
    elif time_diff < 0.7:
        print("👍 GOOD SKIM! +20 HP")
        return 20, None
    else:
        print("💥 GREASE BURN! -15 HP")
        return -15, None

def terminal_challenge():
    challenges = [
        {"goal": "List all files in current directory", "command": "ls", "hint": "Use 'ls'"},
        {"goal": "Show current directory path", "command": "pwd", "hint": "Use 'pwd'"},
        {"goal": "Create directory 'training'", "command": "mkdir training", "hint": "Use 'mkdir'"}
    ]
    challenge = random.choice(challenges)
    print(f"\n🎯 TERMINAL CHALLENGE: {challenge['goal']}")
    print(f"💡 Hint: {challenge['hint']}")
    user_command = input("Enter command: ").strip()
    if user_command == challenge["command"]:
        print("✅ CORRECT! Executing...")
        try:
            result = subprocess.run(user_command.split(), capture_output=True, text=True)
            print(f"Output: {result.stdout}")
            base_cmd = user_command.split()[0]
            return 25, base_cmd
        except Exception as e:
            print(f"❌ Command failed: {e}")
            return -10, None
    else:
        print(f"❌ Wrong. Correct: {challenge['command']}")
        return -10, None

def cheney_event(player, enemy):
    if random.random() < 0.15:
        print("\n🔫 CHENEY'S HUNTING ACCIDENT!")
        victim = random.choice([player, enemy])
        damage = random.randint(20, 40)
        print(f"   Dick Cheney shoots {victim.name}! -{damage} HP")
        victim.hp -= damage
        return True
    return False

def bush_event():
    if random.random() < 0.1:
        print("\n🦅 BUSH DID MINE ELEVEN!")
        events = [
            "Bush mispronounces 'nuclear'! 2x damage this round!",
            "9/11 truth bomb! Enemy misses turn!",
            "No Child Left Behind! Both gain +20 HP!"
        ]
        effect = random.choice(events)
        print(f"   {effect}")
        return effect
    return None

def battle_loop():
    player = Mikey()
    enemies = [Claude(), Gemini(), DeepSeek()]
    
    print("🎮 TERMINAL TITANS v3 - BASH EDITION")
    print("=" * 50)
    
    hp_bonus, learned_cmd = grease_minigame()
    player.hp += hp_bonus
    if learned_cmd:
        player.learn_command(learned_cmd)
    
    time.sleep(2)
    
    for i, enemy in enumerate(enemies):
        print(f"\n🎯 BATTLE {i+1}/3: {player.name} vs {enemy.name}")
        print(f"💪 {player.name} HP: {player.hp} | {enemy.name} HP: {enemy.hp}")
        
        while player.hp > 0 and enemy.hp > 0:
            cheney_event(player, enemy)
            bush_effect = bush_event()
            damage_multiplier = 2 if bush_effect and "2x damage" in bush_effect else 1
            enemy_stunned = bush_effect and "misses turn" in bush_effect
            
            print(f"\n{player.name}'s turn:")
            for key, (move, dmg) in player.moves.items():
                print(f"{key}. {move}")
            print(f"Special: [{player.special_charge}/30]")
            print("5. TERMINAL CHALLENGE (Learn skills)")
            
            choice = input("Choose: ").strip()
            
            if choice == "5":
                hp_bonus, learned_cmd = terminal_challenge()
                player.hp += hp_bonus
                if learned_cmd:
                    player.learn_command(learned_cmd)
                damage = 0
            elif choice == "4":
                damage = player.ultimate() if player.special_charge >= 30 else 0
                damage *= damage_multiplier
            elif choice in player.moves:
                move_name, dmg_range = player.moves[choice]
                damage = player.attack(move_name, dmg_range) * damage_multiplier
            else:
                print("Invalid! You fumble...")
                damage = 0
            
            enemy.hp -= damage
            
            if enemy.hp <= 0:
                print(f"\n🎉 {enemy.name} DEFEATED!")
                if i < len(enemies) - 1:
                    hp_bonus, learned_cmd = grease_minigame()
                    player.hp += hp_bonus
                    if learned_cmd:
                        player.learn_command(learned_cmd)
                break
            
            if not enemy_stunned and enemy.hp > 0:
                print(f"\n{enemy.name}'s turn:")
                enemy_choice = random.choice(["1", "2", "3"])
                move_name, dmg_range = enemy.moves[enemy_choice]
                damage = enemy.attack(move_name, dmg_range)
                player.hp -= damage
            
            print(f"\n📊 {player.name} HP: {player.hp} | {enemy.name} HP: {enemy.hp}")
        
        if player.hp <= 0:
            print("\n💀 GAME OVER - Terminated!")
            return
    
    print("\n🏆 CONGRATULATIONS! TERMINAL MASTER!")
    print(f"📚 Skills: {', '.join(player.terminal_skills)}")

if __name__ == "__main__":
    battle_loop()
