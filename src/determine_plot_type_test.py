#!/usr/bin/env python3

import pytest
from context_test import get_test_brain
from determine_plot_type import determine_plot_type, PlotTypeEnum


def test_voyage_and_return_plot():
    """Test that a time travel story is correctly identified as Voyage and Return"""
    brain = get_test_brain()
    
    description = "a novel about a girl scientist working in a lab who through some accident gets sent back to ancient rome"
    
    result = determine_plot_type(brain, description)
    
    assert result.plot_type == PlotTypeEnum.VOYAGE_AND_RETURN
    assert "time" in result.reasoning.lower() or "travel" in result.reasoning.lower() or "journey" in result.reasoning.lower()
    assert len(result.reasoning) > 20  # Should have substantial reasoning


def test_quest_plot():
    """Test that a typical quest story is correctly identified"""
    brain = get_test_brain()
    
    description = "A young hero must find the three magical artifacts to defeat the dark lord and save the kingdom"
    
    result = determine_plot_type(brain, description)
    
    assert result.plot_type == PlotTypeEnum.THE_QUEST
    assert "quest" in result.reasoning.lower() or "journey" in result.reasoning.lower() or "find" in result.reasoning.lower()
    assert len(result.reasoning) > 20


def test_overcoming_monster_plot():
    """Test that a monster-fighting story is correctly identified"""
    brain = get_test_brain()
    
    description = "A small town is terrorized by a giant dragon. A brave warrior must defeat it to save the people."
    
    result = determine_plot_type(brain, description)
    
    assert result.plot_type == PlotTypeEnum.OVERCOMING_THE_MONSTER
    assert "monster" in result.reasoning.lower() or "dragon" in result.reasoning.lower() or "defeat" in result.reasoning.lower()
    assert len(result.reasoning) > 20


