# Voice Cloner

![Voice Cloner Logo](https://img.shields.io/badge/Voice%20Cloner-Local%20AI-blue.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**Local, Free, Open-Source Voice Cloning Tool**

Clone voices from audio and video samples entirely on your own machine. No cloud dependencies, no usage limits, no paid APIs.

---

## ✨ Features

| Feature | Status | Technology |
|---------|--------|------------|
| Audio Extraction from Video | ✅ Complete | FFmpeg |
| Voice Isolation | ✅ Complete | Demucs (Facebook Research) |
| Voice Cloning | ✅ Complete | RVC (Retrieval-based Voice Conversion) |
| Batch Processing | ✅ Complete | Custom Pipeline |
| GPU Acceleration | ✅ Supported | PyTorch CUDA |
| Local Execution | ✅ Complete | 100% Offline |

---

## 🚀 Quick Start

### One-Command Setup

```bash
git clone https://github.com/your-username/voice-cloner.git
cd voice-cloner
chmod +x setup.sh
./setup.sh
```

### Clone a Voice

```bash
# From an audio file
python src/voice_cloner.py --input samples/my_voice.wav --output clones/my_clone

# From a video file  
python src/voice_cloner.py --input samples/my_video.mp4 --output clones/my_clone

# Process a directory
python src/voice_cloner.py --input samples/ --output clones/
```

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Pipeline](#-pipeline)
- [Configuration](#-configuration)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---

## 📦 Installation

### Prerequisites

| Platform | Requirements |
|----------|--------------|
| **Termux (Android)** | `pkg install python git ffmpeg` |
| **Linux (Debian/Ubuntu)** | `sudo apt install python3 python3-pip git ffmpeg` |
| **macOS** | `brew install python git ffmpeg` |
| **Windows (WSL2)** | Same as Linux |

### Python Dependencies

```bash
pip install -r requirements.txt
```

### Automatic Setup

Run the setup script for your platform:

```bash
chmod +x setup.sh
./setup.sh
```

This will:
1. Install system dependencies
2. Clone Demucs for voice isolation
3. Clone RVC for voice cloning
4. Install all Python packages

---

## 🎯 Usage

### Command Line Interface

```bash
python src/voice_cloner.py [OPTIONS]
```

#### Required Arguments

| Flag | Description |
|------|-------------|
| `--input, -i TEXT` | Input file or directory (audio/video) |

#### Optional Arguments

| Flag | Default | Description |
|------|---------|-------------|
| `--output, -o TEXT` | `outputs/<input>` | Output directory |
| `--method, -m TEXT` | `rvc` | Method: `rvc` or `simple` |
| `--sample-rate INTEGER` | `44100` | Audio sample rate |
| `--epochs INTEGER` | `100` | Training epochs |
| `--verbose, -v` | | Verbose output |
| `--skip-setup` | | Skip dependency checks |

### Examples

```bash
# Basic voice cloning from audio
python src/voice_cloner.py -i voice_sample.wav -o my_voice_clone

# Process video and extract voice
python src/voice_cloner.py -i interview.mp4 -o interview_clone

# Batch process multiple files
python src/voice_cloner.py -i audio_samples/ -o cloned_voices/

# Use simple method (no training, faster)
python src/voice_cloner.py -i test.wav -o test_output -m simple

# Custom sample rate
python src/voice_cloner.py -i recording.wav -o output --sample-rate 48000

# More training epochs (better quality)
python src/voice_cloner.py -i voice.wav -o clone --epochs 200
```

---

## 🔄 Pipeline

### Step-by-Step Process

```
┌─────────────────┐
│   Input File    │
│  (Audio/Video)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Audio Extraction │ ◄─── Video files only
│   (FFmpeg)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Voice Isolation │ ◄─── Separates vocals from music
│   (Demucs)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Feature Extract │ ◄─── Extracts voice characteristics
│     (RVC)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Model Training  │ ◄─── Creates voice model
│     (RVC)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Voice Cloning    │ ◄─── Applies cloned voice
│     (RVC)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Output File   │
│  (Cloned Voice) │
└─────────────────┘
```

### Supported Formats

#### Input Audio
- WAV (`.wav`)
- MP3 (`.mp3`)
- FLAC (`.flac`)
- OGG (`.ogg`)
- M4A (`.m4a`)
- AAC (`.aac`)

#### Input Video
- MP4 (`.mp4`)
- MKV (`.mkv`)
- AVI (`.avi`)
- MOV (`.mov`)
- WebM (`.webm`)
- WMV (`.wmv`)

#### Output
- WAV (`.wav`) - High quality, uncompressed
- MP3 (`.mp3`) - Compressed (optional)

---

## ⚙️ Configuration

### config.json

```json
{
  "sample_rate": 44100,
  "audio_format": "wav",
  "default_method": "rvc",
  "demucs": {
    "model": "demucs",
    "two_stems": "vocals"
  },
  "rvc": {
    "epochs": 100,
    "batch_size": 8,
    "learning_rate": 0.0001
  },
  "output": {
    "format": "wav",
    "quality": "high"
  }
}
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VOICE_CLONER_SAMPLE_RATE` | `44100` | Audio sample rate |
| `VOICE_CLONER_METHOD` | `rvc` | Default cloning method |
| `VOICE_CLONER_EPOCHS` | `100` | Training epochs |

---

## 📚 Documentation

Full documentation is available in the [`docs/`](docs/) directory:

- [Installation Guide](docs/installation.md)
- [User Manual](docs/usage.md)
- [API Reference](docs/api.md)
- [Troubleshooting](docs/troubleshooting.md)
- [FAQ](docs/faq.md)
- [Benchmarking](docs/benchmarking.md)

---

## 🏗️ Architecture

```
voice-cloner/
├── .github/                  # GitHub configuration
│   └── workflows/           # CI/CD workflows
│       ├── test.yml         # Run tests
│       └── release.yml      # Release automation
│
├── docs/                    # Documentation
│   ├── installation.md
│   ├── usage.md
│   ├── api.md
│   └── troubleshooting.md
│
├── src/                     # Source code
│   ├── __init__.py
│   ├── voice_cloner.py      # Main pipeline
│   ├── audio/               # Audio processing modules
│   │   ├── extraction.py
│   │   └── conversion.py
│   ├── isolation/           # Voice isolation
│   │   └── demucs_wrapper.py
│   ├── cloning/             # Voice cloning
│   │   └── rvc_wrapper.py
│   └── utils/               # Utilities
│       ├── config.py
│       └── helpers.py
│
├── tools/                   # External tools (auto-cloned)
│   ├── demucs/              # Voice isolation
│   └── RVC/                 # Voice cloning
│
├── models/                  # Trained voice models
│   └── *.pth
│
├── outputs/                 # Cloned voice outputs
│   └── *.wav
│
├── samples/                 # Sample files for testing
│   ├── audio/
│   └── video/
│
├── tests/                   # Tests
│   ├── __init__.py
│   ├── test_extraction.py
│   ├── test_isolation.py
│   └── test_cloning.py
│
├── .gitignore
├── LICENSE
├── CONTRIBUTING.md
├── README.md
├── requirements.txt
├── setup.py
└── setup.sh
```

---

## 🔧 Development

### Project Structure

```bash
voice-cloner/
├── src/              # Main source code
├── tests/            # Test suite
├── docs/             # Documentation
├── samples/          # Sample files
└── tools/            # External dependencies
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_extraction.py
```

### Code Style

This project follows PEP 8 style guidelines:
- 4-space indentation
- 88-character line length
- Descriptive variable names
- Type hints where appropriate

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

### Ways to Contribute

1. **Report Bugs** - Open an issue with detailed reproduction steps
2. **Suggest Features** - Share your ideas in discussions
3. **Submit Pull Requests** - Fix bugs, add features, improve docs
4. **Test on New Platforms** - Help ensure cross-platform compatibility
5. **Improve Documentation** - Better docs help everyone

### Good First Issues

- [ ] Add support for more audio formats
- [ ] Implement progress bars for long operations
- [ ] Add voice quality metrics
- [ ] Create example notebooks
- [ ] Improve error messages

---

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

```
MIT License

Copyright (c) 2024 Voice Cloner

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## ⚠️ Ethical Considerations

### Responsible Use

Voice cloning technology can be used for both beneficial and harmful purposes. We ask that you:

✅ **DO**
- Use only with consent from voice owners
- Use for educational and research purposes
- Respect privacy and copyright laws
- Be transparent about cloned voices

❌ **DO NOT**
- Clone voices without permission
- Use for fraud, scams, or impersonation
- Create deepfake content for deception
- Violate anyone's privacy or rights

### Legal Notice

The creators of this tool are not responsible for any misuse. Users are solely responsible for ensuring their use complies with all applicable laws and ethical guidelines.

---

## 🆘 Support

### Getting Help

1. **Read the Documentation** - Most questions are answered in [docs/](docs/)
2. **Check the FAQ** - Common issues in [docs/faq.md](docs/faq.md)
3. **Search Issues** - Someone may have had the same question
4. **Open an Issue** - For bugs or feature requests

### Reporting Issues

When reporting an issue, please include:
- Your operating system
- Python version (`python --version`)
- Steps to reproduce
- Error messages (full traceback)
- Sample file (if possible)

---

## 📊 Benchmarks

See [docs/benchmarking.md](docs/benchmarking.md) for performance metrics.

### Quality Comparison

| Method | Quality | Speed | GPU Required | Training Time |
|--------|---------|-------|--------------|---------------|
| RVC (Full) | ★★★★★ | ★★☆ | ✅ Yes | 1-4 hours |
| RVC (Light) | ★★★★ | ★★★ | ❌ No | 30-60 min |
| Simple | ★★★ | ★★★★★ | ❌ No | Instant |

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 2 cores | 4+ cores |
| RAM | 4 GB | 16+ GB |
| Storage | 10 GB | 50+ GB (for models) |
| GPU | None | NVIDIA CUDA-capable |

---

## 🔗 Related Projects

### Voice Isolation
- [Demucs](https://github.com/facebookresearch/demucs) - Facebook's audio separation
- [UVR5](https://github.com/Anjok07/ultimatevocalremovergui) - Ultimate Vocal Remover
- [Spleeter](https://github.com/deezer/spleeter) - Deezer's source separation

### Voice Cloning
- [RVC](https://github.com/liujing04/Retrieval-based-Voice-Conversion-WebUI) - Retrieval-based Voice Conversion
- [Tortoise-TTS](https://github.com/neonbjb/tortoise-tts) - Text to Speech with voice cloning
- [OpenUTAU](https://github.com/stakira/OpenUtau) - Singing voice synthesis

### Commercial Alternatives
- ElevenLabs
- Resemble AI
- Descript Overdub
- VoiceCraft

---

## 🎉 Acknowledgments

- [Facebook Research](https://ai.facebook.com/) - For Demucs
- [RVC Contributors](https://github.com/liujing04/Retrieval-based-Voice-Conversion-WebUI/graphs/contributors) - For RVC
- [PyTorch Team](https://pytorch.org/) - For the ML framework
- All open-source contributors who make this possible

---

<div align="center">

**Made with ❤️ for the open-source community**

*Clone responsibly. Create amazing things.*

</div>
