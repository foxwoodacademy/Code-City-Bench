# Installation Guide

Complete installation instructions for Voice Cloner on various platforms.

## 📋 Requirements

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **Operating System** | Linux, macOS, Windows (WSL2) | Linux, macOS |
| **Python** | 3.8+ | 3.10+ |
| **RAM** | 4 GB | 16+ GB |
| **CPU** | 2 cores | 4+ cores |
| **Storage** | 10 GB | 50+ GB (for models) |
| **GPU** | None | NVIDIA CUDA-capable (for faster training) |

### Dependencies

#### System Packages

| Platform | Packages |
|----------|----------|
| **All Platforms** | Git, FFmpeg |
| **Termux** | `pkg install python git ffmpeg` |
| **Debian/Ubuntu** | `sudo apt install python3 python3-pip git ffmpeg libsndfile1` |
| **Fedora/RHEL** | `sudo dnf install python3 python3-pip git ffmpeg libsndfile` |
| **Arch Linux** | `sudo pacman -S python python-pip git ffmpeg libsndfile` |
| **macOS** | `brew install python git ffmpeg` |

## 🚀 Installation Methods

### Method 1: Automatic Setup (Recommended)

The easiest way to get started:

```bash
# Clone the repository
git clone https://github.com/your-username/voice-cloner.git
cd voice-cloner

# Make setup script executable
chmod +x setup.sh

# Run setup (automatically detects platform)
./setup.sh
```

The setup script will:
1. Install system dependencies
2. Clone Demucs for voice isolation
3. Clone RVC for voice cloning
4. Install all Python packages
5. Verify the installation

### Method 2: Manual Installation

#### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/voice-cloner.git
cd voice-cloner
```

#### Step 2: Install System Dependencies

**Termux (Android):**
```bash
pkg update -y && pkg upgrade -y
pkg install -y python git ffmpeg wget
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt update -y
sudo apt install -y python3 python3-pip python3-venv git ffmpeg wget
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install -y python3 python3-pip python3-virtualenv git ffmpeg wget
```

**macOS:**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew update
brew install python git ffmpeg wget
```

**Windows (WSL2):**
1. Install WSL2 with Ubuntu
2. Follow the Linux (Debian/Ubuntu) instructions above

#### Step 3: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/macOS:
source venv/bin/activate

# On Windows (in WSL2):
source venv/bin/activate
```

#### Step 4: Install Python Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

#### Step 5: Setup External Tools

**Setup Demucs for voice isolation:**
```bash
git clone https://github.com/facebookresearch/demucs tools/demucs
pip install -e tools/demucs
```

**Setup RVC for voice cloning:**
```bash
git clone https://github.com/liujing04/Retrieval-based-Voice-Conversion-WebUI tools/RVC
cd tools/RVC
pip install -r requirements.txt
cd ../..
```

### Method 3: Docker (Alternative)

For containerized deployment:

```bash
# Build the image
docker build -t voice-cloner .

# Run with a volume for input/output files
docker run -it --rm \
  -v $(pwd)/samples:/app/samples \
  -v $(pwd)/outputs:/app/outputs \
  voice-cloner \
  python src/voice_cloner.py -i samples/my_voice.wav -o outputs/
```

## 🔍 Verify Installation

Check that everything is installed correctly:

```bash
# Check Python version
python --version
# Should output: Python 3.8+

# Check pip
pip --version

# Check FFmpeg
ffmpeg -version

# Check Git
git --version

# Run a test
python src/voice_cloner.py --input samples/test.wav --output test_output/ --method simple
```

## ⚙️ Optional Dependencies

### For Development

```bash
pip install -r requirements-dev.txt
```

Contains:
- pytest - Testing framework
- pytest-cov - Coverage reporting
- black - Code formatter
- flake8 - Linter
- mypy - Type checker
- isort - Import sorter
- Sphinx - Documentation generator

### For GPU Acceleration

**NVIDIA CUDA (Linux):**
```bash
# Install CUDA toolkit from NVIDIA website
# Then install PyTorch with CUDA:
pip uninstall torch torchaudio
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**macOS (Metal):**
```bash
pip uninstall torch torchaudio
pip install torch torchaudio
```

