# Coach Bleak: The Accountability Engine

## Overview

Coach Bleak is an advanced AI-powered accountability engine designed to analyze scenarios, audit financial situations, and provide psychological insights. The application leverages multiple AI models and specialized micro-agents to deliver comprehensive analysis and actionable intelligence.

## Features

### Analysis Mode
- Detailed scenario analysis with AI-powered insights
- Bloodhound follow-up questions for deeper investigation
- Entity extraction and red flag detection

### Audit Mode
- Financial situation and transaction analysis
- Corruption probability matrix visualization
- Fear index measurement
- Procedural violations and ethical breaches detection

### Psychological Mode
- Psychological profiling and vulnerability assessment
- Strategic recommendations for psychological engagement
- Target exposure and execution simulation

### Perp Walk Mode
- Simulated accountability scenarios
- Dramatic visualization of consequences

### Document Processing
- URL-based document ingestion
- Entity parsing and relationship mapping
- Red flag analysis of document content

### FOIA Generator
- Automated Freedom of Information Act request generation
- Agency-specific template customization
- Appeal letter generation based on denial patterns

### Aura Insights
- Pattern recognition in complex scenarios
- Entity connection analysis
- Timeline and risk assessment
- Psychological profiling

## Technical Architecture

### Backend
- Flask web application framework
- Integration with Google's Gemini API
- Modular architecture with specialized micro-agents:
  - Document Ingestion Pipeline
  - Entity Parsing and Red Flag Analyzer
  - FOIA Generator Micro-Agent
  - Aura Micro-Agent

### Frontend
- Modern, responsive UI with Tailwind CSS
- Interactive visualizations with Chart.js
- Audio feedback with Tone.js
- Dynamic content rendering

## Getting Started

### Prerequisites
- Python 3.8+
- Flask
- Google API key for Gemini

### Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```
   export GEMINI_API_KEY=your_api_key_here
   ```
   (Use `set` instead of `export` on Windows)

4. Run the application:
   ```
   python app.py
   ```

5. Access the application at `http://localhost:5000`

## Usage

1. Select an operation mode (Analysis, Audit, Psychological, or Perp Walk)
2. Enter a scenario description or paste document text
3. Optionally provide a document URL for analysis
4. Click "Analyze with Coach Bleak"
5. Review the AI-generated analysis, insights, and visualizations
6. For Analysis mode, use the Bloodhound follow-up questions for deeper investigation
7. For Psychological mode, use the EXECUTE button to simulate target exposure

## Project Structure

```
├── app.py                 # Main Flask application
├── modules/
│   ├── document_ingestion.py    # Document processing pipeline
│   ├── entity_analyzer.py       # Entity extraction and red flag detection
│   ├── foia_generator.py        # FOIA request generation
│   └── aura_agent.py            # Aura insights generation
├── static/
│   ├── css/
│   │   └── styles.css           # Application styling
│   └── js/
│       └── main.js              # Frontend functionality
└── templates/
    └── index.html               # Main application template
```

## License

This project is proprietary software.

## Disclaimer

Coach Bleak is designed for educational and informational purposes only. The application should not be used for illegal activities or to harm individuals or organizations. The developers are not responsible for any misuse of this software.