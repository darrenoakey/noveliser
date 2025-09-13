#!/usr/bin/env python3

from enum import Enum
from pydantic import BaseModel, Field
from brain import Brain


class UniversalTheme(str, Enum):
    """Universal themes commonly found in literature"""
    LOVE_AND_RELATIONSHIPS = "Love and Relationships"
    GOOD_VS_EVIL = "Good vs Evil"
    COMING_OF_AGE = "Coming of Age"
    DEATH_AND_LOSS = "Death and Loss"
    POWER_AND_CORRUPTION = "Power and Corruption"
    REDEMPTION = "Redemption"
    SURVIVAL = "Survival"
    IDENTITY_AND_SELF = "Identity and Self-Discovery"
    FREEDOM_VS_OPPRESSION = "Freedom vs Oppression"
    SACRIFICE = "Sacrifice"
    JUSTICE = "Justice"
    BETRAYAL = "Betrayal"
    FORGIVENESS = "Forgiveness"
    FAMILY = "Family"
    FRIENDSHIP = "Friendship"
    COURAGE = "Courage"
    LOYALTY = "Loyalty"
    TRUTH_VS_DECEPTION = "Truth vs Deception"
    HOPE = "Hope"
    REVENGE = "Revenge"
    TIME_AND_CHANGE = "Time and Change"
    TRADITION_VS_PROGRESS = "Tradition vs Progress"
    NATURE_AND_HUMANITY = "Nature and Humanity"
    SCIENCE_AND_ETHICS = "Science and Ethics"
    CULTURAL_EXCHANGE = "Cultural Exchange"
    FATE_VS_FREE_WILL = "Fate vs Free Will"
    ISOLATION_AND_BELONGING = "Isolation and Belonging"


class ThemeSelection(BaseModel):
    """Result of theme selection analysis"""
    themes: list[UniversalTheme] = Field(
        description="2-3 universal themes that best fit the story", 
        min_items=2, 
        max_items=3
    )
    reasoning: str = Field(description="Explanation of why these themes were chosen")


def select_themes(brain: Brain, description: str, plot_type: str) -> ThemeSelection:
    """Select appropriate universal themes for the story."""
    
    messages = [
        {"role": "system", "content": "You are a literary theme analyst with expertise in identifying universal themes in storytelling."},
        {"role": "user", "content": f"Given this story description and plot type ({plot_type}), select 2-3 universal themes that would best fit this narrative:\n\n{description}"}
    ]
    
    return brain.chat_structured(messages, ThemeSelection)