## 📁 Directory Structure

After installation, your directory should look like:

```
voice-cloner/
├── src/
│   └── voice_cloner.py      # Main script
├── tools/
│   ├── demucs/              # Voice isolation (cloned during setup)
│   └── RVC/                 # Voice cloning (cloned during setup)
├── models/                  # Trained models will be saved here
├── outputs/                 # Output files
├── temp/                    # Temporary files
├── samples/                 # Sample files (create this for testing)
├── venv/                    # Virtual environment (if created)
├── requirements.txt
├── setup.sh
└── README.md
```

## 🎯 Platform-Specific Notes

### Termux (Android)

**Limitations:**
- RVC training may be slow on mobile hardware
- GPU acceleration is not available
- Consider using proot-distro with Ubuntu for better compatibility

**Recommended:**
```bash
# Install proot-distro for better Linux environment
pkg install proot-distro
proot-distro install ubuntu
proot-distro login ubuntu
# Then follow Linux instructions inside Ubuntu
```

### macOS

**Notes:**
- FFmpeg installation via Homebrew works well
- M1/M2 Macs: Use native PyTorch for Metal acceleration
- Intel Macs: Use standard PyTorch

**Troubleshooting:**
```bash
# If you get "command not found" for pip:
python3 -m pip install --upgrade pip

# If Python is not in PATH:
export PATH="/usr/local/bin:$PATH"
```

### Windows

**Recommended:** Use WSL2 (Windows Subsystem for Linux)

1. Enable WSL2:
   ```powershell
   wsl --install
   ```

2. Install Ubuntu from Microsoft Store
3. Follow Linux installation instructions inside WSL2

**Alternative:** Native Windows (not recommended)
- Install Python from python.org
- Install FFmpeg from ffmpeg.org
- Install Git from git-scm.com
- Some functionality may not work correctly

### Linux

**Notes:**
- Tested on Ubuntu 20.04/22.04, Debian, Fedora, Arch
- For CUDA support, install NVIDIA drivers first
- Use virtual environment to avoid system Python conflicts

## 🛠️ Troubleshooting Installation

### Common Issues

**"ffmpeg: command not found"**
```bash
# Termux:
pkg install ffmpeg

# Ubuntu/Debian:
sudo apt install ffmpeg

# macOS:
brew install ffmpeg
```

**"ModuleNotFoundError: No module named 'torch'"**
```bash
pip install torch torchaudio
```

**"Python not found"**
```bash
# Try python3 instead
python3 src/voice_cloner.py ...

# Or create a symlink
ln -s $(which python3) /usr/local/bin/python
```

**"Permission denied" when running setup.sh**
```bash
chmod +x setup.sh
./setup.sh
```

**GitHub rate limit exceeded when cloning**
```bash
# Use SSH instead of HTTPS
git clone git@github.com:facebookresearch/demucs.git tools/demucs

# Or use --depth 1 for shallow clone
git clone --depth 1 https://github.com/facebookresearch/demucs.git tools/demucs
```

### Verify External Tools

After setup, verify the external tools are cloned:

```bash
ls -la tools/
# Should show: demucs/ and RVC/
```

If they're missing, clone them manually:

```bash
# Demucs
git clone https://github.com/facebookresearch/demucs tools/demucs
pip install -e tools/demucs

# RVC
git clone https://github.com/liujing04/Retrieval-based-Voice-Conversion-WebUI tools/RVC
```

## 📚 Next Steps

After installation, proceed to:
- [Usage Guide](usage.md) - Learn how to use Voice Cloner
- [Configuration](configuration.md) - Customize settings
- [API Reference](api.md) - Use as a library
