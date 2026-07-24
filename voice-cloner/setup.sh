#!/bin/bash
# Voice Cloner Setup Script
# Run this to install all dependencies

set -e

echo "=========================================="
echo "Voice Cloner Setup"
echo "=========================================="

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "Please don't run as root"
    exit 1
fi

# Detect platform
if [ -d /data/data/com.termux/files ]; then
    echo "Detected: Termux (Android)"
    PLATFORM="termux"
elif [ "$(uname)" == "Linux" ]; then
    echo "Detected: Linux"
    PLATFORM="linux"
elif [ "$(uname)" == "Darwin" ]; then
    echo "Detected: macOS"
    PLATFORM="macos"
else
    echo "Detected: Unknown platform"
    PLATFORM="unknown"
fi

echo ""
echo "Step 1: Installing system dependencies..."

if [ "$PLATFORM" == "termux" ]; then
    # Termux-specific setup
    pkg update -y
    pkg upgrade -y
    
    # Required packages
    pkg install -y \
        python \
        git \
        ffmpeg \
        wget \
        libjpeg-turbo \
        libpng \
        libwebp
    
    # Python packages
    pip install --upgrade pip
    pip install -r requirements.txt
    
    echo ""
    echo "Termux setup complete!"
    echo "Note: For best results, use Termux with proot-distro"
    echo "      (Ubuntu recommended for full RVC support)"
    
elif [ "$PLATFORM" == "linux" ] || [ "$PLATFORM" == "macos" ]; then
    # Linux/macOS setup
    if [ "$PLATFORM" == "linux" ]; then
        if command -v apt-get &> /dev/null; then
            sudo apt-get update -y
            sudo apt-get install -y \
                python3 \
                python3-pip \
                git \
                ffmpeg \
                wget \
                libsndfile1 \
                sox
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y \
                python3 \
                python3-pip \
                git \
                ffmpeg \
                wget \
                libsndfile \
                sox
        elif command -v yum &> /dev/null; then
            sudo yum install -y \
                python3 \
                python3-pip \
                git \
                ffmpeg \
                wget \
                libsndfile \
                sox
        fi
    elif [ "$PLATFORM" == "macos" ]; then
        # macOS
        if ! command -v brew &> /dev/null; then
            echo "Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        
        brew update
        brew install \
            python \
            git \
            ffmpeg \
            wget \
            libsndfile \
            sox
    fi
    
    # Install Python dependencies
    pip3 install --upgrade pip
    pip3 install -r requirements.txt
    
    echo ""
    echo "Linux/macOS setup complete!"
else
    echo "Unsupported platform: $PLATFORM"
    echo "Please install dependencies manually:"
    echo "  - Python 3.8+"
    echo "  - Git"
    echo "  - FFmpeg"
    echo "  - pip"
    echo "Then run: pip install -r requirements.txt"
fi

echo ""
echo "Step 2: Setting up voice isolation (Demucs)..."
cd voice_cloner
if [ ! -d "tools/demucs" ]; then
    git clone https://github.com/facebookresearch/demucs tools/demucs
    pip install -e tools/demucs
    echo "Demucs installed successfully"
else
    echo "Demucs already installed"
fi

echo ""
echo "Step 3: Setting up voice cloning (RVC - optional)..."
if [ ! -d "tools/RVC" ]; then
    echo "Cloning RVC repository..."
    git clone https://github.com/liujing04/Retrieval-based-Voice-Conversion-WebUI tools/RVC
    echo "RVC cloned. Additional setup required."
    echo "See: https://github.com/liujing04/Retrieval-based-Voice-Conversion-WebUI"
    echo ""
    echo "To complete RVC setup, you'll need to:"
    echo "  1. cd tools/RVC"
    echo "  2. pip install -r requirements.txt"
    echo "  3. Download pretrained models"
    echo "  4. Run: python train.py [options]"
else
    echo "RVC already cloned"
fi

echo ""
echo "=========================================="
echo "Voice Cloner Setup Complete!"
echo "=========================================="
echo ""
echo "Usage:"
echo "  python src/voice_cloner.py --input <file/dir> --output <dir>"
echo ""
echo "Examples:"
echo "  # Process a single audio file"
echo "  python src/voice_cloner.py -i my_voice.wav -o output/"
echo ""
echo "  # Process a video file"
echo "  python src/voice_cloner.py -i my_video.mp4 -o output/"
echo ""
echo "  # Process a directory"
echo "  python src/voice_cloner.py -i samples/ -o clones/"
echo ""
echo "Note: RVC requires additional setup for full voice cloning."
echo "      See tools/RVC/README.md for details."
