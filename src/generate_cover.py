#!/usr/bin/env python3

from pathlib import Path
from pydantic import BaseModel
from dazllm import Llm


class CoverResult(BaseModel):
    cover_path: str
    prompt_used: str
    generation_method: str


def generate_cover(title: str, author: str, output_dir: Path, 
                  themes: list[str] | None = None, plot_type: str | None = None) -> CoverResult:
    """Generate a professional book cover using AI image generation."""
    
    # Create a very detailed prompt that emphasizes what should and shouldn't be included
    theme_context = f"The story explores themes of {', '.join(themes)}. " if themes else ""
    plot_context = f"This is a {plot_type.lower()} story. " if plot_type else ""
    
    prompt = f"""Create a professional book cover design. {theme_context}{plot_context}

MANDATORY TEXT REQUIREMENTS - EXACTLY THIS TEXT AND NO OTHER TEXT:
- The title "{title}" must be prominently displayed at the top
- The author name "{author}" must be clearly visible at the bottom  
- These are the ONLY text elements allowed on the cover
- NO other words, NO other text, NO additional writing of any kind

FORBIDDEN TEXT ELEMENTS - ABSOLUTELY DO NOT INCLUDE:
- Do not add any publisher names, imprints, or logos
- Do not include any taglines, subtitles, or promotional text
- Do not add "New York Times Bestseller" or similar marketing text
- Do not include any quotes, reviews, or endorsements
- Do not add genre labels like "A Novel", "Fiction", "Mystery", etc.
- Do not include any website URLs or social media handles
- Do not add any copyright notices or legal text
- Do not include any price information or barcodes
- Do not add any series information or book numbers
- Do not include any award badges or stickers
- No text in foreign languages
- No decorative text or typography experiments
- No hidden text or watermarks

ARTWORK REQUIREMENTS - NOT A PICTURE OF A BOOK:
- Do NOT create an image of a physical book, book spine, or book pages
- Do NOT show someone holding a book or reading a book
- Do NOT depict a bookstore, library, or bookshelf
- Do NOT show book covers, manuscripts, or written documents
- Instead create compelling artwork that captures the story's essence
- Create atmospheric scenes, landscapes, portraits, or abstract compositions
- Focus on mood, color, and visual metaphors related to the story themes
- The artwork should fill the middle section between title and author

LAYOUT SPECIFICATIONS:
- Title "{title}" at the top in large, prominent lettering (15-20% of cover height)
- Artwork in the middle section (60-70% of cover height)  
- Author "{author}" at the bottom in clear, readable text (8-10% of cover height)
- Ensure high contrast between text and background for readability
- Use professional typography - serif for title, sans-serif for author
- Maintain clear visual hierarchy with title most prominent

STYLE REQUIREMENTS:
- Professional commercial book cover appearance
- Rich colors and compelling visual design
- Artwork should reflect the story's genre and themes
- High-quality, polished graphic design
- Suitable for both print and digital publishing

CRITICAL REMINDERS:
- Only "{title}" and "{author}" text - absolutely no other text anywhere
- Not a picture of a book - create artwork suitable FOR a book cover
- Professional publishing industry standard appearance"""
    
    # Ensure the novel-specific directory exists
    novel_dir = output_dir / title.replace(' ', '_').replace(':', '_')
    novel_dir.mkdir(exist_ok=True)
    
    # Generate cover image using dazllm
    cover_filename = f"cover_{title.replace(' ', '_').replace(':', '_')}.png"
    cover_path = novel_dir / cover_filename
    
    try:
        # Use dazllm's image generation with exact DALL-E supported dimensions
        llm = Llm.model_named('openai:gpt-image-1')
        result = llm.image(prompt, str(cover_path), width=1024, height=1536)  # Portrait book cover format - now working with fixed dazllm
        
        return CoverResult(
            cover_path=str(cover_path),
            prompt_used=prompt,
            generation_method="dazllm"
        )
        
    except Exception as e:
        raise Exception(f"Error generating cover image with dazllm: {e}")