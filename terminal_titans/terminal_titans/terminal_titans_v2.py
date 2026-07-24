#!/usr/bin/env python3
# FILE: /storage/emulated/0/code_tool/terminal_titans_v2.py
import random
import os
import time

class Titan:
    def __init__(self, name, hp=100, style=""):
        self.name = name
        self.hp = hp
        self.style = style
        self.special_charge = 0
    
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
    
    def ultimate(self):
        print("👊 MIKEY'S BABYDICK PUNCH - MAXIMUM POWER!")
        return random.randint(40, 60)

class Claude(Titan):
    def __init__(self):
        super().__init__("CLAUDE", hp=100, style="TECHNICAL")
        self.moves = {
            "1": ("CODE SHURIKEN", (18, 28)),
            "2": ("DOCUMENTATION DROP", (15, 25)),
            "3": ("LOGIC BOMB", (25, 20)),
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

def terminal_training():
    """Mini-game: Learn actual terminal commands"""
    commands = {
        "list files": "ls",
        "change directory": "cd",
        "make directory": "mkdir", 
        "print working directory": "pwd",
        "copy file": "cp",
        "move file": "mv"
    }
    
    print("\n🎓 TERMINAL TRAINING - LONG JOHN SILVER'S BOOTCAMP")
    print("Grease-skimming simulation activated!")
    
    english_cmd = random.choice(list(commands.keys()))
    correct_answer = commands[english_cmd]
    
    print(f"\nCommand needed: {english_cmd}")
    user_guess = input("Enter the terminal command: ").strip()
    
    if user_guess == correct_answer:
        print("✅ Correct! You successfully skimmed the grease!")
        print("   +25 HP and +10 Special Charge!")
        return 25, 10
    else:
        print(f"❌ Wrong! Grease burn! Correct was: {correct_answer}")
        print("   -10 HP")
        return -10, 0

def cheney_event(player, enemy):
    """Random Cheney hunting accident"""
    if random.random() < 0.2:  # 20% chance
        print("\n🔫 CHENEY'S HUNTING ACCIDENT!")
        victim = random.choice([player, enemy])
        damage = random.randint(20, 40)
        print(f"   Dick Cheney 'accidentally' shoots {victim.name}!")
        print(f"   -{damage} HP to {victim.name}")
        victim.hp -= damage
        return True
    return False

def battle_loop():
    player = Mikey()
    enemies = [Claude(), Gemini(), DeepSeek()]
    
    for enemy in enemies:
        print(f"\n🎯 BATTLE: {player.name} vs {enemy.name}")
        print(f"💪 {player.name} HP: {player.hp} | {enemy.name} HP: {enemy.hp}")
        
        while player.hp > 0 and enemy.hp > 0:
            # Cheney random event
            cheney_event(player, enemy)
            
            # Player turn
            print(f"\n{player.name}'s turn:")
            for key, (move, dmg) in player.moves.items():
                print(f"{key}. {move}")
            print(f"Special Charge: [{player.special_charge}/30]")
            
            choice = input("Choose attack: ").strip()
            
            if choice == "4":  # Special attack
                damage = player.ultimate() if player.special_charge >= 30 else 0
            elif choice in player.moves:
                move_name, dmg_range = player.moves[choice]
                damage = player.attack(move_name, dmg_range)
            else:
                print("Invalid move! You fumble...")
                damage = 0
            
            enemy.hp -= damage
            
            # Check if enemy defeated
            if enemy.hp <= 0:
                print(f"\n🎉 {enemy.name} DEFEATED!")
                # Terminal training between battles
                hp_bonus, special_bonus = terminal_training()
                player.hp += hp_bonus
                player.special_charge += special_bonus
                break
            
            # Enemy turn
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
            return
    
    print("\n🏆 CONGRATULATIONS! YOU BEAT ALL TERMINAL TITANS!")
    print("You are now a TERMINAL MASTER!")

if __name__ == "__main__":
    print("🎮 TERMINAL TITANS v2 - EXPANDED COMBAT")
    print("Mikey vs The AI Alliance")
    battle_loop()