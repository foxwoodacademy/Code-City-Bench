// Veritas: The Accountability Engine - Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const scenarioInput = document.getElementById('scenarioInput');
    const analyzeButton = document.getElementById('analyzeButton');
    const resultContainer = document.getElementById('resultsSection');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const modeButtons = document.querySelectorAll('.mode-button');
    const documentUrlInput = document.getElementById('documentUrl');
    const followUpInput = document.getElementById('follow-up-input');
    const followUpButton = document.getElementById('follow-up-button');
    const bloodhoundButton = document.getElementById('bloodhound-button');
    const executionButton = document.getElementById('executionButton');
    
    // Audio elements
    const clickSound = document.getElementById('click-sound');
    const typewriterSound = document.getElementById('typewriter-sound');
    const alarmSound = document.getElementById('alarm-sound');
    
    // Current state
    let currentMode = 'analysis'; // Default mode
    let isAnalyzing = false;
    
    // Initialize Tone.js
    let synth;
    
    // Initialize charts
    let corruptionChart;
    let fearIndexChart;
    
    // Initialize Tone.js when user interacts with the page
    document.body.addEventListener('click', function() {
        if (!synth) {
            initializeTone();
        }
    }, { once: true });
    
    // Set up event listeners
    modeButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            modeButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Update current mode
            currentMode = this.dataset.mode;
            
            // Play click sound
            playSound(clickSound);
            
            // Show/hide document URL input for audit mode
            if (currentMode === 'audit') {
                document.querySelector('.document-url-container').classList.remove('hidden');
            } else {
                document.querySelector('.document-url-container').classList.add('hidden');
            }
        });
    });
    
    // Analyze button click handler
    analyzeButton.addEventListener('click', function() {
        if (isAnalyzing) return; // Prevent multiple submissions
        
        const scenario = scenarioInput.value.trim();
        if (!scenario) {
            showError('Please enter a scenario to analyze.');
            return;
        }
        
        // Start analysis
        analyzeScenario(scenario);
    });
    
    // Follow-up button click handler
    followUpButton.addEventListener('click', function() {
        const followUpQuestion = followUpInput.value.trim();
        if (!followUpQuestion) {
            showError('Please enter a follow-up question.');
            return;
        }
        
        // Get the original scenario
        const scenario = scenarioInput.value.trim();
        if (!scenario) {
            showError('Original scenario is missing.');
            return;
        }
        
        // Send follow-up request
        analyzeScenario(scenario, followUpQuestion);
    });
    
    // Bloodhound button click handler
    bloodhoundButton.addEventListener('click', function() {
        const scenario = scenarioInput.value.trim();
        if (!scenario) {
            showError('Please enter a scenario first.');
            return;
        }
        
        // Set mode to bloodhound questions
        currentMode = 'bloodhound_questions';
        
        // Start analysis in bloodhound mode
        analyzeScenario(scenario);
    });
    
    // Execution button click handler
    executionButton.addEventListener('click', function() {
        // Play alarm sound
        playSound(alarmSound);
        
        // Add visual effects
        document.body.classList.add('execution-mode');
        setTimeout(() => {
            document.body.classList.remove('execution-mode');
        }, 3000);
        
        // Set mode to perp walk
        currentMode = 'perpWalk';
        
        // Send perp walk request
        analyzeScenario('execution');
    });
    
    // Function to analyze scenario
    function analyzeScenario(scenario, followUpQuestion = '') {
        isAnalyzing = true;
        
        // Show loading indicator
        loadingIndicator.classList.remove('hidden');
        resultContainer.innerHTML = '';
        
        // Play typewriter sound
        playSound(typewriterSound);
        
        // Prepare request data
        const requestData = {
            scenario: scenario,
            mode: currentMode,
            followUpQuestion: followUpQuestion,
            documentUrl: documentUrlInput ? documentUrlInput.value.trim() : ''
        };
        
        // Send request to backend
        fetch('/analyze_scenario', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Hide loading indicator
            loadingIndicator.classList.add('hidden');
            
            // Display results
            displayResults(data);
            
            // Reset analyzing state
            isAnalyzing = false;
        })
        .catch(error => {
            console.error('Error:', error);
            showError('An error occurred while analyzing the scenario. Please try again.');
            
            // Hide loading indicator
            loadingIndicator.classList.add('hidden');
            
            // Reset analyzing state
            isAnalyzing = false;
        });
    }
    
    // Function to display results
    function displayResults(data) {
        // Handle error
        if (data.error) {
            showError(data.error);
            return;
        }
        
        // Show results section
        resultContainer.classList.remove('hidden');
        
        // Update AI response
        if (data.aiResponse) {
            const aiResponseDiv = document.getElementById('aiResponse');
            if (aiResponseDiv) {
                aiResponseDiv.innerHTML = formatResponse(data.aiResponse);
            }
        }
        
        // Update Aura insights
        if (data.auraInsights) {
            const auraSection = document.getElementById('auraInsightsSection');
            const auraDiv = document.getElementById('auraInsights');
            if (auraSection && auraDiv) {
                auraSection.classList.remove('hidden');
                auraDiv.innerHTML = formatResponse(data.auraInsights);
            }
        }
        
        // Update FOIA output
        if (data.foiaOutput) {
            const foiaSection = document.getElementById('foiaOutputSection');
            const foiaDiv = document.getElementById('foiaOutput');
            if (foiaSection && foiaDiv) {
                foiaSection.classList.remove('hidden');
                foiaDiv.innerHTML = formatResponse(data.foiaOutput);
            }
        }
    }
    
    // Function to format response text
    function formatResponse(text) {
        return text.replace(/\n/g, '<br>');
    }
    
    // Function to show error
    function showError(message) {
        const errorDiv = document.getElementById('errorMessage');
        if (errorDiv) {
            errorDiv.querySelector('.error-text').textContent = message;
            errorDiv.classList.remove('hidden');
            setTimeout(() => {
                errorDiv.classList.add('hidden');
            }, 5000);
        } else {
            alert(message);
        }
        }

    
    // Function to play sound
    function playSound(audioElement) {
        if (audioElement) {
            audioElement.currentTime = 0;
            audioElement.play().catch(e => console.log('Audio play error:', e));
        }
    }
    
    // Function to initialize Tone.js
    function initializeTone() {
        // Start Tone.js
        Tone.start();
        
        // Create a synth
        synth = new Tone.PolySynth(Tone.Synth).toDestination();
        synth.volume.value = -10; // Set volume
    }
    
    // Function to play tone sequence based on mode
    function playToneSequence(mode) {
        if (!synth) return;
        
        // Define sequences for different modes
        const sequences = {
            'analysis': ['C4', 'E4', 'G4', 'C5'],
            'audit': ['D4', 'F4', 'A4', 'D5', 'F5'],
            'psychoWarfare': ['E3', 'B3', 'E4', 'G#4', 'B4'],
            'perpWalk': ['G3', 'C4', 'D#4', 'G4', 'C5', 'D#5'],
            'bloodhound_questions': ['F#3', 'A3', 'C#4', 'F#4']
        };
        
        // Get sequence for current mode or use default
        const sequence = sequences[mode] || sequences.analysis;
        
        // Play sequence
        const now = Tone.now();
        sequence.forEach((note, i) => {
            synth.triggerAttackRelease(note, '8n', now + i * 0.15);
        });
    }
    
    // Function to create corruption probability matrix chart
    function createCorruptionChart(response) {
        // Try to extract corruption probability matrix values
        const matrixMatch = response.match(/\[\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\]/);
        
        if (!matrixMatch) return;
        
        // Extract values
        const values = matrixMatch.slice(1, 6).map(Number);
        
        // Create or update chart
        const chartCanvas = document.getElementById('corruption-chart');
        if (!chartCanvas) return;
        
        if (corruptionChart) {
            corruptionChart.destroy();
        }
        
        corruptionChart = new Chart(chartCanvas, {
            type: 'radar',
            data: {
                labels: ['Financial Irregularity', 'Procedural Violation', 'Conflict of Interest', 'Transparency Issue', 'Authority Abuse'],
                datasets: [{
                    label: 'Corruption Probability Matrix',
                    data: values,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(255, 99, 132, 1)',
                    pointRadius: 5
                }]
            },
            options: {
                scales: {
                    r: {
                        angleLines: {
                            display: true
                        },
                        suggestedMin: 0,
                        suggestedMax: 10
                    }
                }
            }
        });
    }
    
    // Function to create fear index chart
    function createFearIndexChart(response) {
        // Try to extract fear index value
        const fearMatch = response.match(/Fear Index[^\d]+(\d+)/);
        
        if (!fearMatch) return;
        
        // Extract value
        const fearValue = parseInt(fearMatch[1]);
        
        // Create or update chart
        const chartCanvas = document.getElementById('fear-index-chart');
        if (!chartCanvas) return;
        
        if (fearIndexChart) {
            fearIndexChart.destroy();
        }
        
        fearIndexChart = new Chart(chartCanvas, {
            type: 'gauge',
            data: {
                datasets: [{
                    value: fearValue,
                    minValue: 0,
                    maxValue: 100,
                    backgroundColor: function(context) {
                        const value = context.dataset.value;
                        const alpha = (value / 100) * 0.8 + 0.2;
                        return `rgba(255, ${200 - value * 2}, 0, ${alpha})`;
                    }
                }]
            },
            options: {
                needle: {
                    radiusPercentage: 2,
                    widthPercentage: 3.2,
                    lengthPercentage: 80,
                    color: 'rgba(0, 0, 0, 1)'
                },
                valueLabel: {
                    display: true,
                    formatter: function(value) {
                        return value + '/100';
                    },
                    color: 'rgba(255, 255, 255, 1)',
                    backgroundColor: 'rgba(0, 0, 0, 0.3)',
                    borderRadius: 5,
                    padding: {
                        top: 10,
                        bottom: 10
                    }
                }
            }
        });
    }
});