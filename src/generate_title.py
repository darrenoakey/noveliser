#!/usr/bin/env python3

from pydantic import BaseModel
from brain import Brain


class Title(BaseModel):
    title: str


def generate_title(brain: Brain, description: str) -> Title:
    """Generate a working title from the story description."""
    
    messages = [
        {"role": "system", "content": "You are a creative title generator for novels."},
        {"role": "user", "content": f"Create a compelling, memorable title for this story:\n\n{description}\n\nRespond with just the title, no quotes or explanation."}
    ]
    
    title_text = brain.chat(messages).strip().strip('"\'')
    return Title(title=title_text)