#!/usr/bin/env python3

import pytest
from context_test import get_test_brain
from create_characters import create_characters, CharacterRole


def test_time_travel_story_characters():
    """Test character creation for a time travel story"""
    brain = get_test_brain()
    
    description = "a novel about a girl scientist working in a lab who through some accident gets sent back to ancient rome"
    plot_type = "Voyage and Return"
    themes = ["Science and Ethics", "Cultural Exchange", "Identity and Self-Discovery"]
    
    result = create_characters(brain, description, plot_type, themes)
    
    # Check that we have multiple characters
    assert len(result.characters) >= 3
    assert len(result.characters) <= 8
    
    # Check that at least one character is the protagonist
    protagonist_count = sum(1 for char in result.characters if char.role == CharacterRole.PROTAGONIST)
    assert protagonist_count >= 1
    
    # Check that all characters have required fields
    for character in result.characters:
        assert len(character.name) > 0
        assert len(character.biography) > 20  # Should be substantial
        assert character.role in CharacterRole
        assert len(character.traits) >= 1
    
    print(f"Created {len(result.characters)} characters:")
    for char in result.characters:
        print(f"  - {char.name} ({char.role.value}): {char.biography[:100]}...")


def test_fantasy_quest_characters():
    """Test character creation for a fantasy quest"""
    brain = get_test_brain()
    
    description = "A young farmboy discovers he has magical powers and must defeat the dark wizard to save his kingdom"
    plot_type = "The Quest"
    themes = ["Good vs Evil", "Coming of Age", "Courage"]
    
    result = create_characters(brain, description, plot_type, themes)
    
    # Check basic requirements
    assert len(result.characters) >= 3
    assert len(result.characters) <= 8
    
    # Should have protagonist and antagonist for this type of story
    roles = [char.role for char in result.characters]
    assert CharacterRole.PROTAGONIST in roles
    assert CharacterRole.ANTAGONIST in roles
    
    print(f"Created {len(result.characters)} fantasy characters:")
    for char in result.characters:
        print(f"  - {char.name} ({char.role.value})")


def test_romance_characters():
    """Test character creation for a romance story"""
    brain = get_test_brain()
    
    description = "Two people from different social classes fall in love despite family opposition"
    plot_type = "Comedy"
    themes = ["Love and Relationships", "Family", "Freedom vs Oppression"]
    
    result = create_characters(brain, description, plot_type, themes)
    
    # Check basic requirements
    assert len(result.characters) >= 3
    assert len(result.characters) <= 8
    
    # Should have at least protagonist (could have dual protagonists for romance)
    protagonist_count = sum(1 for char in result.characters if char.role == CharacterRole.PROTAGONIST)
    assert protagonist_count >= 1
    
    print(f"Created {len(result.characters)} romance characters:")
    for char in result.characters:
        print(f"  - {char.name} ({char.role.value})")


