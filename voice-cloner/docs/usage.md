# Usage Guide

Complete guide to using Voice Cloner for voice cloning tasks.

## 🎯 Quick Start

### Basic Usage

Clone a voice from an audio file:

```bash
python src/voice_cloner.py --input my_voice.wav --output my_clone
```

Clone a voice from a video file:

```bash
python src/voice_cloner.py --input my_video.mp4 --output my_clone
```

### Command Line Interface

```
python src/voice_cloner.py [OPTIONS]
```

## 📝 Examples

### Example 1: Clone from Audio File

```bash
# Basic cloning
python src/voice_cloner.py -i samples/voice.wav -o outputs/voice_clone

# With custom sample rate
python src/voice_cloner.py -i voice.wav -o clone --sample-rate 48000

# With more training epochs (better quality)
python src/voice_cloner.py -i voice.wav -o clone --epochs 200
```

### Example 2: Clone from Video File

```bash
# Extract and clone voice from video
python src/voice_cloner.py -i interview.mp4 -o interview_clone

# Specify output directory
python src/voice_cloner.py -i video.mp4 -o my_project/clones/video1
```

### Example 3: Batch Processing

```bash
# Process all files in a directory
python src/voice_cloner.py -i samples/ -o clones/

# Process with verbose output
python src/voice_cloner.py -i audio_samples/ -o cloned/ -v
```

### Example 4: Different Methods

```bash
# Use RVC (default, high quality, requires training)
python src/voice_cloner.py -i voice.wav -o clone -m rvc

# Use simple method (fast, no training)
python src/voice_cloner.py -i voice.wav -o clone -m simple
```

## 🎛️ Command Line Options

### Required Arguments

| Flag | Description |
|------|-------------|
| `--input, -i TEXT` | Input file or directory. Can be audio or video. |

### Optional Arguments

| Flag | Default | Description |
|------|---------|-------------|
| `--output, -o TEXT` | `outputs/<input_name>` | Output directory for results. |
| `--method, -m TEXT` | `rvc` | Cloning method: `rvc` or `simple`. |
| `--sample-rate INTEGER` | `44100` | Audio sample rate in Hz. |
| `--epochs INTEGER` | `100` | Number of training epochs for RVC. |
| `--verbose, -v` | | Enable verbose output. |
| `--skip-setup` | | Skip dependency checks. |

### Configuration File

You can also use a `config.json` file for default settings:

```json
{
  "sample_rate": 48000,
  "default_method": "simple",
  "epochs": 50,
  "output_format": "wav"
}
```

## 📁 Input Files

### Supported Formats

#### Audio Files

| Format | Extension | Notes |
|--------|-----------|-------|
| WAV | `.wav` | Uncompressed, recommended |
| MP3 | `.mp3` | Compressed, supported |
| FLAC | `.flac` | Lossless, supported |
| OGG | `.ogg` | Open format, supported |
| M4A | `.m4a` | Apple format, supported |
| AAC | `.aac` | Advanced Audio Coding |
| AIFF | `.aiff` | Audio Interchange File |
| WMA | `.wma` | Windows Media Audio |

#### Video Files

| Format | Extension | Notes |
|--------|-----------|-------|
| MP4 | `.mp4` | Most common, recommended |
| MKV | `.mkv` | Matroska format |
| AVI | `.avi` | Audio Video Interleave |
| MOV | `.mov` | Apple QuickTime |
| WebM | `.webm` | Web format |
| WMV | `.wmv` | Windows Media Video |
| FLV | `.flv` | Flash Video |

### Input Quality Guidelines

For best results:

✅ **DO:**
- Use high-quality source material (44.1kHz or higher)
- Ensure clear, loud voice recordings
- Minimize background noise
- Use at least 5-10 seconds of voice samples
- Speak naturally and clearly

❌ **AVOID:**
- Low-quality recordings (< 16kHz sample rate)
- Heavy compression artifacts
- Excessive background noise
- Very short samples (< 2 seconds)
- Whispering or muffled speech

## 🎨 Output Files

### Output Directory Structure

```
outputs/
├── <input_name>/
│   ├── audio.wav              # Extracted audio (if from video)
│   ├── vocals.mp3             # Isolated vocals (from Demucs)
│   ├── features.npy           # Extracted voice features
│   ├── model.pth              # Trained voice model
│   └── cloned_output.wav      # Final cloned voice
└── <next_input>/
    └── ...
```

