#!/usr/bin/env python3

from pydantic import BaseModel
from brain import Brain


class WritingStyle(BaseModel):
    style_description: str
    tone: str
    voice: str
    pacing: str
    examples: list[str]


def define_writing_style(brain: Brain, outline: str, themes: list[str]) -> WritingStyle:
    """Define the writing style for consistency across the novel."""
    
    messages = [
        {"role": "system", "content": "You are a writing style consultant."},
        {"role": "user", "content": f"""Define a consistent writing style for this novel:

Themes: {', '.join(themes)}
Story outline: {outline[:1000]}...

Provide specific guidance on:
- Overall style description
- Tone (e.g., serious, light, dramatic, humorous)
- Voice (e.g., first-person, third-person limited, omniscient)
- Pacing (e.g., fast-paced, measured, varies by section)
- 2-3 example sentences showing the style"""}
    ]
    
    result = brain.chat_structured(messages, WritingStyle)
    return result