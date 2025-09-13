#!/usr/bin/env python3

import tempfile
from pathlib import Path
from noveliser import write_novel
import json


def test_multi_chapter_novel():
    """Integration test that generates a novel with 2 chapters, 2 sections each"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        output_dir = Path(temp_dir)
        
        print("=" * 60)
        print("INTEGRATION TEST: 2 chapters, 2 sections each")
        print("=" * 60)
        
        try:
            result = write_novel(
                description="A simple detective story about solving a mystery",
                output_dir=output_dir,
                model_name="ollama:llama3.2:latest",
                num_chapters=2,
                sections_per_chapter=2,
                author="Test Author"
            )
            
            print(f"\nGeneration completed successfully!")
            print(f"EPUB: {result.epub_path}")
            print(f"Cover: {result.cover_path}")
            
            # Find the novel directory
            novel_dirs = [d for d in output_dir.iterdir() if d.is_dir()]
            if not novel_dirs:
                raise Exception("No novel directory found")
            
            novel_dir = novel_dirs[0]
            print(f"\nNovel directory: {novel_dir.name}")
            
            # Check break_into_N_chapters.json 
            break_files = list(novel_dir.glob("break_into_*_chapters.json"))
            if not break_files:
                raise Exception("No break_into_chapters file found")
            break_file = break_files[0]
            if not break_file.exists():
                raise Exception("break_into_chapters.json not found")
            
            with open(break_file) as f:
                chapters_data = json.load(f)
            
            chapters = chapters_data.get('chapters', [])
            print(f"\nPlanned chapters: {len(chapters)}")
            
            if len(chapters) != 2:
                raise Exception(f"Expected 2 chapters in plan, got {len(chapters)}")
            
            for ch in chapters:
                sections = ch.get('sections', [])
                print(f"  Chapter {ch['number']}: '{ch['title']}' - {len(sections)} sections")
                if len(sections) != 2:
                    raise Exception(f"Chapter {ch['number']} has {len(sections)} sections, expected 2")
            
            # Check that all section files were written
            expected_files = [
                "write_chapter_1,_section_1.json",
                "write_chapter_1,_section_2.json", 
                "write_chapter_2,_section_1.json",
                "write_chapter_2,_section_2.json"
            ]
            
            print(f"\nChecking for section files...")
            missing_files = []
            for expected_file in expected_files:
                file_path = novel_dir / expected_file
                if file_path.exists():
                    print(f"  ✓ {expected_file}")
                else:
                    print(f"  ✗ {expected_file} - MISSING")
                    missing_files.append(expected_file)
            
            if missing_files:
                print(f"\nFAILED: Missing section files: {missing_files}")
                return False
            
            print(f"\n✅ SUCCESS: Novel generated with 2 chapters, 2 sections each!")
            return True
            
        except Exception as e:
            print(f"\n❌ FAILED: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == "__main__":
    success = test_multi_chapter_novel()
    exit(0 if success else 1)