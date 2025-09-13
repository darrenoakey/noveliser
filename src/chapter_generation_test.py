#!/usr/bin/env python3

import json
from pathlib import Path
from brain import Brain
from break_into_chapters import break_into_chapters, ChapterPlan
from context_test import get_test_brain


def test_multiple_chapters_generation():
    """Test that break_into_chapters generates the correct number of chapters"""
    brain = get_test_brain()
    
    test_cases = [
        (1, 1, "Single chapter, single section"),
        (3, 2, "Three chapters, two sections each"),
        (5, 1, "Five chapters, one section each"),
    ]
    
    sample_outline = """
    This is a story about a detective solving a complex case. 
    It begins with the discovery of a crime, proceeds through investigation,
    encounters various suspects and red herrings, builds to a confrontation 
    with the true culprit, and concludes with justice being served.
    The detective also undergoes personal growth throughout the journey.
    """
    
    for num_chapters, sections_per_chapter, description in test_cases:
        print(f"\nTesting: {description}")
        print(f"Requesting: {num_chapters} chapters, {sections_per_chapter} sections per chapter")
        
        result = break_into_chapters(brain, sample_outline, num_chapters, sections_per_chapter)
        
        print(f"Generated: {len(result.chapters)} chapters")
        
        # Check the number of chapters
        assert len(result.chapters) == num_chapters, f"Expected {num_chapters} chapters, got {len(result.chapters)}"
        
        # Check each chapter has the correct number of sections
        for i, chapter in enumerate(result.chapters):
            print(f"  Chapter {i+1}: {len(chapter.sections)} sections")
            assert len(chapter.sections) == sections_per_chapter, f"Chapter {i+1}: Expected {sections_per_chapter} sections, got {len(chapter.sections)}"
            
            # Verify numbering
            assert chapter.number == i + 1, f"Chapter numbering incorrect"
            for j, section in enumerate(chapter.sections):
                assert section.number == j + 1, f"Section numbering incorrect in chapter {i+1}"
        
        print(f"✅ Test passed for {description}")


def inspect_recent_generation():
    """Inspect a recent novel generation to see what happened"""
    # Look for the most recent novel directory
    output_dir = Path("/Volumes/T9/darrenoakey/src/noveliser/output")
    
    # Find directories with break_into_chapters.json
    novel_dirs = [d for d in output_dir.iterdir() if d.is_dir() and (d / "break_into_chapters.json").exists()]
    
    if not novel_dirs:
        print("No novel directories found with break_into_chapters.json")
        return
    
    # Sort by modification time and take the most recent
    recent_dir = max(novel_dirs, key=lambda d: (d / "break_into_chapters.json").stat().st_mtime)
    
    print(f"\nInspecting: {recent_dir.name}")
    
    # Read the break_into_chapters.json
    with open(recent_dir / "break_into_chapters.json", 'r') as f:
        data = json.load(f)
    
    chapters = data.get('chapters', [])
    print(f"Found {len(chapters)} chapters in the file")
    
    for chapter in chapters:
        sections = chapter.get('sections', [])
        print(f"  Chapter {chapter.get('number', '?')}: '{chapter.get('title', 'Untitled')}' - {len(sections)} sections")
    
    # Check what sections were actually written
    written_sections = []
    for f in recent_dir.iterdir():
        if f.name.startswith("write_chapter_") and f.name.endswith(".json"):
            written_sections.append(f.name)
    
    print(f"\nActually written section files: {sorted(written_sections)}")


if __name__ == "__main__":
    print("Testing chapter generation...")
    # First inspect what's happening
    inspect_recent_generation()
    
    # Then run the actual test
    test_multiple_chapters_generation()