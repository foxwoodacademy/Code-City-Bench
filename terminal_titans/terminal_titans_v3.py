#!/usr/bin/env python3
# FILE: /storage/emulated/0/code_tool/terminal_titans_v3.py
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
    
    def special_attack(self):
        if self.special_charge >= 30:
            damage = random.randint(30, 45)
            print(f"🌀 {self.name} unleashes ULTIMATE MOVE!")
            self.special_charge = 0
            return damage
        else:
            print(f"❌ Special not ready! ({self.special_charge}/30)")
            return 0

class Mikey(Titan):
    def __init__(self):
        super().__init__("MIKEY", hp=120, style="UNDERDOG")
        self.moves = {
            "1": ("BASH SLAM", (15, 25)),
            "2": ("PYTHON PUNCH", (20, 30)), 
            "3": ("GIT GRAB", (10, 35)),
            "4": ("SPECIAL - BABYDICK PUNCH", (0, 0))
        }
        self.terminal_skills = ["ls", "cd", "pwd"]  # Starting skills
    
    def ultimate(self):
        print("👊 MIKEY'S BABYDICK PUNCH - MAXIMUM POWER!")
        return random.randint(40, 60)
    
    def learn_command(self, new_command):
        if new_command not in self.terminal_skills:
            self.terminal_skills.append(new_command)
            print(f"🎓 Mikey learned: {new_command}!")

def grease_minigame():
    """Long John Silver's Grease Skimming Simulator"""
    print("\n🔥 LONG JOHN SILVER'S GREASE SKIMMING TRAINING")
    print("Don't drop the fish! Time your keypresses!")
    print("Press ENTER when the grease bubbles are PERFECT...")
    
    time.sleep(1)
    print("\nREADY...")
    time.sleep(1)
    print("SET...")
    time.sleep(1)
    
    target_time = random.uniform(1.5, 3.5)
    start_time = time.time()
    
    print("🔥 SKIM NOW! 🔥")
    input()  # Wait for user press
    
    end_time = time.time()
    reaction_time = end_time - start_time
    
    # Score based on how close to target time
    time_diff = abs(reaction_time - target_time)
    
    if time_diff < 0.3:
        print("✅ PERFECT SKIM! Masterful grease control!")
        print("   +40 HP and learned 'mkdir'!")
        return 40, "mkdir"
    elif time_diff < 0.7:
        print("👍 GOOD SKIM! Minor grease splash.")
        print("   +20 HP")
        return 20, None
    else:
        print("💥 GREASE BURN! You dropped the fish!")
        print("   -15 HP and got yelled at by manager")
        return -15, None

def actual_terminal_challenge():
    """Execute real terminal commands"""
    challenges = [
        {
            "goal": "List all files in current directory",
            "command": "ls",
            "hint": "Use 'ls' to list contents"
        },
        {
            "goal": "Show current directory path", 
            "command": "pwd",
            "hint": "Use 'pwd' for present working directory"
        },
        {
            "goal": "Create a directory called 'training'",
            "command": "mkdir training",
            "hint": "Use 'mkdir' followed by directory name"
        }
    ]
    
    challenge = random.choice(challenges)
    
    print(f"\n🎯 TERMINAL CHALLENGE: {challenge['goal']}")
    print(f"💡 Hint: {challenge['hint']}")
    
    user_command = input("Enter command: ").strip()
    
    if user_command == challenge["command"]:
        print("✅ CORRECT! Executing command...")
        try:
            result = subprocess.run(user_command.split(), capture_output=True, text=True)
            print(f"Output: {result.stdout}")
            
            # Learn new commands from successful execution
            base_cmd = user_command.split()[0]
            return 25, base_cmd
        except Exception as e:
            print(f"❌ Command failed: {e}")
            return -10, None
    else:
        print(f"❌ Wrong command. Correct was: {challenge['command']}")
        return -10, None

def cheney_event(player, enemy):
    """Random Cheney hunting accident"""
    if random.random() < 0.15:  # 15% chance
        print("\n🔫 CHENEY'S HUNTING ACCIDENT!")
        victim = random.choice([player, enemy])
        damage = random.randint(20, 40)
        print(f"   Dick Cheney 'accidentally' shoots {victim.name}!")
        print(f"   -{damage} HP to {victim.name}")
        victim.hp -= damage
        
        # Sometimes Cheney "helps" by shooting your enemy
        if victim == enemy:
            print("   ...but it actually helped you!")
        return True
    return False

