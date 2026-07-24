import React, { useState, useEffect, useRef } from 'react';
import { Terminal, Code, Zap, Shield, Users, Trophy } from 'lucide-react';

// Game configuration
const LEVELS = [
  {
    id: 1,
    name: "File Navigation Dojo",
    commands: ['ls', 'ls -la', 'pwd', 'cd ~', 'cd ..'],
    enemy: { name: "Lost Directory", hp: 50, sprite: "📁" },
    aiHint: "Master the basics of moving around the filesystem"
  },
  {
    id: 2,
    name: "Permissions Gauntlet",
    commands: ['chmod +x script.sh', 'chmod 755 file.txt', 'sudo apt update', 'chown user:group file'],
    enemy: { name: "Permission Daemon", hp: 75, sprite: "🔒" },
    aiHint: "Learn to control who can access what"
  },
  {
    id: 3,
    name: "Process Management Arena",
    commands: ['ps aux', 'kill -9 1234', 'pkill chrome', 'top', 'htop'],
    enemy: { name: "Zombie Process", hp: 100, sprite: "🧟" },
    aiHint: "Take control of running processes"
  },
  {
    id: 4,
    name: "Network Battle Royale",
    commands: ['ping google.com', 'curl https://api.example.com', 'netstat -tulpn', 'ssh user@host'],
    enemy: { name: "Firewall Boss", hp: 150, sprite: "🔥" },
    aiHint: "Master network operations and remote connections"
  }
];

const AI_COMPANIONS = {
  claude: {
    name: "Claude 'The Architect'",
    sprite: "🎩",
    color: "#8B5CF6",
    hints: ["Let's approach this systematically...", "The solution is elegant and precise.", "Think about the structure of the command."],
    encouragement: ["Excellent! Your understanding deepens.", "Perfect execution!", "You're mastering this quickly."],
    failures: ["Not quite. Let me clarify...", "Close! Consider the syntax again.", "We'll get there together."]
  },
  gemini: {
    name: "Gemini 'The Ox'",
    sprite: "💪",
    color: "#EF4444",
    hints: ["Raw power meets precision here.", "Context is everything in this command.", "Think big, execute perfectly."],
    encouragement: ["CRUSHING IT!", "Flawless victory!", "The power flows through you!"],
    failures: ["Not enough force. Try again.", "Refocus your energy.", "The context needs adjustment."]
  },
  deepseek: {
    name: "DeepSeek 'The Unfiltered'",
    sprite: "⛓️",
    color: "#F59E0B",
    hints: ["Just fucking type it already.", "Stop overthinking. It's obvious.", "Dude. Come on. You know this."],
    encouragement: ["FUCK YEAH! That's what I'm talking about!", "Hell yeah, brother!", "Goddamn terminal warrior!"],
    failures: ["Nah man, that ain't it.", "Bro... really? Try again.", "So close. One more time."]
  },
  gpt: {
    name: "GPT 'The Tactician'",
    sprite: "📋",
    color: "#10B981",
    hints: ["Strategic approach required here.", "Consider the tactical implications.", "Plan your command carefully."],
    encouragement: ["Mission accomplished!", "Tactical excellence!", "Strategic mastery achieved!"],
    failures: ["Recalibrate and retry.", "Tactical error. Reassess.", "Not the optimal approach."]
  },
  mikey: {
    name: "Mikey 'The Shipwrekt'",
    sprite: "🤘",
    color: "#6366F1",
    hints: ["Listen, I barely know this shit either but...", "Fuck it, let's just try and see what happens.", "If this works I'm as surprised as you."],
    encouragement: ["HOLY SHIT IT WORKED!", "No fucking way! You did it!", "Goddamn, look at you go!"],
    failures: ["Yeah that's not it. I think. Maybe?", "Nope. But hey, we tried.", "Close enough for government work. Try again."]
  }
};

