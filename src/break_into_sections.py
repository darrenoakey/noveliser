#!/usr/bin/env python3

from pydantic import BaseModel, Field
from brain import Brain
from break_into_chapters import Chapter


class Section(BaseModel):
    number: int = Field(description="The section number within the chapter")
    goal: str = Field(description="What this section aims to accomplish within the chapter")
    key_events: str = Field(description="Specific events and story beats that happen in this section")


class SingleSection(BaseModel):
    goal: str = Field(description="What this section aims to accomplish within the chapter")
    key_events: str = Field(description="Specific events and story beats that happen in this section")


class SectionPlan(BaseModel):
    sections: list[Section]


def break_into_sections(brain: Brain, chapter: Chapter, sections_per_chapter: int) -> SectionPlan:
    """Break a chapter into sections for writing."""
    
    if sections_per_chapter == 1:
        # Single section - different prompt and model
        messages = [
            {"role": "system", "content": "You are a writing structure expert who plans how to write a complete chapter as a single section."},
            {"role": "user", "content": f"""Plan how to write this complete chapter as a single section:

CHAPTER: {chapter.title}

OPENING SITUATION: {chapter.opening_situation}
CHAPTER GOAL: {chapter.chapter_goal}  
CLOSING SITUATION: {chapter.closing_situation}
KEY EVENTS: {', '.join(chapter.key_events)}

Since this is a single section, provide:
1. GOAL: What this section aims to accomplish (the same as the chapter goal)
2. KEY EVENTS: All the specific events and story beats that happen to get from opening to closing situation

This section should be a complete chapter of approximately 1500-2000 words when written."""}
        ]
        
        single_result = brain.chat_structured(messages, SingleSection)
        
        # Convert to SectionPlan format
        section = Section(
            number=1,
            goal=single_result.goal,
            key_events=single_result.key_events
        )
        return SectionPlan(sections=[section])
    
    else:
        # Multiple sections - original logic
        messages = [
            {"role": "system", "content": f"You are a writing structure expert who breaks chapters into manageable writing sections. You MUST create exactly {sections_per_chapter} sections, no more, no less."},
            {"role": "user", "content": f"""Break this chapter into EXACTLY {sections_per_chapter} sections for writing:

CHAPTER: {chapter.title}

OPENING SITUATION: {chapter.opening_situation}
CHAPTER GOAL: {chapter.chapter_goal}  
CLOSING SITUATION: {chapter.closing_situation}
KEY EVENTS: {', '.join(chapter.key_events)}

MANDATORY REQUIREMENT: You MUST create exactly {sections_per_chapter} sections. Not {sections_per_chapter - 1}, not {sections_per_chapter + 1}, but exactly {sections_per_chapter}.

Each section should:
1. GOAL: What this section aims to accomplish within the chapter
2. KEY EVENTS: Specific events and story beats that happen in this section

The sections should progress logically from the opening situation to the closing situation, incorporating all the key events that need to happen in this chapter.

Each section should be a manageable writing unit of approximately 1500-2000 words when written.

CRITICAL: Create exactly {sections_per_chapter} sections that collectively tell this complete chapter. Count carefully - you must have exactly {sections_per_chapter} sections in your response."""}
        ]
        
        result = brain.chat_structured(messages, SectionPlan)
        
        # Validate we got the right number of sections
        if len(result.sections) != sections_per_chapter:
            raise ValueError(f"LLM failed to generate correct number of sections. Requested {sections_per_chapter}, got {len(result.sections)}")
        
        # Ensure sections are numbered correctly
        for i, section in enumerate(result.sections):
            section.number = i + 1
        
        return result