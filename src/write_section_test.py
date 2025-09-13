#!/usr/bin/env python3

import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from context_test import get_test_brain
from write_section import write_section
from break_into_chapters import Chapter, Section
from define_writing_style import WritingStyle


def test_write_section_basic():
    """Test writing a basic section"""
    brain = get_test_brain()
    
    # Create test data
    chapter = Chapter(
        number=1,
        title="The Beginning",
        summary="The story starts",
        sections=[
            Section(number=1, goal="Introduce the protagonist", key_events="Character wakes up, discovers something strange")
        ]
    )
    
    section = chapter.sections[0]
    
    writing_style = WritingStyle(
        style_description="Clear, engaging narrative style",
        tone="mysterious",
        voice="third-person limited",
        pacing="measured",
        examples=["The morning light filtered through the curtains.", "She knew something was wrong."]
    )
    
    result = write_section(brain, chapter, section, "", [], writing_style)
    
    # Check that we got text
    assert len(result.text) > 500  # Should be substantial
    assert isinstance(result.new_facts, list)
    
    # Should mention the chapter/section goals
    text_lower = result.text.lower()
    assert any(word in text_lower for word in ["wake", "woke", "morning", "discover", "strange"])
    
    print(f"Section length: {len(result.text)} characters")
    print(f"New facts: {len(result.new_facts)}")


def test_write_section_with_context():
    """Test writing a section with previous text and facts"""
    brain = get_test_brain()
    
    chapter = Chapter(
        number=2,
        title="The Investigation", 
        summary="Character investigates further",
        sections=[
            Section(number=1, goal="Character searches for clues", key_events="Finds a mysterious letter")
        ]
    )
    
    section = chapter.sections[0]
    
    writing_style = WritingStyle(
        style_description="Suspenseful mystery style",
        tone="tense", 
        voice="third-person",
        pacing="building tension",
        examples=["The silence was deafening.", "Every shadow seemed to hide a secret."]
    )
    
    previous_text = "Sarah had always been curious, but this was different. The strange sound from last night still echoed in her mind."
    established_facts = ["Sarah is the protagonist", "She heard a strange sound last night", "She lives alone"]
    
    result = write_section(brain, chapter, section, previous_text, established_facts, writing_style)
    
    # Should reference previous context
    assert len(result.text) > 500
    assert "Sarah" in result.text or "she" in result.text.lower()
    
    # Should mention searching/investigation
    text_lower = result.text.lower()
    assert any(word in text_lower for word in ["search", "look", "find", "letter", "clue"])
    
    print(f"Continued section length: {len(result.text)} characters")