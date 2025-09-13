#!/usr/bin/env python3

"""
Quick test to verify that multiple chapters are actually written
when enough time is given.
"""

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from src.noveliser import write_novel
from pathlib import Path
import tempfile

def test_multiple_chapters():
    """Test that multiple chapters are actually written"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        output_dir = Path(temp_dir)
        
        # Use a faster model and minimal chapters/sections
        print("Testing with 2 chapters, 1 section each...")
        
        result = write_novel(
            description="A very simple test story",
            output_dir=output_dir,
            model_name="ollama:llama3.2:latest",
            num_chapters=2,
            sections_per_chapter=1,
            author="Test Author"
        )
        
        print(f"\nResult: {result}")
        
        # Check what files were created
        novel_dirs = [d for d in output_dir.iterdir() if d.is_dir()]
        if novel_dirs:
            novel_dir = novel_dirs[0]
            print(f"\nNovel directory: {novel_dir.name}")
            
            # Count chapter files
            chapter_files = list(novel_dir.glob("write_chapter_*.json"))
            print(f"Chapter files found: {len(chapter_files)}")
            for cf in sorted(chapter_files):
                print(f"  - {cf.name}")
            
            # Check break_into_chapters
            break_file = novel_dir / "break_into_chapters.json"
            if break_file.exists():
                import json
                with open(break_file) as f:
                    data = json.load(f)
                    chapters = data.get('chapters', [])
                    print(f"\nPlanned chapters: {len(chapters)}")
                    for ch in chapters:
                        print(f"  - Chapter {ch['number']}: {ch['title']} ({len(ch.get('sections', []))} sections)")
            
            # Verify
            if len(chapter_files) == 2:
                print("\n✅ SUCCESS: Both chapters were written!")
            else:
                print(f"\n❌ ISSUE: Expected 2 chapter files, found {len(chapter_files)}")
        
        return result

if __name__ == "__main__":
    test_multiple_chapters()