# API Reference

Use Voice Cloner as a Python library in your own projects.

## 📦 Installation as a Package

### From Source

```bash
# Clone the repository
git clone https://github.com/your-username/voice-cloner.git
cd voice-cloner

# Install in development mode
pip install -e .
```

### Import the Package

```python
from voice_cloner import VoiceCloner
from voice_cloner.src.voice_cloner import VoiceCloner

# Or import specific functions
from voice_cloner.src.voice_cloner import (
    VoiceCloner,
    extract_audio_from_video,
    isolate_vocals,
    train_voice_model,
    clone_voice
)
```

## 🏗️ Classes

### VoiceCloner

Main class for voice cloning operations.

```python
class VoiceCloner(config: dict = None)
```

**Parameters:**
- `config` (dict, optional): Configuration dictionary. Defaults to `{}`.

**Attributes:**
- `config` (dict): Configuration settings
- `base_dir` (Path): Base directory of the project
- `models_dir` (Path): Directory for trained models
- `outputs_dir` (Path): Directory for output files
- `temp_dir` (Path): Directory for temporary files

---

#### Methods

##### `__init__(config: dict = None)`

Initialize the VoiceCloner with configuration.

**Example:**
```python
cloner = VoiceCloner()

# With custom config
cloner = VoiceCloner({
    'sample_rate': 48000,
    'method': 'simple'
})
```

---

##### `extract_audio_from_video(video_path: str, output_path: str = None) -> str`

Extract audio from a video file using FFmpeg.

**Parameters:**
- `video_path` (str): Path to the video file
- `output_path` (str, optional): Output path for audio. Defaults to `temp/<video_name>.wav`

**Returns:**
- `str`: Path to the extracted audio file

**Raises:**
- `FileNotFoundError`: If video file doesn't exist
- `subprocess.CalledProcessError`: If FFmpeg fails

**Example:**
```python
cloner = VoiceCloner()
audio_path = cloner.extract_audio_from_video('video.mp4')
print(f"Extracted audio to: {audio_path}")
```

---

##### `isolate_vocals(audio_path: str, output_dir: str = None) -> str`

Isolate vocals from audio using Demucs.

**Parameters:**
- `audio_path` (str): Path to the audio file
- `output_dir` (str, optional): Output directory. Defaults to `temp/demucs_output`

**Returns:**
- `str`: Path to the isolated vocals file

**Raises:**
- `FileNotFoundError`: If audio file doesn't exist
- `subprocess.CalledProcessError`: If Demucs fails

**Example:**
```python
cloner = VoiceCloner()
vocals_path = cloner.isolate_vocals('audio.wav')
print(f"Isolated vocals at: {vocals_path}")
```

---

##### `extract_vocal_features(vocal_path: str, output_dir: str = None) -> Tuple[str, str]`

Extract vocal features for cloning using RVC.

**Parameters:**
- `vocal_path` (str): Path to the isolated vocals file
- `output_dir` (str, optional): Output directory. Defaults to `temp/rvc_features`

**Returns:**
- `Tuple[str, str]`: Paths to (feature_file, model_path)

**Example:**
```python
cloner = VoiceCloner()
feature_path, model_path = cloner.extract_vocal_features('vocals.mp3')
print(f"Features: {feature_path}")
print(f"Model: {model_path}")
```

---

##### `train_voice_model(vocal_files: List[str], output_model: str = None, epochs: int = 100) -> str`

Train a voice model from vocal samples.

**Parameters:**
- `vocal_files` (List[str]): List of vocal sample file paths
- `output_model` (str, optional): Path for output model. Defaults to `models/voice_<hash>.pth`
- `epochs` (int, optional): Number of training epochs. Defaults to 100

**Returns:**
- `str`: Path to the trained model file

**Example:**
```python
cloner = VoiceCloner()
model_path = cloner.train_voice_model([
    'sample1.wav',
    'sample2.wav',
    'sample3.wav'
], epochs=200)
print(f"Trained model saved to: {model_path}")
```

---

##### `clone_voice(input_file: str, reference_voice: str, output_file: str = None, method: str = "rvc") -> str`

Clone voice from reference to input file.

