#!/usr/bin/env python3

from pydantic import BaseModel
from brain import Brain
from create_characters import Character


class Outline(BaseModel):
    outline: str


def create_outline(brain: Brain, description: str, plot_type: str, themes: list[str], 
                  characters: list[Character], num_chapters: int, sections_per_chapter: int) -> Outline:
    """Create a detailed story outline from description, plot type, themes, and characters."""
    
    char_descriptions = "\n".join([f"- {c.name} ({c.role.value}): {c.biography}" for c in characters])
    total_sections = num_chapters * sections_per_chapter
    
    scope_guidance = ""
    if num_chapters == 1:
        scope_guidance = "This is a complete short story that must have a full beginning, middle, and end within a single chapter."
    elif num_chapters <= 3:
        scope_guidance = f"This is a novella with {num_chapters} chapters that must tell a complete story with full resolution."
    else:
        scope_guidance = f"This is a full novel with {num_chapters} chapters that should have rich development and multiple plot threads."
    
    messages = [
        {"role": "system", "content": "You are a master story outliner who creates compelling narrative structures that fit perfectly within the specified scope."},
        {"role": "user", "content": f"""Create a detailed story outline that tells a COMPLETE story within exactly {num_chapters} chapters and {total_sections} total sections:

Description: {description}
Plot Type: {plot_type}
Themes: {', '.join(themes)}
Characters:
{char_descriptions}

SCOPE: {scope_guidance}

CRITICAL: This outline must contain a complete story arc with:
- Clear beginning that establishes setting, characters, and conflict
- Well-developed middle that explores the conflict and develops characters
- Satisfying resolution that ties up all plot threads
- All major plot points, character development, and thematic elements must fit within {num_chapters} chapters

The story should feel complete and satisfying at this length, not like a fragment or the beginning of a longer work."""}
    ]
    
    outline_text = brain.chat(messages)
    return Outline(outline=outline_text)