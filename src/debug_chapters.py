#!/usr/bin/env python3

from brain import Brain
from dazllm import Llm
from break_into_chapters import break_into_chapters
import json

def debug_break_into_chapters():
    """Debug the break_into_chapters function to see what's happening"""
    
    # Set up the brain
    llm = Llm.model_named("ollama:llama3.2:latest")
    brain = Brain(llm)
    
    sample_outline = """
    This is a complete story that follows a character through multiple phases.
    
    Phase 1: The character discovers a problem and begins to investigate.
    Phase 2: The character encounters obstacles and challenges.
    Phase 3: The character overcomes the challenges and resolves the problem.
    
    Each phase has its own arc and development, building to a satisfying conclusion.
    """
    
    print("Testing break_into_chapters with 3 chapters, 1 section each...")
    print("=" * 60)
    
    result = break_into_chapters(brain, sample_outline, 3, 1)
    
    print(f"Generated {len(result.chapters)} chapters:")
    print(json.dumps(result.model_dump(), indent=2))
    
    if len(result.chapters) != 3:
        print(f"\n❌ ERROR: Expected 3 chapters, got {len(result.chapters)}")
    else:
        print("\n✅ SUCCESS: Got 3 chapters as expected")

if __name__ == "__main__":
    debug_break_into_chapters()