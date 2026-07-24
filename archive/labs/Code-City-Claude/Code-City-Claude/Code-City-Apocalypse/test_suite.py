#!/usr/bin/env python3
import sys
sys.path.append('/data/data/com.termux/files/home/code_city')

print("Testing imports...")
try:
    from obelisk.lib.ai.gemini_wrapper import GeminiWrapper
    print("  ✓ Gemini")
except Exception as e:
    print(f"  ✗ Gemini: {e}")

try:
    from obelisk.boardroom.vertical_ai import VerticalAI
    print("  ✓ Vertical AI")
except Exception as e:
    print(f"  ✗ Vertical AI: {e}")

try:
    from obelisk.rapper.beat_generator import BeatGenerator
    print("  ✓ Beat Gen")
except Exception as e:
    print(f"  ✗ Beat Gen: {e}")

print("\nTesting beat creation...")
try:
    from obelisk.rapper.beat_generator import BeatGenerator
    gen = BeatGenerator()
    gen.create_beat().save('/tmp/test.mid')
    print("  ✓ Beat created")
except Exception as e:
    print(f"  ✗ Failed: {e}")

print("\n✓ Tests complete")
print("\nNext: nano shared/config/config.yaml (add API key)")
