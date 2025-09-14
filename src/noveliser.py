#!/usr/bin/env python3

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.expanduser('~/src/dazllm'))

from brain import Brain
from dazllm import Llm

# Import our clean, tested modules
from record import record, reset_novel_dir, set_continue_mode, set_novel_dir
from generate_title import generate_title
from generate_cover import generate_cover
from determine_plot_type import determine_plot_type
from select_themes import select_themes
from create_characters import create_characters
from create_outline import create_outline
from add_humor_and_romance import add_humor_and_romance
from define_writing_style import define_writing_style
from break_into_chapters import break_into_chapters
from break_into_sections import break_into_sections
from write_section import write_section
from epub_generator import create_epub
from metadata import BookMetadata, BookStatus, write_metadata, read_metadata, mark_book_finished
from datetime import datetime


def write_novel(description: str, output_dir: Path, model_name: str = "ollama:gpt-oss:20b",
                num_chapters: int = 10, sections_per_chapter: int = 10, author: str = "Darren Oakey",
                continue_novel_dir: Path = None) -> Path:
    """
    Generate a complete novel using a clean, linear pipeline.
    Each step is recorded and displayed with progress tracking.
    Can continue from a previous incomplete novel generation.
    """

    # Handle continue mode
    if continue_novel_dir:
        set_continue_mode(True)
        set_novel_dir(continue_novel_dir)
        metadata = read_metadata(continue_novel_dir)
        if metadata:
            description = metadata.description
            model_name = metadata.model_name
            num_chapters = metadata.num_chapters
            sections_per_chapter = metadata.sections_per_chapter
            author = metadata.author
    else:
        # Reset the novel directory state for this new novel
        reset_novel_dir()
    
    # Initialize the brain
    llm = Llm.model_named(model_name)
    brain = Brain(llm)
    
    # Linear pipeline - each line is clear and testable
    # Use lambdas for all steps to enable skipping in continue mode
    title = record("Generate a title", None,
                  lambda: generate_title(brain, description), output_dir)

    # Create metadata immediately after getting the title
    if not continue_novel_dir:
        # Handle both object and dict formats
        title_str = title.title if hasattr(title, 'title') else title.get('title', title)
        novel_dir = output_dir / title_str.replace(' ', '_').replace(':', '_')
        novel_dir.mkdir(exist_ok=True)
        metadata = BookMetadata(
            title=title_str,
            description=description,
            status=BookStatus.ONGOING,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            author=author,
            model_name=model_name,
            num_chapters=num_chapters,
            sections_per_chapter=sections_per_chapter
        )
        write_metadata(novel_dir, metadata)

    # Generate cover immediately after title for early visual feedback
    # Generate cover immediately after title for early visual feedback
    title_str = title.title if hasattr(title, 'title') else title.get('title', title)
    cover = record("Generate cover image", title,
                  lambda: generate_cover(title_str, author, output_dir), output_dir)

    plot_type = record("Determine plot type", title,
                      lambda: determine_plot_type(brain, description), output_dir)

    # Handle both object and dict formats for plot_type
    plot_type_value = plot_type.plot_type.value if hasattr(plot_type, 'plot_type') else plot_type.get('plot_type', plot_type)
    themes = record("Select themes", plot_type,
                   lambda: select_themes(brain, description, plot_type_value), output_dir)
    
    # Handle both object and dict formats for themes
    theme_values = [t.value for t in themes.themes] if hasattr(themes, 'themes') else themes.get('themes', [])
    characters = record("Create characters", themes,
                       lambda: create_characters(brain, description, plot_type_value,
                                       theme_values), output_dir)
    
    # Handle both object and dict formats for characters
    chars = characters.characters if hasattr(characters, 'characters') else characters.get('characters', [])
    outline = record("Create outline", characters,
                    lambda: create_outline(brain, description, plot_type_value,
                                 theme_values, chars,
                                 num_chapters, sections_per_chapter), output_dir)
    
    # Handle both object and dict formats for outline
    outline_text = outline.outline if hasattr(outline, 'outline') else outline.get('outline', outline)
    enhanced_outline = record("Add humor and romance", outline,
                            lambda: add_humor_and_romance(brain, outline_text), output_dir)
    
    # Handle both object and dict formats for enhanced_outline
    enhanced_text = enhanced_outline.outline if hasattr(enhanced_outline, 'outline') else enhanced_outline.get('outline', enhanced_outline)
    writing_style = record("Define writing style", enhanced_outline,
                         lambda: define_writing_style(brain, enhanced_text,
                                            theme_values), output_dir)
    
    chapters = record(f"Break into {num_chapters} chapters", writing_style,
                     lambda: break_into_chapters(brain, enhanced_text,
                                       chars,
                                       theme_values,
                                       plot_type_value,
                                       enhanced_text,
                                       num_chapters), output_dir)
    
    # Write all the sections
    all_text = ""
    facts = []
    content_by_chapter = {}
    
    # Handle both object and dict formats for chapters
    chapter_list = chapters.chapters if hasattr(chapters, 'chapters') else chapters.get('chapters', [])
    for chapter in chapter_list:
        chapter_num = chapter.number if hasattr(chapter, 'number') else chapter.get('number')
        content_by_chapter[chapter_num] = {}

        # Break this chapter into sections
        section_plan = record(f"Break Chapter {chapter_num} into {sections_per_chapter} sections", chapter,
                             lambda ch=chapter: break_into_sections(brain, ch, sections_per_chapter), output_dir)

        # Handle both object and dict formats for sections
        section_list = section_plan.sections if hasattr(section_plan, 'sections') else section_plan.get('sections', [])

        # Write each section
        for section in section_list:
            section_num = section.number if hasattr(section, 'number') else section.get('number')
            section_result = record(f"Write Chapter {chapter_num}, Section {section_num}",
                                  (chapter, section, all_text, facts),
                                  lambda ch=chapter, sec=section, txt=all_text, f=facts, ws=writing_style: write_section(brain, ch, sec, txt, f, ws),
                                  output_dir)

            # Update state for next section
            section_text = section_result.text if hasattr(section_result, 'text') else section_result.get('text', '')
            new_facts = section_result.new_facts if hasattr(section_result, 'new_facts') else section_result.get('new_facts', [])
            all_text += "\n\n" + section_text
            facts.extend(new_facts)
            content_by_chapter[chapter_num][section_num] = section_text
    
    # Create the final EPUB
    # Convert chapters to dict format if needed
    chapters_data = [ch.model_dump() if hasattr(ch, 'model_dump') else ch for ch in chapter_list]
    epub_result = record("Create EPUB", content_by_chapter,
                        lambda: create_epub(title_str, author,
                                  chapters_data,
                                  content_by_chapter, output_dir,
                                  theme_values,
                                  plot_type_value), output_dir)

    # Mark the book as finished
    novel_dir = output_dir / title_str.replace(' ', '_').replace(':', '_')
    epub_path = epub_result.epub_path if hasattr(epub_result, 'epub_path') else epub_result.get('epub_path', '')
    cover_path = cover.cover_path if hasattr(cover, 'cover_path') else cover.get('cover_path', '')
    mark_book_finished(novel_dir, epub_path, cover_path)

    return epub_result