### Output Formats

| Type | Format | Description |
|------|--------|-------------|
| Extracted Audio | WAV | 16-bit PCM, 44.1kHz (or custom) |
| Isolated Vocals | MP3 | From Demucs processing |
| Features | NPY | NumPy array with voice features |
| Model | PTH | PyTorch model file |
| Cloned Output | WAV | Final cloned voice |

## 🔄 The Pipeline Explained

Voice Cloner processes files through these stages:

### Stage 1: Audio Extraction (Video Only)

If the input is a video file, audio is extracted using FFmpeg:

```bash
ffmpeg -i input.mp4 -vn -acodec pcm_s16le -ar 44100 -ac 2 output.wav
```

**Options:**
- `-vn`: No video
- `-acodec pcm_s16le`: 16-bit PCM encoding
- `-ar 44100`: Sample rate
- `-ac 2`: Stereo audio

### Stage 2: Voice Isolation

Vocals are separated from background music/noise using Demucs:

```bash
python -m demucs --mp3 --two-stems vocals input.wav -o output_dir
```

This creates:
- `vocals.mp3`: Isolated voice
- `no_vocals.mp3`: Background music/noise

### Stage 3: Feature Extraction

Voice characteristics are extracted for cloning:

- Spectral features
- Pitch information
- Timbre characteristics
- Speaker embeddings

### Stage 4: Model Training (RVC Method)

A voice model is trained using the isolated vocals:

```bash
# Training parameters
python tools/RVC/train.py \
  --input vocals.mp3 \
  --output model.pth \
  --epochs 100 \
  --batch_size 8 \
  --learning_rate 0.0001
```

### Stage 5: Voice Cloning

The trained model is used to clone the voice onto target audio:

```bash
python tools/RVC/infer.py \
  --input target.wav \
  --model model.pth \
  --output cloned.wav
```

## ⚡ Methods Compared

### RVC Method (Default)

| Aspect | Details |
|--------|---------|
| Quality | ★★★★★ (Best) |
| Speed | ★★☆ (Slow) |
| Training Required | ✅ Yes |
| GPU Acceleration | ✅ Supported |
| Use Case | High-quality cloning |
| Training Time | 30 min - 4 hours |

**Best for:** Production use, high-quality results

**Requirements:**
- PyTorch with CUDA (for GPU)
- Significant RAM (16+ GB recommended)
- Storage for models (~1-2 GB per voice)

### Simple Method

| Aspect | Details |
|--------|---------|
| Quality | ★★★ (Good) |
| Speed | ★★★★★ (Fastest) |
| Training Required | ❌ No |
| GPU Acceleration | ❌ Not needed |
| Use Case | Quick testing, lightweight |
| Processing Time | Seconds |

**Best for:** Quick tests, low-resource devices, simple use cases

## 🎯 Use Cases

### Use Case 1: Voice Preservation

Clone a loved one's voice for future use in videos or audiobooks.

```bash
# Process a collection of voice recordings
python src/voice_cloner.py -i family_voices/ -o preserved_voices/
```

### Use Case 2: Content Creation

Create voiceovers with your own cloned voice.

```bash
# Clone your voice from a sample
python src/voice_cloner.py -i my_voice_sample.wav -o my_voice_model

# Then use the model for new content
# (See: Using Trained Models section)
```

### Use Case 3: Language Learning

Clone native speaker voices for language practice.

```bash
# Clone from educational material
python src/voice_cloner.py -i language_samples/ -o language_voices/
```

### Use Case 4: Audio Restoration

Isolate and clean up voices from old recordings.

```bash
# Extract voice from noisy audio
python src/voice_cloner.py -i old_recording.wav -o restored/
```

### Use Case 5: Research

Experiment with voice cloning technology.

```bash
# Test with different parameters
python src/voice_cloner.py -i test.wav -o experiment1 --epochs 50
python src/voice_cloner.py -i test.wav -o experiment2 --epochs 200
```

## 🔄 Using Trained Models

After training, you can reuse voice models:

