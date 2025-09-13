#!/usr/bin/env python3

from pydantic import BaseModel, Field
from brain import Brain


class Chapter(BaseModel):
    number: int = Field(description="The chapter number")
    title: str = Field(description="A compelling chapter title")
    opening_situation: str = Field(description="Where we are at the start of the chapter - character states, plot situation, setting")
    chapter_goal: str = Field(description="What this chapter aims to achieve in the overall story arc")
    closing_situation: str = Field(description="Where we are at the end of the chapter - how things have changed")
    key_events: list[str] = Field(description="List of major plot points and story beats that must happen in this chapter")


class ChapterPlan(BaseModel):
    chapters: list[Chapter]


def break_into_chapters(brain: Brain, outline: str, characters: list, themes: list, plot_type: str, humor_romance_elements: str, num_chapters: int) -> ChapterPlan:
    """Flesh out the story outline into detailed chapters that progress the overall story."""
    
    character_list = "\n".join([f"- {char.name} ({char.role.value}): {char.biography}" for char in characters])
    theme_list = ", ".join(themes)
    
    messages = [
        {"role": "system", "content": "You are a story development expert who takes story outlines and fleshes them out into detailed chapter breakdowns that progress the overall story."},
        {"role": "user", "content": f"""Here's a story outline with all elements. Please flesh this out into EXACTLY {num_chapters} chapters that tell the complete story from beginning to end:

STORY OUTLINE:
{outline}

PLOT TYPE: {plot_type}

THEMES: {theme_list}

CHARACTERS:
{character_list}

HUMOR & ROMANCE ELEMENTS:
{humor_romance_elements}

Please develop this into {num_chapters} chapters. For each chapter, provide:

1. TITLE: A compelling chapter title
2. OPENING SITUATION: Where we are at the start of this chapter (character states, plot situation, setting)
3. CHAPTER GOAL: What this chapter aims to achieve in progressing the overall story
4. CLOSING SITUATION: Where we are at the end of this chapter (how things have changed)
5. KEY EVENTS: A list of the major plot points and story beats that must happen in this chapter

CRITICAL REQUIREMENTS:
- The chapters must cover the ENTIRE story from beginning to end
- Chapters are parts of the whole story, not independent narrative arcs
- Include the themes, plot type, humor and romance elements throughout
- Ensure proper story pacing and character development across all chapters
- The final chapter must provide complete closure and resolution
- Ensure no duplication across the story and across the chapters

Create exactly {num_chapters} chapters that progress the complete story."""}
    ]
    
    result = brain.chat_structured(messages, ChapterPlan)
    
    # Validate we got the right number of chapters
    if len(result.chapters) != num_chapters:
        raise ValueError(f"LLM failed to generate correct number of chapters. Requested {num_chapters}, got {len(result.chapters)}")
    
    # Ensure chapters are numbered correctly
    for i, chapter in enumerate(result.chapters):
        chapter.number = i + 1
    
    return result