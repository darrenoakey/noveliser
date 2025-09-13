#!/usr/bin/env python3

from enum import Enum
from pydantic import BaseModel, Field
from brain import Brain


class PlotTypeEnum(str, Enum):
    """Christopher Booker's Seven Basic Plots"""
    OVERCOMING_THE_MONSTER = "Overcoming the Monster"
    RAGS_TO_RICHES = "Rags to Riches"
    THE_QUEST = "The Quest"
    VOYAGE_AND_RETURN = "Voyage and Return"
    COMEDY = "Comedy"
    TRAGEDY = "Tragedy"
    REBIRTH = "Rebirth"


class PlotType(BaseModel):
    """Result of plot type determination"""
    plot_type: PlotTypeEnum = Field(description="The basic plot type that best fits the story")
    reasoning: str = Field(description="Explanation of why this plot type was chosen")


def determine_plot_type(brain: Brain, description: str) -> PlotType:
    """Determine which of the 7 basic plots fits the story description best."""
    
    messages = [
        {"role": "system", "content": "You are a literary analyst specializing in Christopher Booker's Seven Basic Plots."},
        {"role": "user", "content": f"Analyze this story description and determine which of the 7 basic plots it best fits:\n\n{description}"}
    ]
    
    return brain.chat_structured(messages, PlotType)