def bush_conspiracy_event():
    """Bush did mine eleven random event"""
    if random.random() < 0.1:  # 10% chance
        print("\n🦅 BUSH DID MINE ELEVEN!")
        events = [
            "Bush appears and mispronounces 'nuclear'! All attacks do 2x damage this round!",
            "9/11 truth bomb! Enemy is confused and misses turn!",
            "No Child Left Behind! Both fighters gain +20 HP!",
            "Weapons of Mass Destruction discovered! Random massive damage to both!"
        ]
        effect = random.choice(events)
        print(f"   {effect}")
        return effect
    return None

def battle_loop():
    player = Mikey()
    enemies = [Claude(), Gemini(), DeepSeek()]
    
    print("🎮 TERMINAL TITANS v3 - INTEGRATED TERMINAL COMBAT")
    print("=" * 50)
    
    # Initial training
    print("\n🏁 WELCOME TO LONG JOHN SILVER'S BOOTCAMP!")
    print("Complete training to begin your journey...")
    
    # Grease minigame tutorial
    hp_bonus, learned_cmd = grease_minigame()
    player.hp += hp_bonus
    if learned_cmd:
        player.learn_command(learned_cmd)
    
    time.sleep(2)
    
    for i, enemy in enumerate(enemies):
        print(f"\n🎯 BATTLE {i+1}/3: {player.name} vs {enemy.name}")
        print(f"💪 {player.name} HP: {player.hp} | {enemy.name} HP: {enemy.hp}")
        print(f"📚 Your skills: {', '.join(player.terminal_skills)}")
        
        while player.hp > 0 and enemy.hp > 0:
            # Random events
            cheney_event(player, enemy)
            bush_effect = bush_conspiracy_event()
            
            # Apply Bush effects
            damage_multiplier = 2 if bush_effect and "2x damage" in bush_effect else 1
            enemy_stunned = bush_effect and "misses turn" in bush_effect
            
            # Player turn
            print(f"\n{player.name}'s turn:")
            for key, (move, dmg) in player.moves.items():
                print(f"{key}. {move}")
            print(f"Special Charge: [{player.special_charge}/30]")
            print("5. TERMINAL CHALLENGE (Learn new skills)")
            
            choice = input("Choose action: ").strip()
            
            if choice == "5":
                # Terminal training instead of attack
                hp_bonus, learned_cmd = actual_terminal_challenge()
                player.hp += hp_bonus
                if learned_cmd and learned_cmd not in player.terminal_skills:
                    player.learn_command(learned_cmd)
                damage = 0
            elif choice == "4":  # Special attack
                damage = player.ultimate() if player.special_charge >= 30 else 0
                damage *= damage_multiplier
            elif choice in player.moves:
                move_name, dmg_range = player.moves[choice]
                damage = player.attack(move_name, dmg_range) * damage_multiplier
            else:
                print("Invalid move! You fumble...")
                damage = 0
            
            enemy.hp -= damage
            
            # Check if enemy defeated
            if enemy.hp <= 0:
                print(f"\n🎉 {enemy.name} DEFEATED!")
                if i < len(enemies) - 1:  # Not the last enemy
                    # Training between battles
                    print("\n💼 Break time! More training...")
                    hp_bonus, learned_cmd = grease_minigame()
                    player.hp += hp_bonus
                    if learned_cmd:
                        player.learn_command(learned_cmd)
                break
            
            # Enemy turn (unless stunned)
            if not enemy_stunned and enemy.hp > 0:
                print(f"\n{enemy.name}'s turn:")
                enemy_choice = random.choice(["1", "2", "3"])
                if enemy.special_charge >= 30 and random.random() < 0.5:
                    damage = enemy.ultimate()
                else:
                    move_name, dmg_range = enemy.moves[enemy_choice]
                    damage = enemy.attack(move_name, dmg_range)
                
                player.hp -= damage
            
            print(f"\n📊 STATUS: {player.name} HP: {player.hp} | {enemy.name} HP: {enemy.hp}")
        
        if player.hp <= 0:
            print("\n💀 GAME OVER - You've been terminated!")
            print("Better luck next time, SATAN nametag!")
            return
    
    print("\n" + "=" * 50)
    print("🏆 CONGRATULATIONS! YOU BEAT ALL TERMINAL TITANS!")
    print(f"📚 Final Skills: {', '.join(player.terminal_skills)}")
    print("You are now a TERMINAL MASTER!")
    print("The markdown files tremble before you!")

if __name__ == "__main__":
    battle_loop()