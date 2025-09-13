#!/usr/bin/env python3

import pytest
from context_test import get_test_brain
from select_themes import select_themes, UniversalTheme


def test_time_travel_story_themes():
    """Test theme selection for a time travel story"""
    brain = get_test_brain()
    
    description = "a novel about a girl scientist working in a lab who through some accident gets sent back to ancient rome"
    plot_type = "Voyage and Return"
    
    result = select_themes(brain, description, plot_type)
    
    # Should select themes relevant to time travel, science, and cultural exchange
    expected_themes = {
        UniversalTheme.TIME_AND_CHANGE,
        UniversalTheme.CULTURAL_EXCHANGE, 
        UniversalTheme.SCIENCE_AND_ETHICS,
        UniversalTheme.IDENTITY_AND_SELF,
        UniversalTheme.ISOLATION_AND_BELONGING
    }
    
    # Check that at least one expected theme is present
    assert len(set(result.themes) & expected_themes) >= 1
    assert len(result.themes) >= 2
    assert len(result.themes) <= 3
    assert len(result.reasoning) > 20
    
    print(f"Selected themes: {[theme.value for theme in result.themes]}")
    print(f"Reasoning: {result.reasoning}")


def test_hero_quest_themes():
    """Test theme selection for a classic hero's quest"""
    brain = get_test_brain()
    
    description = "A young farmboy discovers he has magical powers and must defeat the dark wizard to save his kingdom"
    plot_type = "The Quest"
    
    result = select_themes(brain, description, plot_type)
    
    # Should select themes relevant to heroes and quests
    expected_themes = {
        UniversalTheme.GOOD_VS_EVIL,
        UniversalTheme.COMING_OF_AGE,
        UniversalTheme.COURAGE,
        UniversalTheme.SACRIFICE
    }
    
    # Check that at least one expected theme is present
    assert len(set(result.themes) & expected_themes) >= 1
    assert len(result.themes) >= 2
    assert len(result.themes) <= 3
    assert len(result.reasoning) > 20
    
    print(f"Selected themes: {[theme.value for theme in result.themes]}")


def test_romance_themes():
    """Test theme selection for a romance story"""
    brain = get_test_brain()
    
    description = "Two people from different social classes fall in love despite family opposition"
    plot_type = "Comedy"
    
    result = select_themes(brain, description, plot_type)
    
    # Should select themes relevant to love and social barriers
    expected_themes = {
        UniversalTheme.LOVE_AND_RELATIONSHIPS,
        UniversalTheme.FAMILY,
        UniversalTheme.FREEDOM_VS_OPPRESSION,
        UniversalTheme.TRADITION_VS_PROGRESS
    }
    
    # Check that at least one expected theme is present
    assert len(set(result.themes) & expected_themes) >= 1
    assert len(result.themes) >= 2
    assert len(result.themes) <= 3
    assert len(result.reasoning) > 20
    
    print(f"Selected themes: {[theme.value for theme in result.themes]}")


