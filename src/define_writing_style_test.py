#!/usr/bin/env python3

import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from context_test import get_test_brain
from define_writing_style import define_writing_style


def test_define_writing_style_for_thriller():
    """Test defining writing style for a thriller"""
    brain = get_test_brain()
    
    outline = """
    A cybersecurity expert discovers a conspiracy within their own company.
    They must gather evidence while avoiding detection by corporate security.
    The stakes escalate when they realize the conspiracy involves national security.
    Racing against time, they must expose the truth before becoming a victim.
    """
    
    themes = ["Trust and Betrayal", "Technology and Privacy", "Justice"]
    
    result = define_writing_style(brain, outline, themes)
    
    # Check all required fields are present
    assert result.style_description
    assert result.tone
    assert result.voice
    assert result.pacing
    assert len(result.examples) >= 2
    
    # Style should be appropriate for thriller
    assert any(word in result.tone.lower() or word in result.pacing.lower() 
              for word in ["tense", "suspense", "fast", "urgent", "dramatic"])
    
    print(f"Tone: {result.tone}")
    print(f"Voice: {result.voice}")
    print(f"Pacing: {result.pacing}")
    print(f"Examples: {result.examples}")


def test_define_writing_style_for_romance():
    """Test defining writing style for a romance"""
    brain = get_test_brain()
    
    outline = """
    Two rival bookshop owners compete for customers in a small town.
    Their rivalry turns to friendship as they face a common threat.
    Slowly, they realize their feelings run deeper than friendship.
    They must overcome their pride to find love together.
    """
    
    themes = ["Love", "Pride and Prejudice", "Community"]
    
    result = define_writing_style(brain, outline, themes)
    
    # Check all fields present
    assert result.style_description
    assert result.tone
    assert result.voice
    assert result.pacing
    assert len(result.examples) >= 2 and len(result.examples) <= 3
    
    # Style should be appropriate for romance
    style_text = (result.style_description + result.tone).lower()
    assert any(word in style_text for word in ["warm", "emotional", "intimate", "romantic", "heartfelt"])
    
    print(f"Style description: {result.style_description[:100]}...")


def test_writing_style_examples_are_actual_sentences():
    """Test that example sentences are properly formatted"""
    brain = get_test_brain()
    
    outline = "A simple story about a journey."
    themes = ["Adventure", "Discovery"]
    
    result = define_writing_style(brain, outline, themes)
    
    # Examples should be actual sentences
    for example in result.examples:
        assert len(example) > 10  # Not just a word or two
        assert example[0].isupper() or example[0] == '"'  # Starts with capital or quote
        assert example.strip()[-1] in '.!?"'  # Ends with punctuation
    
    print(f"Example sentences: {result.examples}")