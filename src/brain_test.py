#!/usr/bin/env python3

import sys
import os
from pathlib import Path
sys.path.append(os.path.expanduser('~/src/dazllm'))
from dazllm import Llm
from brain import Brain
from pydantic import BaseModel


class TestResponse(BaseModel):
    text: str
    count: int


def test_brain_chat():
    """Test basic brain chat functionality"""
    llm = Llm("ollama:gpt-oss:20b")
    brain = Brain(llm)
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say hello in exactly 3 words."}
    ]
    
    response = brain.chat(messages)
    
    assert isinstance(response, str)
    assert len(response) > 0
    print(f"✅ Brain chat response: {response}")


def test_brain_structured_chat():
    """Test brain structured chat with Pydantic models"""
    llm = Llm("ollama:gpt-oss:20b")
    brain = Brain(llm)
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant that responds in JSON."},
        {"role": "user", "content": "Create a simple test response with text 'Hello World' and count 42."}
    ]
    
    response = brain.chat_structured(messages, TestResponse)
    
    assert isinstance(response, TestResponse)
    assert hasattr(response, 'text')
    assert hasattr(response, 'count')
    print(f"✅ Structured response: text='{response.text}', count={response.count}")


def test_brain_caching():
    """Test that brain caches identical requests"""
    llm = Llm("ollama:gpt-oss:20b")
    brain = Brain(llm)
    
    messages = [
        {"role": "system", "content": "You are a consistent assistant."},
        {"role": "user", "content": "Return exactly the word 'CACHED' with no other text."}
    ]
    
    # First call
    response1 = brain.chat(messages)
    
    # Second call - should be cached
    response2 = brain.chat(messages)
    
    # Responses should be identical due to caching
    assert response1 == response2
    print(f"✅ Caching works: '{response1}' == '{response2}'")