```bash
# Train a model
python src/voice_cloner.py -i voice_sample.wav -o my_voice

# The model is saved at: models/voice_<hash>.pth

# Use the model to clone new audio
# (This functionality will be expanded in future versions)
```

## 📊 Monitoring Progress

### Verbose Output

Use the `-v` or `--verbose` flag for detailed progress:

```bash
python src/voice_cloner.py -i voice.wav -o clone -v
```

This will show:
- Current processing stage
- File paths being used
- Processing times
- Any warnings or issues

### Progress Files

During processing, temporary files are created in the `temp/` directory:

```
temp/
├── demucs_output/      # Demucs processing
├── rvc_features/       # RVC feature extraction
└── *.wav               # Intermediate audio files
```

## ⚙️ Customizing Parameters

### Sample Rate

Higher sample rates provide better quality but use more storage:

```bash
# 44.1kHz (CD quality, default)
python src/voice_cloner.py -i voice.wav -o clone --sample-rate 44100

# 48kHz (Studio quality)
python src/voice_cloner.py -i voice.wav -o clone --sample-rate 48000

# 16kHz (Telephone quality, faster)
python src/voice_cloner.py -i voice.wav -o clone --sample-rate 16000
```

### Training Epochs

More epochs = better quality but longer training:

```bash
# Quick test (10 epochs)
python src/voice_cloner.py -i voice.wav -o test --epochs 10

# Good quality (100 epochs, default)
python src/voice_cloner.py -i voice.wav -o clone --epochs 100

# High quality (200+ epochs)
python src/voice_cloner.py -i voice.wav -o high_quality --epochs 200
```

### Method Selection

Choose between quality and speed:

```bash
# RVC: Best quality, requires training
python src/voice_cloner.py -i voice.wav -o clone -m rvc

# Simple: Fast, no training, lower quality
python src/voice_cloner.py -i voice.wav -o clone -m simple
```

## 🛠️ Tips & Tricks

### Tip 1: Better Voice Isolation

For better vocal isolation:
- Use high-quality source material
- Ensure the voice is clear and loud
- Minimize background music/noise
- Use at least 10 seconds of audio

### Tip 2: Faster Processing

To speed up processing:
- Use `--method simple` for quick tests
- Reduce `--epochs` for faster training
- Use a lower `--sample-rate`
- Process on GPU if available

### Tip 3: Batch Processing

Process multiple files efficiently:

```bash
# Create a samples directory
mkdir samples
# Add all your audio/video files
cp *.wav samples/
cp *.mp4 samples/

# Process all files
python src/voice_cloner.py -i samples/ -o clones/
```

### Tip 4: Clean Up

Remove temporary files to save space:

```bash
# Remove temp directory
rm -rf temp/

# Remove outputs
rm -rf outputs/

# Start fresh
rm -rf temp/ outputs/ models/
```

## 🐛 Troubleshooting Usage

### "No files found to process"

**Cause:** Input directory is empty or contains unsupported files.

**Solution:**
```bash
# Check what files are in the directory
ls samples/

# Only supported formats will be processed
# Supported: .wav, .mp3, .flac, .ogg, .m4a, .mp4, .mkv, .avi, .mov, .webm
```

### "Output directory already exists"

**Cause:** The output directory exists from a previous run.

**Solution:**
```bash
# Remove the existing directory
rm -rf outputs/my_clone

# Or specify a new output path
python src/voice_cloner.py -i voice.wav -o new_output/
```

### "Not enough memory"

**Cause:** RVC training requires significant RAM.

**Solution:**
```bash
# Use simple method (no training)
python src/voice_cloner.py -i voice.wav -o clone -m simple

# Reduce epochs
python src/voice_cloner.py -i voice.wav -o clone --epochs 10

# Use a machine with more RAM
```

### "CUDA out of memory"

**Cause:** GPU doesn't have enough VRAM.

**Solution:**
```bash
# Use CPU only
# (RVC will automatically use CPU if CUDA is not available)

# Reduce batch size (in config.json or future versions)

# Use a GPU with more VRAM
```

## 📚 Next Steps

- [Installation Guide](installation.md) - Setup instructions
- [API Reference](api.md) - Use as a Python library
- [Troubleshooting](troubleshooting.md) - Common issues and fixes
- [FAQ](faq.md) - Frequently asked questions