def main():
    import argparse
    from colorama import init, Fore, Style
    
    init(autoreset=True)
    
    parser = argparse.ArgumentParser(description='Generate a novel using AI')
    parser.add_argument('description', help='Novel description')
    parser.add_argument('--chapters', type=int, default=10,
                       help='Number of chapters (default: 10)')
    parser.add_argument('--sections', type=int, default=10,
                       help='Sections per chapter (default: 10)')
    parser.add_argument('--model', default='ollama:gpt-oss:20b',
                       help='LLM model to use')
    parser.add_argument('--author', default='Darren Oakey',
                       help='Author name (default: Darren Oakey)')
    
    args = parser.parse_args()
    
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Starting novel generation...{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    # Set output directory relative to script location
    script_dir = Path(__file__).parent.parent
    output_dir = script_dir / "output"
    output_dir.mkdir(exist_ok=True)
    
    try:
        epub_result = write_novel(
            args.description,
            output_dir,
            args.model,
            args.chapters,
            args.sections,
            args.author
        )
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ Novel generation complete!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}📖 EPUB file: {epub_result.epub_path}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}🎨 Cover image: {epub_result.cover_path}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Generation interrupted by user{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}Error during generation: {e}{Style.RESET_ALL}")
        raise


if __name__ == "__main__":
    main()