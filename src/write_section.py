#!/usr/bin/env python3

from pydantic import BaseModel
from brain import Brain
from break_into_chapters import Chapter
from break_into_sections import Section


class SectionResult(BaseModel):
    text: str
    new_facts: list[str]


def write_section(brain: Brain, chapter: Chapter, section: Section, 
                 previous_text: str, established_facts: list[str], 
                 writing_style: str) -> SectionResult:
    """Write a single section of the novel."""
    
    # Determine position in story
    is_first_section = chapter.number == 1 and section.number == 1
    # Note: We can't determine if it's the last section without knowing total chapters
    
    messages = [
        {"role": "system", "content": f"""You are writing a section of a larger novel.

Writing Style:
{writing_style.style_description}
Tone: {writing_style.tone}
Voice: {writing_style.voice}
Pacing: {writing_style.pacing}

CRITICAL: You are writing ONLY one section, not a complete story.
{'Start the story naturally.' if is_first_section else 'Continue from where the previous section left off.'}
Do NOT conclude or wrap up unless this is explicitly the final section."""},
        {"role": "user", "content": f"""Write the next section of the story:

Chapter Title: {chapter.title}
Section Goal: {section.goal}
Key Events: {section.key_events}

{f'Previous text (last 2000 chars):\n{previous_text[-2000:]}' if previous_text else 'This is the beginning of the story.'}

Established Facts:
{chr(10).join(established_facts) if established_facts else 'None yet'}

Write approximately 1500-2000 words for this section. Maintain continuity and style. 
IMPORTANT: Do NOT include section headings, chapter numbers, or section numbers in your output. Write only the narrative text."""}
    ]
    
    section_text = brain.chat(messages)
    
    # Extract new facts
    fact_messages = [
        {"role": "system", "content": "You extract concrete facts from text that need to remain consistent."},
        {"role": "user", "content": f"""Extract new factual details from this section that should remain consistent:

{section_text}

Existing facts:
{chr(10).join(established_facts)}

Extract only NEW concrete facts like character descriptions, locations, relationships, objects, etc. 
Return as a simple list."""}
    ]
    
    fact_response = brain.chat(fact_messages)
    # Parse the response into a list (simple approach)
    new_facts = [line.strip('- ').strip() for line in fact_response.split('\n') 
                if line.strip() and not line.strip().startswith('Existing')]
    
    return SectionResult(text=section_text, new_facts=new_facts)