**Parameters:**
- `input_file` (str): Input audio file to clone voice onto
- `reference_voice` (str): Reference voice sample or model
- `output_file` (str, optional): Output file path. Defaults to `outputs/cloned_<input_name>`
- `method` (str, optional): Cloning method (`'rvc'` or `'simple'`). Defaults to `'rvc'`

**Returns:**
- `str`: Path to the output file with cloned voice

**Example:**
```python
cloner = VoiceCloner()
cloned_path = cloner.clone_voice(
    input_file='target.wav',
    reference_voice='my_voice.wav',
    method='rvc'
)
print(f"Cloned voice saved to: {cloned_path}")
```

---

##### `process_file(input_path: str, output_dir: str = None) -> dict`

Complete pipeline for a single file.

**Parameters:**
- `input_path` (str): Input file (audio or video)
- `output_dir` (str, optional): Output directory. Defaults to `outputs/<input_name>`

**Returns:**
- `dict`: Dictionary with results including:
  - `input`: Input file path
  - `output_dir`: Output directory
  - `steps`: Processing steps
  - `final_output`: Final output file path
  - `voice_model`: Trained voice model path

**Example:**
```python
cloner = VoiceCloner()
result = cloner.process_file('my_voice.wav')
print(f"Final output: {result['final_output']}")
print(f"Voice model: {result['voice_model']}")
```

---

##### `process_directory(input_dir: str, output_dir: str = None) -> List[dict]`

Process all files in a directory.

**Parameters:**
- `input_dir` (str): Input directory with files
- `output_dir` (str, optional): Output directory. Defaults to `outputs/<input_dir_name>`

**Returns:**
- `List[dict]`: List of results for each processed file

**Example:**
```python
cloner = VoiceCloner()
results = cloner.process_directory('samples/')
for result in results:
    print(f"Processed: {result['input']} -> {result['final_output']}")
```

---

## 🎯 Functions

### Standalone Functions

You can also use the functions directly without instantiating the class.

---

#### `main()`

Run the command-line interface.

**Example:**
```python
from voice_cloner.src.voice_cloner import main

# This is what gets called when running from command line
main()
```

---

## 📝 Examples

### Example 1: Basic Voice Cloning

```python
from voice_cloner.src.voice_cloner import VoiceCloner

# Initialize
cloner = VoiceCloner()

# Clone a voice from audio file
result = cloner.process_file('my_voice.wav', 'my_clone')

print(f"Input: {result['input']}")
print(f"Output: {result['final_output']}")
print(f"Model: {result['voice_model']}")
```

### Example 2: Extract Vocals from Video

```python
from voice_cloner.src.voice_cloner import VoiceCloner

cloner = VoiceCloner()

# Extract audio from video
audio_path = cloner.extract_audio_from_video('interview.mp4')

# Isolate vocals
vocals_path = cloner.isolate_vocals(audio_path)

print(f"Extracted vocals: {vocals_path}")
```

### Example 3: Batch Process Multiple Files

```python
from voice_cloner.src.voice_cloner import VoiceCloner

cloner = VoiceCloner()

# Process all files in a directory
results = cloner.process_directory('audio_samples/')

# Print summary
print(f"Processed {len(results)} files:")
for result in results:
    if 'final_output' in result:
        print(f"  ✓ {result['input']}")
    else:
        print(f"  ✗ {result['input']}: {result.get('error', 'Unknown error')}")
```

### Example 4: Custom Pipeline

```python
from voice_cloner.src.voice_cloner import VoiceCloner

cloner = VoiceCloner()

# Step 1: Extract audio (if video)
input_file = 'video.mp4'
try:
    audio_path = cloner.extract_audio_from_video(input_file)
except:
    audio_path = input_file

# Step 2: Isolate vocals
vocals_path = cloner.isolate_vocals(audio_path)

# Step 3: Train model
model_path = cloner.train_voice_model([vocals_path], epochs=50)

# Step 4: Clone to new audio
cloned_path = cloner.clone_voice(
    input_file='new_audio.wav',
    reference_voice=vocals_path,
    method='simple'
)

print(f"Custom pipeline complete: {cloned_path}")
```

### Example 5: Use with Different Methods

