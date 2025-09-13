#!/usr/bin/env python3

import uuid
from pathlib import Path
from pydantic import BaseModel
from ebooklib import epub
from generate_cover import generate_cover


class EpubResult(BaseModel):
    epub_path: str
    cover_path: str


def create_epub(title: str, author: str, chapters: list[dict[str, any]], 
               content_by_chapter: dict[int, dict], output_dir: Path,
               themes: list[str] | None = None, plot_type: str | None = None) -> EpubResult:
    """Create an EPUB file from the novel content."""
    
    # Generate cover using AI
    cover_result = generate_cover(title, author, output_dir, themes, plot_type)
    cover_path = Path(cover_result.cover_path)
    
    book = epub.EpubBook()
    
    # Set metadata
    book.set_identifier(str(uuid.uuid4()))
    book.set_title(title)
    book.set_language('en')
    book.add_author(author)
    
    # Add cover to EPUB
    with open(cover_path, 'rb') as f:
        book.set_cover("cover.png", f.read())
    
    # Create chapters
    epub_chapters = []
    spine = ['nav']
    num_chapters = len(content_by_chapter)
    
    for chapter_num, chapter_data in content_by_chapter.items():
        chapter = chapters[chapter_num - 1]
        
        # Only add chapter heading if there's more than one chapter
        if num_chapters > 1:
            chapter_content = f"<h1>Chapter {chapter_num}: {chapter['title']}</h1>\n"
            chapter_title = f"Chapter {chapter_num}: {chapter['title']}"
        else:
            chapter_content = ""  # No chapter heading for single chapter
            chapter_title = title  # Use the book title instead
        
        for section_num, section_text in chapter_data.items():
            if isinstance(section_text, str):
                # Split into paragraphs for better formatting
                paragraphs = section_text.split('\n\n')
                for para in paragraphs:
                    if para.strip():
                        chapter_content += f"<p>{para.strip()}</p>\n"
        
        # Create epub chapter
        epub_chapter = epub.EpubHtml(
            title=chapter_title,
            file_name=f'chapter_{chapter_num}.xhtml',
            lang='en'
        )
        epub_chapter.content = chapter_content
        
        book.add_item(epub_chapter)
        epub_chapters.append(epub_chapter)
        spine.append(epub_chapter)
    
    # Add navigation (only if multiple chapters)
    if num_chapters > 1:
        book.toc = epub_chapters
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
    
    # Set spine
    book.spine = spine
    
    # Write epub
    epub_path = output_dir / f"{title.replace(':', ' -')}.epub"
    epub.write_epub(str(epub_path), book, {})
    
    return EpubResult(epub_path=str(epub_path), cover_path=str(cover_path))