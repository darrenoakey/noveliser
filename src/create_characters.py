#!/usr/bin/env python3

from enum import Enum
from pydantic import BaseModel
from brain import Brain


class CharacterRole(str, Enum):
    PROTAGONIST = "protagonist"
    ANTAGONIST = "antagonist" 
    SUPPORTING = "supporting"
    MINOR = "minor"


class Character(BaseModel):
    name: str
    biography: str
    role: CharacterRole
    traits: list[str]  # personality traits


class CharactersList(BaseModel):
    characters: list[Character]


def create_characters(brain: Brain, description: str, plot_type: str, themes: list[str]) -> CharactersList:
    """Create characters based on story description, plot type, and themes."""
    
    theme_text = ', '.join(themes)
    
    # Check if the description contains character names that should be used
    character_instruction = ""
    description_lower = description.lower()
    if "character" in description_lower or "named" in description_lower or any(word in description_lower for word in ["here are the characters", "character names", "characters are"]):
        character_instruction = "\n\nIMPORTANT: The description contains specific character names or character information. You MUST use these exact names and any provided character details from the description. Do not create entirely new character names if names are already provided in the description."
    
    messages = [
        {"role": "system", "content": "You are a character creation expert. Create compelling characters with distinct personalities and clear roles. If character names are provided in the description, you MUST use those exact names."},
        {"role": "user", "content": f"""Create 3-8 characters for this story:

Description: {description}
Plot Type: {plot_type}
Themes: {theme_text}

Create characters with full biographies and personality traits.{character_instruction}"""}
    ]
    
    result = brain.chat_structured(messages, CharactersList)
    return result