```python
from voice_cloner.src.voice_cloner import VoiceCloner

cloner = VoiceCloner()

# RVC method (high quality, slow)
result_rvc = cloner.process_file('voice.wav', 'clone_rvc', method='rvc')

# Simple method (fast, lower quality)
result_simple = cloner.process_file('voice.wav', 'clone_simple', method='simple')

print(f"RVC: {result_rvc['final_output']}")
print(f"Simple: {result_simple['final_output']}")
```

### Example 6: Error Handling

```python
from voice_cloner.src.voice_cloner import VoiceCloner

cloner = VoiceCloner()

try:
    result = cloner.process_file('nonexistent.wav')
except FileNotFoundError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## 📊 Return Types

### Process Result Dictionary

```python
result = {
    'input': str,              # Input file path
    'output_dir': str,         # Output directory
    'steps': dict,             # Processing steps
    'final_output': str,       # Final output file path
    'voice_model': str         # Trained voice model path
}
```

### Steps Dictionary

```python
steps = {
    'audio_extraction': str,   # Path to extracted audio (or {'skipped': True})
    'vocal_isolation': str,   # Path to isolated vocals
    'feature_extraction': dict, # {'features': str, 'model': str}
    'model_training': str,     # Path to trained model
    'voice_cloning': str       # Path to cloned output
}
```

---

## 🔧 Configuration

### Using config.json

Create a `config.json` file in the project root:

```json
{
  "sample_rate": 48000,
  "audio_format": "wav",
  "default_method": "simple",
  "demucs": {
    "model": "demucs",
    "two_stems": "vocals"
  },
  "rvc": {
    "epochs": 50,
    "batch_size": 4,
    "learning_rate": 0.0001
  },
  "output": {
    "format": "wav",
    "quality": "high"
  }
}
```

The VoiceCloner will automatically load this configuration.

### Environment Variables

You can also set configuration via environment variables:

```bash
export VOICE_CLONER_SAMPLE_RATE=48000
export VOICE_CLONER_METHOD=simple
```

These will be read by the VoiceCloner on initialization.

---

## 🎓 Best Practices

### 1. Resource Management

```python
from voice_cloner.src.voice_cloner import VoiceCloner
import shutil

cloner = VoiceCloner()

try:
    result = cloner.process_file('voice.wav')
finally:
    # Clean up temp files if needed
    if cloner.temp_dir.exists():
        shutil.rmtree(cloner.temp_dir)
```

### 2. Progress Tracking

```python
from voice_cloner.src.voice_cloner import VoiceCloner
from tqdm import tqdm

cloner = VoiceCloner()

# Process multiple files with progress
files = ['file1.wav', 'file2.wav', 'file3.wav']
for file in tqdm(files, desc='Processing'):
    result = cloner.process_file(file)
    # Do something with result
```

### 3. Custom Config per Instance

```python
from voice_cloner.src.voice_cloner import VoiceCloner

# Different configurations for different tasks
high_quality_config = {
    'sample_rate': 48000,
    'method': 'rvc',
    'epochs': 200
}

fast_config = {
    'sample_rate': 22050,
    'method': 'simple',
    'epochs': 10
}

cloner_hq = VoiceCloner(high_quality_config)
cloner_fast = VoiceCloner(fast_config)
```

---

## 🐛 Error Handling

### Common Exceptions

| Exception | Cause | Solution |
|-----------|-------|----------|
| `FileNotFoundError` | Input file doesn't exist | Check file path |
| `subprocess.CalledProcessError` | FFmpeg/Demucs failed | Check dependencies |
| `MemoryError` | Not enough RAM | Reduce batch size or use simple method |
| `RuntimeError` | CUDA out of memory | Use CPU or reduce model size |

### Handling Errors

```python
from voice_cloner.src.voice_cloner import VoiceCloner
import sys

cloner = VoiceCloner()

try:
    result = cloner.process_file('voice.wav')
except FileNotFoundError:
    print("Error: Input file not found")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
```

---

## 📚 Related Documentation

- [Installation Guide](installation.md) - Setup instructions
- [Usage Guide](usage.md) - Command-line usage
- [Troubleshooting](troubleshooting.md) - Common issues
- [FAQ](faq.md) - Frequently asked questions
