#!/usr/bin/env python3

import pytest
from context_test import get_test_brain
from break_into_sections import break_into_sections
from break_into_chapters import Chapter


def test_break_chapter_into_sections():
    """Test breaking a chapter into sections"""
    brain = get_test_brain()
    
    # Create a sample chapter
    chapter = Chapter(
        number=1,
        title="The Investigation Begins",
        opening_situation="Detective Sarah is at her desk reviewing cold cases when a new lead arrives.",
        chapter_goal="Establish the mystery and begin the investigation that will drive the story.",
        closing_situation="Sarah has gathered initial clues and identified the main suspects to investigate.",
        key_events=[
            "Sarah receives a mysterious phone call about the old case",
            "She visits the crime scene and discovers new evidence", 
            "Sarah interviews the victim's family and learns about hidden secrets",
            "A threatening message warns her to stop investigating"
        ]
    )
    
    # Break into 3 sections
    result = break_into_sections(brain, chapter, 3)
    
    # Check that we got exactly 3 sections
    assert len(result.sections) == 3
    
    # Check that sections are numbered correctly
    for i, section in enumerate(result.sections):
        assert section.number == i + 1
        assert len(section.goal) > 0
        assert len(section.key_events) > 0
    
    print(f"✅ Chapter broken into {len(result.sections)} sections:")
    for section in result.sections:
        print(f"  Section {section.number}: {section.goal}")


def test_single_section_chapter():
    """Test breaking a chapter into just 1 section"""
    brain = get_test_brain()
    
    chapter = Chapter(
        number=1,
        title="Short Chapter",
        opening_situation="The protagonist faces the final challenge.",
        chapter_goal="Resolve the central conflict.",
        closing_situation="The story concludes with resolution.",
        key_events=["Final confrontation", "Resolution achieved"]
    )
    
    result = break_into_sections(brain, chapter, 1)
    
    assert len(result.sections) == 1
    assert result.sections[0].number == 1
    
    print(f"✅ Chapter broken into 1 section successfully")


if __name__ == "__main__":
    test_break_chapter_into_sections()
    test_single_section_chapter()