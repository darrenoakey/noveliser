#!/usr/bin/env python3

import pytest
from context_test import get_test_brain
from break_into_chapters import break_into_chapters
from create_characters import Character, CharacterRole


def test_break_into_chapters_basic():
    """Test breaking an outline into chapters with characters"""
    brain = get_test_brain()
    
    outline = """
    ACT 1: Introduction
    The protagonist discovers their calling and faces initial challenges.
    They meet allies and learn about the main conflict.
    
    ACT 2: Development  
    The protagonist faces escalating challenges and setbacks.
    They grow stronger through trials and discover hidden truths.
    A major crisis forces them to question everything.
    
    ACT 3: Resolution
    The protagonist confronts the main antagonist.
    They use everything they've learned to overcome the final challenge.
    The world is changed by their actions.
    """
    
    characters = [
        Character(
            name="Alex",
            biography="A young hero discovering their destiny",
            role=CharacterRole.PROTAGONIST,
            traits=["brave", "determined", "curious"]
        ),
        Character(
            name="Mentor",
            biography="An wise guide who helps the hero",
            role=CharacterRole.SUPPORTING,
            traits=["wise", "patient", "experienced"]
        ),
        Character(
            name="Dark Lord",
            biography="The main antagonist threatening the world",
            role=CharacterRole.ANTAGONIST,
            traits=["powerful", "evil", "cunning"]
        )
    ]
    
    result = break_into_chapters(brain, outline, characters, 
                                ["Adventure", "Growth"], "Quest", 
                                "Contains humor and romance elements", num_chapters=3)
    
    # Check structure
    assert len(result.chapters) == 3
    for i, chapter in enumerate(result.chapters):
        assert chapter.number == i + 1
        assert len(chapter.title) > 0
        assert len(chapter.opening_situation) > 0
        assert len(chapter.chapter_goal) > 0
        assert len(chapter.closing_situation) > 0
        assert len(chapter.key_events) > 0
    
    print(f"Generated {len(result.chapters)} chapters:")
    for chapter in result.chapters:
        print(f"  Chapter {chapter.number}: {chapter.title}")
        print(f"    Goal: {chapter.chapter_goal}")


def test_single_chapter_story():
    """Test creating a single chapter story"""
    brain = get_test_brain()
    
    outline = """
    A detective solves a murder mystery in one day.
    They gather clues, interview suspects, and reveal the killer.
    """
    
    characters = [
        Character(
            name="Detective Smith",
            biography="An experienced investigator",
            role=CharacterRole.PROTAGONIST,
            traits=["observant", "logical", "persistent"]
        )
    ]
    
    result = break_into_chapters(brain, outline, characters,
                                ["Mystery", "Justice"], "Crime", 
                                "Detective story with resolution", num_chapters=1)
    
    assert len(result.chapters) == 1
    chapter = result.chapters[0]
    assert chapter.number == 1
    assert len(chapter.title) > 0
    assert "detective" in chapter.opening_situation.lower() or "investigat" in chapter.opening_situation.lower()
    
    print(f"Single chapter: {chapter.title}")
    print(f"Opening: {chapter.opening_situation}")
    print(f"Closing: {chapter.closing_situation}")


if __name__ == "__main__":
    test_break_into_chapters_basic()
    test_single_chapter_story()