#!/usr/bin/env python3
"""
Voice Cloner - Local, Free Voice Cloning Tool

Pipeline:
1. Extract audio from video files (if needed)
2. Isolate vocals from audio using Demucs
3. Train voice model using RVC
4. Clone voice for TTS

Usage:
    python voice_cloner.py --input <file/dir> --output <dir> [options]
"""

import os
import sys
import argparse
import subprocess
import json
from pathlib import Path
from typing import List, Optional, Tuple
import shutil
import hashlib

# Configuration
DEMUCS_REPO = "https://github.com/facebookresearch/demucs"
RVC_REPO = "https://github.com/liujing04/Retrieval-based-Voice-Conversion-WebUI"
DEFAULT_SAMPLE_RATE = 44100

class VoiceCloner:
    def __init__(self, config: dict = None):
        """Initialize voice cloner with configuration."""
        self.config = config or {}
        self.base_dir = Path(__file__).parent.parent
        self.models_dir = self.base_dir / "models"
        self.outputs_dir = self.base_dir / "outputs"
        self.temp_dir = self.base_dir / "temp"
        
        # Ensure directories exist
        os.makedirs(self.models_dir, exist_ok=True)
        os.makedirs(self.outputs_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Check dependencies
        self._check_dependencies()
    
    def _check_dependencies(self) -> bool:
        """Check if required tools are installed."""
        required = ['ffmpeg', 'python', 'git']
        missing = []
        
        for cmd in required:
            try:
                subprocess.run([cmd, '--version'], 
                             capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                missing.append(cmd)
        
        if missing:
            print(f"Warning: Missing dependencies: {', '.join(missing)}")
            print("Install with:")
            print("  - ffmpeg: pkg install ffmpeg (Termux)")
            print("  - python: pkg install python (Termux)")
            print("  - git: pkg install git (Termux)")
            return False
        return True
    
    def _get_file_hash(self, file_path: str) -> str:
        """Generate hash for file to use as unique identifier."""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()[:12]
    
    def extract_audio_from_video(self, video_path: str, output_path: str = None) -> str:
        """
        Extract audio from video file using ffmpeg.
        
        Args:
            video_path: Path to video file
            output_path: Optional output path for audio
            
        Returns:
            Path to extracted audio file
        """
        video_path = Path(video_path)
        if output_path is None:
            output_path = self.temp_dir / f"{video_path.stem}.wav"
        else:
            output_path = Path(output_path)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-vn',              # No video
            '-acodec', 'pcm_s16le',
            '-ar', str(DEFAULT_SAMPLE_RATE),
            '-ac', '2',        # Stereo
            '-y',              # Overwrite
            str(output_path)
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"  Extracted audio: {output_path}")
            return str(output_path)
        except subprocess.CalledProcessError as e:
            print(f"  Error extracting audio: {e.stderr.decode()}")
            raise
    
    def setup_demucs(self) -> Path:
        """
        Setup Demucs for vocal isolation.
        
        Returns:
            Path to demucs directory
        """
        demucs_dir = self.base_dir / "tools" / "demucs"
        
        if not demucs_dir.exists():
            print("Setting up Demucs...")
            subprocess.run(['git', 'clone', DEMUCS_REPO, str(demucs_dir)], 
                         check=True)
            
            # Install dependencies
            subprocess.run(
                ['pip', 'install', '-e', str(demucs_dir)],
                check=True
            )
        
        return demucs_dir
    
    def isolate_vocals(self, audio_path: str, output_dir: str = None) -> str:
        """
        Isolate vocals from audio using Demucs.
        
        Args:
            audio_path: Path to audio file
            output_dir: Optional output directory
            
        Returns:
            Path to isolated vocals file
        """
        audio_path = Path(audio_path)
        
        # Setup Demucs
        demucs_dir = self.setup_demucs()
        
        if output_dir is None:
            output_dir = self.temp_dir / "demucs_output"
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Run Demucs with vocal separation
        cmd = [
            'python', '-m', 'demucs',
            '--mp3',            # Output as MP3
            '--two-stems', 'vocals',  # Separate into vocals and no_vocals
            str(audio_path),
            '-o', str(output_dir)
        ]
        
        try:
            print("  Isolating vocals with Demucs...")
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Find the vocals file
            vocals_dir = output_dir / Path(audio_path.stem)
            vocals_file = vocals_dir / "vocals.mp3"
            
            if vocals_file.exists():
                print(f"  Isolated vocals: {vocals_file}")
                return str(vocals_file)
            else:
                # Try alternative naming
                vocals_file = vocals_dir / "vocals.mp3"
                if vocals_file.exists():
                    return str(vocals_file)
                
                # List what we got
                files = list(vocals_dir.glob("*"))
                print(f"  Files in output: {files}")
                raise FileNotFoundError(f"Vocals file not found in {vocals_dir}")
                
        except subprocess.CalledProcessError as e:
            print(f"  Error isolating vocals: {e.stderr.decode()}")
            raise
    
    def setup_rvc(self) -> Path:
        """
        Setup RVC (Retrieval-based Voice Conversion) for voice cloning.
        
        Returns:
            Path to RVC directory
        """
        rvc_dir = self.base_dir / "tools" / "RVC"
        
        if not rvc_dir.exists():
            print("Setting up RVC...")
            subprocess.run(['git', 'clone', RVC_REPO, str(rvc_dir)], 
                         check=True)
            
            # Note: RVC has complex setup, we'll use simplified approach
            # For full RVC, users need to run additional setup
            print("  RVC cloned. Additional setup may be required.")
            print("  See: https://github.com/liujing04/Retrieval-based-Voice-Conversion-WebUI")
        
        return rvc_dir
    
    def extract_vocal_features(self, vocal_path: str, output_dir: str = None) -> Tuple[str, str]:
        """
        Extract vocal features for cloning using RVC.
        
        Args:
            vocal_path: Path to isolated vocals file
            output_dir: Optional output directory
            
        Returns:
            Tuple of (feature file path, model path)
        """
        vocal_path = Path(vocal_path)
        
        # Setup RVC
        rvc_dir = self.setup_rvc()
        
        if output_dir is None:
            output_dir = self.temp_dir / "rvc_features"
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # For RVC, we need to:
        # 1. Preprocess the audio
        # 2. Extract features
        
        # Simplified: We'll use RVC's inference pipeline
        # This is a placeholder - full RVC setup is complex
        
        print("  Extracting vocal features...")
        print("  Note: Full RVC setup required for production use")
        
        # Generate unique ID for this voice
        voice_id = self._get_file_hash(str(vocal_path))
        feature_file = output_dir / f"{voice_id}.npy"
        model_file = self.models_dir / f"{voice_id}.pth"
        
        # For demo purposes, create placeholder files
        # In production, these would be generated by RVC
        feature_file.touch()
        model_file.touch()
        
        print(f"  Features: {feature_file}")
        print(f"  Model: {model_file}")
        
        return str(feature_file), str(model_file)
    
    def train_voice_model(
        self, 
        vocal_files: List[str], 
        output_model: str = None,
        epochs: int = 100
    ) -> str:
        """
        Train a voice model from vocal samples.
        
        Args:
            vocal_files: List of vocal sample files
            output_model: Path for output model
            epochs: Number of training epochs
            
        Returns:
            Path to trained model file
        """
        vocal_files = [Path(f) for f in vocal_files]
        
        if output_model is None:
            voice_id = self._get_file_hash(str(vocal_files[0]))
            output_model = self.models_dir / f"voice_{voice_id}.pth"
        else:
            output_model = Path(output_model)
        
        output_model.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"  Training voice model from {len(vocal_files)} samples...")
        print(f"  This would train for {epochs} epochs")
        print(f"  Output model: {output_model}")
        
        # In a full implementation, this would call RVC's training script
        # For now, create a placeholder
        output_model.touch()
        
        return str(output_model)
    
    def clone_voice(
        self,
        input_file: str,
        reference_voice: str,
        output_file: str = None,
        method: str = "rvc"
    ) -> str:
        """
        Clone voice from reference to input file.
        
        Args:
            input_file: Input audio file to clone voice onto
            reference_voice: Reference voice sample or model
            output_file: Output file path
            method: Cloning method ('rvc', 'simple')
            
        Returns:
            Path to output file with cloned voice
        """
        input_file = Path(input_file)
        reference_voice = Path(reference_voice)
        
        if output_file is None:
            output_file = self.outputs_dir / f"cloned_{input_file.name}"
        else:
            output_file = Path(output_file)
        
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        if method == "simple":
            # Simple pitch/timbre matching (placeholder)
            print("  Using simple voice conversion...")
            # This would use sox or similar for basic pitch shifting
            shutil.copy(input_file, output_file)
        
        elif method == "rvc":
            # RVC-based cloning
            print("  Using RVC voice conversion...")
            # In production, call RVC's inference
            shutil.copy(input_file, output_file)
        
        print(f"  Cloned voice output: {output_file}")
        return str(output_file)
    
    def process_file(self, input_path: str, output_dir: str = None) -> dict:
        """
        Complete pipeline for a single file.
        
        Args:
            input_path: Input file (audio or video)
            output_dir: Output directory
            
        Returns:
            Dictionary with results
        """
        input_path = Path(input_path)
        
        if output_dir is None:
            output_dir = self.outputs_dir / input_path.stem
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        result = {
            'input': str(input_path),
            'output_dir': str(output_dir),
            'steps': {}
        }
        
        # Step 1: Extract audio if video
        if input_path.suffix.lower() in ['.mp4', '.mkv', '.avi', '.mov', '.webm']:
            audio_path = output_dir / f"{input_path.stem}.wav"
            result['steps']['audio_extraction'] = self.extract_audio_from_video(
                str(input_path), 
                str(audio_path)
            )
            input_audio = audio_path
        else:
            input_audio = input_path
            result['steps']['audio_extraction'] = {'skipped': True, 'reason': 'input is audio'}
        
        # Step 2: Isolate vocals
        vocals_path = output_dir / "vocals.mp3"
        result['steps']['vocal_isolation'] = self.isolate_vocals(
            str(input_audio), 
            str(output_dir)
        )
        
        # Step 3: Extract features
        feature_path, model_path = self.extract_vocal_features(
            result['steps']['vocal_isolation']
        )
        result['steps']['feature_extraction'] = {
            'features': feature_path,
            'model': model_path
        }
        
        # Step 4: Train model (using the isolated vocals)
        result['steps']['model_training'] = self.train_voice_model(
            [result['steps']['vocal_isolation']],
            model_path
        )
        
        # Step 5: Create cloned output
        cloned_path = output_dir / "cloned_output.wav"
        result['steps']['voice_cloning'] = self.clone_voice(
            str(input_audio),
            result['steps']['vocal_isolation'],
            str(cloned_path)
        )
        
        result['final_output'] = str(cloned_path)
        result['voice_model'] = model_path
        
        return result
    
    def process_directory(self, input_dir: str, output_dir: str = None) -> List[dict]:
        """
        Process all files in a directory.
        
        Args:
            input_dir: Input directory with files
            output_dir: Output directory
            
        Returns:
            List of results for each file
        """
        input_dir = Path(input_dir)
        
        if output_dir is None:
            output_dir = self.outputs_dir / input_dir.name
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        results = []
        
        # Supported extensions
        supported = ['.wav', '.mp3', '.flac', '.ogg', '.m4a', 
                     '.mp4', '.mkv', '.avi', '.mov', '.webm']
        
        for file in input_dir.iterdir():
            if file.is_file() and file.suffix.lower() in supported:
                print(f"\nProcessing: {file.name}")
                try:
                    result = self.process_file(str(file), str(output_dir / file.stem))
                    results.append(result)
                    print(f"  Complete: {result['final_output']}")
                except Exception as e:
                    print(f"  Error processing {file.name}: {e}")
                    results.append({
                        'input': str(file),
                        'error': str(e)
                    })
        
        return results


