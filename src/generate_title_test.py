#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.expanduser('~/src/dazllm'))
from dazllm import Llm
from brain import Brain
from generate_title import generate_title


def test_title_generation():
    """Test basic title generation"""
    llm = Llm("ollama:gpt-oss:20b")
    brain = Brain(llm)
    
    description = "a novel about a girl scientist working in a lab who through some accident gets sent back to ancient rome"
    
    result = generate_title(brain, description)
    
    assert result.title
    assert len(result.title) > 0
    assert isinstance(result.title, str)
    print(f"✅ Title generated: {result.title}")


def test_title_generation_short_description():
    """Test title generation with shorter description"""
    llm = Llm("ollama:gpt-oss:20b")
    brain = Brain(llm)
    
    description = "A romantic comedy about two rivals"
    
    result = generate_title(brain, description)
    
    assert result.title
    assert len(result.title) > 0
    print(f"✅ Short description title: {result.title}")