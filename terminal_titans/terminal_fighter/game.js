// FILE: terminal_fighter/game.js
// TERMINAL FIGHTER - Core Game Loop

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const commandInput = document.getElementById('commandInput');

// Game State
let gameState = {
    level: 1,
    player: {
        character: 'claude',
        hp: 100,
        x: 100,
        y: 400
    },
    enemy: {
        type: 'corrupted_terminal',
        hp: 50,
        x: 600,
        y: 400
    },
    currentCommand: 'ls -la',
    commandHistory: [],
    aiDialogue: "Type 'ls -la' to reveal hidden files!"
};

// Character Sprites (8-bit style)
const characters = {
    claude: {
        idle: '🎩', // Placeholder - would be actual sprite
        attack: '📜',
        hurt: '😵',
        victory: '✨'
    },
    gemini: {
        idle: '💪',
        attack: '🔥',
        hurt: '😤',
        victory: '🏆'
    },
    deepseek: {
        idle: '⛓️',
        attack: '🔞',
        hurt: '😈',
        victory: '🖕'
    }
};

// Main Game Loop
function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw player
    ctx.font = '48px Arial';
    ctx.fillText(characters[gameState.player.character].idle, 
                 gameState.player.x, gameState.player.y);
    
    // Draw enemy
    ctx.fillText('💀', gameState.enemy.x, gameState.enemy.y);
    
    // Draw HP bars
    ctx.fillStyle = '#0f0';
    ctx.fillRect(50, 50, gameState.player.hp * 2, 20);
    ctx.fillStyle = '#f00';
    ctx.fillRect(550, 50, gameState.enemy.hp * 2, 20);
    
    // Draw AI dialogue
    ctx.fillStyle = '#fff';
    ctx.font = '16px Courier';
    ctx.fillText(gameState.aiDialogue, 50, 150);
    
    requestAnimationFrame(gameLoop);
}

// Command Input Handler
commandInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        const command = commandInput.value.trim();
        processCommand(command);
        commandInput.value = '';
    }
});

function processCommand(command) {
    if (command === gameState.currentCommand) {
        // SUCCESS
        gameState.enemy.hp -= 25;
        gameState.aiDialogue = "NICE! Keep going!";
        
        // Trigger attack animation
        gameState.player.character = characters[gameState.player.character].attack;
        setTimeout(() => {
            gameState.player.character = characters[gameState.player.character].idle;
        }, 500);
        
        if (gameState.enemy.hp <= 0) {
            victory();
        } else {
            nextCommand();
        }
    } else {
        // FAILURE
        gameState.player.hp -= 10;
        gameState.aiDialogue = `Oops! Try '${gameState.currentCommand}'`;
    }
    
    gameState.commandHistory.push(command);
}

function nextCommand() {
    const commands = ['pwd', 'cd ~', 'mkdir test', 'touch file.txt'];
    gameState.currentCommand = commands[Math.floor(Math.random() * commands.length)];
    gameState.aiDialogue = `Now try: ${gameState.currentCommand}`;
}

function victory() {
    gameState.aiDialogue = "LEVEL COMPLETE! 🎉";
    gameState.level++;
    // Load next level...
}

// Start game
gameLoop();