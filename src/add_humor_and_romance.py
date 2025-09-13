#!/usr/bin/env python3

from pydantic import BaseModel
from brain import Brain


class EnhancedOutline(BaseModel):
    outline: str
    humor_elements: list[str]
    romance_elements: list[str]


class ElementsList(BaseModel):
    elements: list[str]


def add_humor_and_romance(brain: Brain, outline: str) -> EnhancedOutline:
    """Review and enhance outline with humor and romance elements."""
    
    messages = [
        {"role": "system", "content": "You are a story editor specializing in adding depth through humor and romance."},
        {"role": "user", "content": f"""Review this outline and enhance it with subtle humor and romance:

{outline}

Add:
1. At least one humorous subplot or character quirk
2. A romantic element (doesn't have to be the main focus)
3. Moments of levity to balance any serious themes

Return the enhanced outline while preserving the core story."""}
    ]
    
    enhanced_text = brain.chat(messages)
    
    # Extract what was added
    humor_prompt = [
        {"role": "system", "content": "You extract humor elements from story outlines."},
        {"role": "user", "content": f"List the humor elements in this outline:\n{enhanced_text}\n\nProvide a list of 1-5 specific humor elements."}
    ]
    
    romance_prompt = [
        {"role": "system", "content": "You extract romance elements from story outlines."},
        {"role": "user", "content": f"List the romance elements in this outline:\n{enhanced_text}\n\nProvide a list of 1-5 specific romance elements."}
    ]
    
    humor_result = brain.chat_structured(humor_prompt, ElementsList)
    romance_result = brain.chat_structured(romance_prompt, ElementsList)
    
    return EnhancedOutline(
        outline=enhanced_text,
        humor_elements=humor_result.elements,
        romance_elements=romance_result.elements
    )