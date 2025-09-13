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
from record import record, reset_novel_dir
from generate_title import generate_title
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


def write_novel(description: str, output_dir: Path, model_name: str = "ollama:gpt-oss:20b", 
                num_chapters: int = 10, sections_per_chapter: int = 10, author: str = "Darren Oakey") -> Path:
    """
    Generate a complete novel using a clean, linear pipeline.
    Each step is recorded and displayed with progress tracking.
    """
    
    # Reset the novel directory state for this new novel
    reset_novel_dir()
    
    # Initialize the brain
    llm = Llm.model_named(model_name)
    brain = Brain(llm)
    
    # Linear pipeline - each line is clear and testable
    title = record("Generate a title", None, 
                  generate_title(brain, description), output_dir)
    
    plot_type = record("Determine plot type", title,
                      determine_plot_type(brain, description), output_dir)
    
    themes = record("Select themes", plot_type,
                   select_themes(brain, description, plot_type.plot_type.value), output_dir)
    
    characters = record("Create characters", themes,
                       create_characters(brain, description, plot_type.plot_type.value, 
                                       [t.value for t in themes.themes]), output_dir)
    
    outline = record("Create outline", characters,
                    create_outline(brain, description, plot_type.plot_type.value,
                                 [t.value for t in themes.themes], characters.characters,
                                 num_chapters, sections_per_chapter), output_dir)
    
    enhanced_outline = record("Add humor and romance", outline,
                            add_humor_and_romance(brain, outline.outline), output_dir)
    
    writing_style = record("Define writing style", enhanced_outline,
                         define_writing_style(brain, enhanced_outline.outline, 
                                            [t.value for t in themes.themes]), output_dir)
    
    chapters = record(f"Break into {num_chapters} chapters", writing_style,
                     break_into_chapters(brain, enhanced_outline.outline, 
                                       characters.characters, 
                                       [t.value for t in themes.themes],
                                       plot_type.plot_type.value,
                                       enhanced_outline.outline,
                                       num_chapters), output_dir)
    
    # Write all the sections
    all_text = ""
    facts = []
    content_by_chapter = {}
    
    for chapter in chapters.chapters:
        content_by_chapter[chapter.number] = {}
        
        # Break this chapter into sections
        section_plan = record(f"Break Chapter {chapter.number} into {sections_per_chapter} sections", chapter,
                             break_into_sections(brain, chapter, sections_per_chapter), output_dir)
        
        # Write each section
        for section in section_plan.sections:
            section_result = record(f"Write Chapter {chapter.number}, Section {section.number}", 
                                  (chapter, section, all_text, facts),
                                  write_section(brain, chapter, section, all_text, facts, writing_style),
                                  output_dir)
            
            # Update state for next section
            all_text += "\n\n" + section_result.text
            facts.extend(section_result.new_facts)
            content_by_chapter[chapter.number][section.number] = section_result.text
    
    # Create the final EPUB
    epub_result = record("Create EPUB", content_by_chapter,
                        create_epub(title.title, author, 
                                  [ch.model_dump() for ch in chapters.chapters],
                                  content_by_chapter, output_dir,
                                  [t.value for t in themes.themes],
                                  plot_type.plot_type.value), output_dir)
    
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