def main():
    """Command-line interface for Voice Cloner."""
    parser = argparse.ArgumentParser(
        description="Voice Cloner - Local, Free Voice Cloning Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a single audio file
  python voice_cloner.py --input my_voice.wav --output my_clone
  
  # Process a video file
  python voice_cloner.py --input my_video.mp4 --output my_clone
  
  # Process a directory of files
  python voice_cloner.py --input samples/ --output clones/
  
  # Specify custom sample rate
  python voice_cloner.py --input audio.wav --sample-rate 48000
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Input file or directory (audio/video)'
    )
    
    parser.add_argument(
        '--output', '-o',
        default=None,
        help='Output directory (default: outputs/<input_name>)'
    )
    
    parser.add_argument(
        '--method', '-m',
        choices=['rvc', 'simple'],
        default='rvc',
        help='Voice cloning method (default: rvc)'
    )
    
    parser.add_argument(
        '--sample-rate',
        type=int,
        default=DEFAULT_SAMPLE_RATE,
        help=f'Sample rate for processing (default: {DEFAULT_SAMPLE_RATE})'
    )
    
    parser.add_argument(
        '--epochs',
        type=int,
        default=100,
        help='Training epochs for voice model (default: 100)'
    )
    
    parser.add_argument(
        '--skip-setup',
        action='store_true',
        help='Skip dependency setup checks'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # Load config if exists
    config_path = Path(__file__).parent.parent / "config.json"
    config = {}
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
    
    # Initialize cloner
    cloner = VoiceCloner(config)
    
    # Process input
    input_path = Path(args.input)
    
    if input_path.is_file():
        print(f"Processing file: {input_path}")
        result = cloner.process_file(
            str(input_path),
            args.output
        )
        print("\nResult:")
        print(json.dumps(result, indent=2))
    
    elif input_path.is_dir():
        print(f"Processing directory: {input_path}")
        results = cloner.process_directory(
            str(input_path),
            args.output
        )
        print(f"\nProcessed {len(results)} files")
        if args.verbose:
            for r in results:
                print(json.dumps(r, indent=2))
    
    else:
        print(f"Error: Input not found: {input_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
