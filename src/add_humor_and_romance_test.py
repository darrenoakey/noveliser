#!/usr/bin/env python3

import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from context_test import get_test_brain
from add_humor_and_romance import add_humor_and_romance


def test_add_humor_and_romance_to_serious_outline():
    """Test adding humor and romance to a serious outline"""
    brain = get_test_brain()
    
    serious_outline = """
    ACT 1: Dr. Elena Chen discovers a dangerous virus outbreak in her lab.
    The virus threatens to spread globally. She must work against time.
    
    ACT 2: Elena teams with epidemiologist Dr. Marcus Wade to find a cure.
    They face resistance from government officials who want to weaponize the virus.
    
    ACT 3: Elena and Marcus develop an antidote but must risk their lives to deploy it.
    They succeed in stopping the outbreak and expose the conspiracy.
    """
    
    result = add_humor_and_romance(brain, serious_outline)
    
    # Check that enhanced outline exists and is longer
    assert len(result.outline) >= len(serious_outline)
    assert result.outline != serious_outline
    
    # Check that humor and romance elements were identified
    assert len(result.humor_elements) >= 1
    assert len(result.romance_elements) >= 1
    
    # Should still contain the core story
    assert "virus" in result.outline.lower() or "outbreak" in result.outline.lower()
    assert "Elena" in result.outline or "scientist" in result.outline.lower()
    
    print(f"Humor elements: {result.humor_elements}")
    print(f"Romance elements: {result.romance_elements}")


def test_add_humor_and_romance_preserves_core_story():
    """Test that enhancement preserves the core narrative"""
    brain = get_test_brain()
    
    original_outline = """
    A detective investigates a series of art thefts in Paris.
    The thief leaves cryptic clues at each scene.
    The detective discovers the thief is stealing to expose forgeries.
    They must work together to catch the real criminals.
    """
    
    result = add_humor_and_romance(brain, original_outline)
    
    # Core elements should still be present
    assert "detective" in result.outline.lower()
    assert "thief" in result.outline.lower() or "theft" in result.outline.lower()
    assert "Paris" in result.outline or "art" in result.outline.lower()
    
    # Should have added elements
    assert len(result.humor_elements) > 0
    assert len(result.romance_elements) > 0
    
    print(f"Enhanced outline length: {len(result.outline)}")
    print(f"Original length: {len(original_outline)}")