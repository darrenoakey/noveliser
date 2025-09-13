#!/usr/bin/env python3

import pytest
from context_test import get_test_brain
from create_outline import create_outline
from create_characters import Character, CharacterRole


def test_time_travel_outline():
    """Test outline creation for a time travel story"""
    brain = get_test_brain()
    
    description = "a novel about a girl scientist working in a lab who through some accident gets sent back to ancient rome"
    plot_type = "Voyage and Return"
    themes = ["Science and Ethics", "Cultural Exchange", "Identity and Self-Discovery"]
    
    # Create sample characters
    characters = [
        Character(
            name="Dr. Elara Quinn",
            biography="A 28-year-old biophysicist working in quantum mechanics research",
            role=CharacterRole.PROTAGONIST,
            traits=["brilliant", "curious", "adaptable"]
        ),
        Character(
            name="Marcus Aurelius Drusus", 
            biography="A Roman senator and philosopher interested in natural phenomena",
            role=CharacterRole.SUPPORTING,
            traits=["wise", "scholarly", "diplomatic"]
        ),
        Character(
            name="Tiberius Valerius",
            biography="A Roman general suspicious of foreign influences",
            role=CharacterRole.ANTAGONIST,
            traits=["traditional", "suspicious", "powerful"]
        )
    ]
    
    result = create_outline(brain, description, plot_type, themes, characters, 10, 10)
    
    # Check that outline is substantial
    assert len(result.outline) > 200
    assert "Elara" in result.outline or "scientist" in result.outline.lower()
    assert "Rome" in result.outline or "roman" in result.outline.lower()
    
    # Should contain plot structure elements
    outline_lower = result.outline.lower()
    plot_elements = ["beginning", "conflict", "resolution", "journey", "return", "discovery"]
    assert any(element in outline_lower for element in plot_elements)
    
    print(f"Outline length: {len(result.outline)} characters")
    print(f"Outline preview: {result.outline[:200]}...")


def test_fantasy_quest_outline():
    """Test outline creation for a fantasy quest"""
    brain = get_test_brain()
    
    description = "A young farmboy discovers he has magical powers and must defeat the dark wizard to save his kingdom"
    plot_type = "The Quest"
    themes = ["Good vs Evil", "Coming of Age", "Courage"]
    
    characters = [
        Character(
            name="Tomas",
            biography="A 16-year-old farmboy with latent magical abilities",
            role=CharacterRole.PROTAGONIST,
            traits=["brave", "naive", "determined"]
        ),
        Character(
            name="Lord Malakar",
            biography="An ancient wizard who seeks to rule the kingdom with dark magic",
            role=CharacterRole.ANTAGONIST,
            traits=["cunning", "powerful", "ruthless"]
        )
    ]
    
    result = create_outline(brain, description, plot_type, themes, characters, 10, 10)
    
    assert len(result.outline) > 200
    assert "Tomas" in result.outline or "farmboy" in result.outline.lower()
    assert "magic" in result.outline.lower() or "wizard" in result.outline.lower()
    
    print(f"Fantasy outline created: {len(result.outline)} characters")