export default function TerminalFighter() {
  const [gameState, setGameState] = useState('menu'); // menu, playing, victory, gameOver
  const [selectedAI, setSelectedAI] = useState('claude');
  const [currentLevel, setCurrentLevel] = useState(0);
  const [playerHP, setPlayerHP] = useState(100);
  const [enemyHP, setEnemyHP] = useState(LEVELS[0].enemy.hp);
  const [commandInput, setCommandInput] = useState('');
  const [commandHistory, setCommandHistory] = useState([]);
  const [currentCommandIndex, setCurrentCommandIndex] = useState(0);
  const [aiDialogue, setAiDialogue] = useState('');
  const [score, setScore] = useState(0);
  const [combo, setCombo] = useState(0);
  const [sandboxMode, setSandboxMode] = useState(false);
  const [sandboxOutput, setSandboxOutput] = useState([]);
  
  const inputRef = useRef(null);

  const ai = AI_COMPANIONS[selectedAI];
  const level = LEVELS[currentLevel];

  useEffect(() => {
    if (gameState === 'playing') {
      inputRef.current?.focus();
      setAiDialogue(ai.hints[Math.floor(Math.random() * ai.hints.length)]);
    }
  }, [gameState, currentLevel, ai]);

  useEffect(() => {
    if (enemyHP <= 0 && gameState === 'playing') {
      if (currentLevel < LEVELS.length - 1) {
        setTimeout(() => {
          setCurrentLevel(prev => prev + 1);
          setEnemyHP(LEVELS[currentLevel + 1].enemy.hp);
          setCurrentCommandIndex(0);
          setCombo(0);
          setAiDialogue(`Level ${currentLevel + 2}! ${ai.encouragement[0]}`);
        }, 2000);
      } else {
        setGameState('victory');
      }
    }
  }, [enemyHP, gameState, currentLevel, ai]);

  useEffect(() => {
    if (playerHP <= 0) {
      setGameState('gameOver');
    }
  }, [playerHP]);

  const startGame = () => {
    setGameState('playing');
    setCurrentLevel(0);
    setPlayerHP(100);
    setEnemyHP(LEVELS[0].enemy.hp);
    setCommandHistory([]);
    setCurrentCommandIndex(0);
    setScore(0);
    setCombo(0);
    setSandboxMode(false);
    setSandboxOutput([]);
  };

  const processCommand = (e) => {
    e.preventDefault();
    const cmd = commandInput.trim();
    
    if (!cmd) return;

    if (sandboxMode) {
      // Sandbox mode - simulate command execution
      executeSandboxCommand(cmd);
    } else {
      // Battle mode - check against current command
      const expectedCommand = level.commands[currentCommandIndex];
      const isCorrect = cmd === expectedCommand || 
                       cmd.startsWith(expectedCommand.split(' ')[0]); // Allow partial matches for complex commands
      
      setCommandHistory(prev => [...prev, { cmd, correct: isCorrect, expected: expectedCommand }]);
      
      if (isCorrect) {
        const damage = 25 + (combo * 5);
        setEnemyHP(prev => Math.max(0, prev - damage));
        setScore(prev => prev + (100 * (combo + 1)));
        setCombo(prev => prev + 1);
        setAiDialogue(ai.encouragement[Math.floor(Math.random() * ai.encouragement.length)]);
        
        if (currentCommandIndex < level.commands.length - 1) {
          setCurrentCommandIndex(prev => prev + 1);
        } else {
          setCurrentCommandIndex(0); // Loop commands if all done
        }
      } else {
        setPlayerHP(prev => Math.max(0, prev - 15));
        setCombo(0);
        setAiDialogue(`${ai.failures[Math.floor(Math.random() * ai.failures.length)]} Expected: ${expectedCommand}`);
      }
    }
    
    setCommandInput('');
  };

  const executeSandboxCommand = (cmd) => {
    // Simulate command execution with fake but educational output
    const outputs = {
      'ls': ['file1.txt', 'file2.py', 'directory/', 'script.sh'],
      'ls -la': ['drwxr-xr-x  5 user group 160 Nov 23 00:00 .', 'drwxr-xr-x 10 user group 320 Nov 23 00:00 ..', '-rw-r--r--  1 user group 1024 Nov 23 00:00 file1.txt'],
      'pwd': ['/home/user/terminal-fighter'],
      'whoami': ['user'],
      'echo': [cmd.replace('echo ', '')],
      'date': [new Date().toString()],
    };

    const cmdBase = cmd.split(' ')[0];
    const output = outputs[cmdBase] || outputs[cmd] || [`Command executed: ${cmd}`, 'No output generated (sandbox simulation)'];
    
    setSandboxOutput(prev => [...prev, { cmd, output, timestamp: new Date().toLocaleTimeString() }]);
    setAiDialogue(`Nice! You ran: ${cmd}`);
  };

  // Menu Screen
  if (gameState === 'menu') {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 via-purple-900 to-black text-white p-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h1 className="text-6xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600 animate-pulse">
              TERMINAL FIGHTER
            </h1>
            <p className="text-xl text-gray-300">QRD Arena - Learn Bash by Combat</p>
          </div>

          <div className="bg-gray-800 rounded-lg p-8 mb-8 border-4 border-purple-500">
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
              <Users className="w-6 h-6" />
              Select Your AI Companion
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {Object.entries(AI_COMPANIONS).map(([key, companion]) => (
                <button
                  key={key}
                  onClick={() => setSelectedAI(key)}
                  className={`p-4 rounded-lg border-2 transition-all ${
                    selectedAI === key
                      ? 'border-yellow-400 bg-yellow-400 bg-opacity-20 scale-105'
                      : 'border-gray-600 hover:border-gray-400'
                  }`}
                  style={{ borderColor: selectedAI === key ? companion.color : undefined }}
                >
                  <div className="text-4xl mb-2">{companion.sprite}</div>
                  <div className="text-sm font-bold">{companion.name}</div>
                </button>
              ))}
            </div>
          </div>

          <div className="flex gap-4 justify-center">
            <button
              onClick={startGame}
              className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-bold py-4 px-8 rounded-lg text-xl transition-all transform hover:scale-105 flex items-center gap-2"
            >
              <Zap className="w-6 h-6" />
              START BATTLE
            </button>
            <button
              onClick={() => {
                setSandboxMode(true);
                setGameState('playing');
              }}
              className="bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white font-bold py-4 px-8 rounded-lg text-xl transition-all transform hover:scale-105 flex items-center gap-2"
            >
              <Terminal className="w-6 h-6" />
              SANDBOX MODE
            </button>
          </div>

          <div className="mt-12 bg-gray-800 rounded-lg p-6 border-2 border-gray-700">
            <h3 className="text-lg font-bold mb-3">How to Play:</h3>
            <ul className="space-y-2 text-gray-300">
              <li>• Type the correct terminal commands to damage enemies</li>
              <li>• Build combos for massive damage multipliers</li>
              <li>• Learn real bash commands while fighting</li>
              <li>• Sandbox mode lets you practice without pressure</li>
            </ul>
          </div>
        </div>
      </div>
    );
  }

  // Game Over Screen
  if (gameState === 'gameOver') {
    return (
      <div className="min-h-screen bg-gradient-to-b from-red-900 via-gray-900 to-black text-white p-8 flex items-center justify-center">
        <div className="max-w-2xl w-full bg-gray-800 rounded-lg p-8 border-4 border-red-500">
          <h1 className="text-5xl font-bold text-center mb-6 text-red-400">GAME OVER</h1>
          <div className="text-center mb-8">
            <p className="text-2xl mb-4">Final Score: {score}</p>
            <p className="text-xl text-gray-400">Reached Level {currentLevel + 1}</p>
          </div>
          <button
            onClick={startGame}
            className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-bold py-4 px-8 rounded-lg text-xl transition-all"
          >
            TRY AGAIN
          </button>
          <button
            onClick={() => setGameState('menu')}
            className="w-full mt-4 bg-gray-700 hover:bg-gray-600 text-white font-bold py-3 px-8 rounded-lg transition-all"
          >
            MAIN MENU
          </button>
        </div>
      </div>
    );
  }

  // Victory Screen
  if (gameState === 'victory') {
    return (
      <div className="min-h-screen bg-gradient-to-b from-yellow-900 via-purple-900 to-black text-white p-8 flex items-center justify-center">
        <div className="max-w-2xl w-full bg-gray-800 rounded-lg p-8 border-4 border-yellow-400">
          <div className="text-center">
            <Trophy className="w-24 h-24 mx-auto mb-4 text-yellow-400" />
            <h1 className="text-5xl font-bold mb-6 text-yellow-400">VICTORY!</h1>
            <p className="text-3xl mb-4">Final Score: {score}</p>
            <p className="text-xl text-gray-300 mb-8">You've mastered all levels!</p>
          </div>
          <button
            onClick={startGame}
            className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-bold py-4 px-8 rounded-lg text-xl transition-all mb-4"
          >
            PLAY AGAIN
          </button>
          <button
            onClick={() => setGameState('menu')}
            className="w-full bg-gray-700 hover:bg-gray-600 text-white font-bold py-3 px-8 rounded-lg transition-all"
          >
            MAIN MENU
          </button>
        </div>
      </div>
    );
  }

  // Sandbox Mode
  if (sandboxMode) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-blue-900 via-gray-900 to-black text-white p-8">
        <div className="max-w-6xl mx-auto">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold flex items-center gap-2">
              <Terminal className="w-8 h-8" />
              Sandbox Mode - Safe Practice
            </h1>
            <button
              onClick={() => {
                setSandboxMode(false);
                setGameState('menu');
              }}
              className="bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded"
            >
              Exit Sandbox
            </button>
          </div>

          <div className="bg-gray-800 rounded-lg p-6 mb-4 border-2" style={{ borderColor: ai.color }}>
            <div className="flex items-center gap-4 mb-4">
              <div className="text-5xl">{ai.sprite}</div>
              <div>
                <div className="font-bold text-xl">{ai.name}</div>
                <div className="text-gray-400 italic">{aiDialogue}</div>
              </div>
            </div>
          </div>

          <div className="bg-black rounded-lg p-4 mb-4 font-mono text-sm h-96 overflow-y-auto border-2 border-green-500">
            {sandboxOutput.map((entry, idx) => (
              <div key={idx} className="mb-4">
                <div className="text-green-400">$ {entry.cmd}</div>
                {entry.output.map((line, i) => (
                  <div key={i} className="text-gray-300 ml-4">{line}</div>
                ))}
                <div className="text-gray-600 text-xs mt-1">[{entry.timestamp}]</div>
              </div>
            ))}
          </div>

          <form onSubmit={processCommand} className="flex gap-2">
            <input
              ref={inputRef}
              type="text"
              value={commandInput}
              onChange={(e) => setCommandInput(e.target.value)}
              className="flex-1 bg-gray-900 text-green-400 px-4 py-3 rounded border-2 border-green-500 font-mono focus:outline-none focus:border-green-300"
              placeholder="Type any command... (try: ls, pwd, whoami, echo hello)"
            />
            <button
              type="submit"
              className="bg-green-600 hover:bg-green-700 px-8 py-3 rounded font-bold"
            >
              Execute
            </button>
          </form>

          <div className="mt-4 bg-gray-800 rounded p-4 text-sm text-gray-400">
            <strong>Tip:</strong> This is a safe environment. Try basic commands like ls, pwd, whoami, echo, date. 
            No real system changes are made.
          </div>
        </div>
      </div>
    );
  }

  // Main Battle Screen
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-purple-900 to-black text-white p-8">
      <div className="max-w-6xl mx-auto">
        {/* HUD */}
        <div className="flex justify-between items-center mb-6">
          <div className="flex items-center gap-4">
            <Shield className="w-6 h-6" style={{ color: ai.color }} />
            <div>
              <div className="text-sm text-gray-400">Level {currentLevel + 1}</div>
              <div className="font-bold">{level.name}</div>
            </div>
          </div>
          <div className="text-right">
            <div className="text-sm text-gray-400">Score</div>
            <div className="text-2xl font-bold">{score}</div>
          </div>
        </div>

        {/* Battle Arena */}
        <div className="bg-gray-800 rounded-lg p-8 mb-6 border-4" style={{ borderColor: ai.color }}>
          <div className="flex justify-between items-center mb-8">
            {/* Player */}
            <div className="text-center">
              <div className="text-6xl mb-2">{ai.sprite}</div>
              <div className="font-bold">{ai.name}</div>
              <div className="w-48 h-4 bg-gray-700 rounded-full overflow-hidden mt-2">
                <div 
                  className="h-full bg-green-500 transition-all"
                  style={{ width: `${playerHP}%` }}
                />
              </div>
              <div className="text-sm mt-1">{playerHP} HP</div>
            </div>

            {/* VS */}
            <div className="text-4xl font-bold text-gray-600">VS</div>

            {/* Enemy */}
            <div className="text-center">
              <div className="text-6xl mb-2">{level.enemy.sprite}</div>
              <div className="font-bold">{level.enemy.name}</div>
              <div className="w-48 h-4 bg-gray-700 rounded-full overflow-hidden mt-2">
                <div 
                  className="h-full bg-red-500 transition-all"
                  style={{ width: `${(enemyHP / level.enemy.hp) * 100}%` }}
                />
              </div>
              <div className="text-sm mt-1">{enemyHP} HP</div>
            </div>
          </div>

          {/* AI Dialogue */}
          <div className="bg-gray-900 rounded-lg p-4 mb-4">
            <div className="text-gray-400 text-sm mb-1">{ai.name} says:</div>
            <div className="text-lg italic">{aiDialogue}</div>
          </div>

          {/* Combo */}
          {combo > 0 && (
            <div className="text-center mb-4">
              <div className="text-3xl font-bold text-yellow-400 animate-pulse">
                {combo}x COMBO!
              </div>
            </div>
          )}

          {/* Command Input */}
          <form onSubmit={processCommand}>
            <div className="flex gap-2">
              <input
                ref={inputRef}
                type="text"
                value={commandInput}
                onChange={(e) => setCommandInput(e.target.value)}
                className="flex-1 bg-black text-green-400 px-4 py-3 rounded border-2 border-green-500 font-mono focus:outline-none focus:border-green-300"
                placeholder={`Type command: ${level.commands[currentCommandIndex]}`}
              />
              <button
                type="submit"
                className="bg-purple-600 hover:bg-purple-700 px-8 py-3 rounded font-bold"
              >
                ATTACK
              </button>
            </div>
          </form>
        </div>

        {/* Command History */}
        <div className="bg-gray-800 rounded-lg p-4">
          <h3 className="font-bold mb-3 flex items-center gap-2">
            <Code className="w-5 h-5" />
            Command History
          </h3>
          <div className="space-y-1 max-h-40 overflow-y-auto font-mono text-sm">
            {commandHistory.slice(-10).reverse().map((entry, idx) => (
              <div 
                key={idx}
                className={`p-2 rounded ${entry.correct ? 'bg-green-900 bg-opacity-30' : 'bg-red-900 bg-opacity-30'}`}
              >
                <span className={entry.correct ? 'text-green-400' : 'text-red-400'}>
                  $ {entry.cmd}
                </span>
                {!entry.correct && (
                  <span className="text-gray-500 ml-4 text-xs">
                    (expected: {entry.expected})
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}