#!/usr/bin/env python3

import json
import os
from pathlib import Path
from typing import Any, Optional
from colorama import init, Fore, Style
from pydantic import BaseModel

init(autoreset=True)

# Global state for the novel directory and continue mode
_novel_dir: Optional[Path] = None
_continue_mode: bool = False


def record(step_description: str, previous_result: Any, generator_result: Any, output_dir: Path = Path("output")) -> Any:
    """
    Record a step in the novel generation process with nice console output.
    In continue mode, skips execution if the output already exists.

    Args:
        step_description: What this step does (e.g., "Generate a title")
        previous_result: Result from the previous step (for context display)
        generator_result: The result from the generator function (or a callable that generates it)
        output_dir: Base directory for outputs

    Returns:
        The generator_result (for chaining)
    """
    global _continue_mode

    # Determine the novel directory (stateful)
    novel_dir = _get_or_set_novel_dir(None, output_dir)

    # Generate step filename
    step_name = step_description.lower().replace(' ', '_').replace('generate_', '').replace('determine_', '').replace('create_', '').replace('select_', '')
    file_path = novel_dir / f"{step_name}.json"

    # In continue mode, check if this step was already completed
    if _continue_mode and file_path.exists():
        print(f"\n{Fore.CYAN}{'─' * 60}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}⏭️  Skipping: {step_description} (already completed){Style.RESET_ALL}")

        # Load and return the existing result
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        # Try to reconstruct the object if possible
        from metadata import update_metadata_step
        update_metadata_step(novel_dir, step_description, completed=True)

        # Return the loaded data
        return json_data

    # Execute the generator if it's callable
    if callable(generator_result):
        # Display what we're doing
        print(f"\n{Fore.CYAN}{'─' * 60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📝 {step_description}...{Style.RESET_ALL}")

        # Show context from previous step if available
        if previous_result:
            prev_str = _format_for_display(previous_result)
            if prev_str:
                print(f"{Fore.BLUE}   Context: {prev_str}{Style.RESET_ALL}")

        # Update metadata to show current step
        from metadata import update_metadata_step
        update_metadata_step(novel_dir, step_description, completed=False)

        # Execute the generator
        actual_result = generator_result()
    else:
        # Display what we're doing
        print(f"\n{Fore.CYAN}{'─' * 60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📝 {step_description}...{Style.RESET_ALL}")

        # Show context from previous step if available
        if previous_result:
            prev_str = _format_for_display(previous_result)
            if prev_str:
                print(f"{Fore.BLUE}   Context: {prev_str}{Style.RESET_ALL}")

        actual_result = generator_result

    # Format the result for display
    result_str = _format_for_display(actual_result)
    print(f"{Fore.GREEN}✓ Result: {result_str}{Style.RESET_ALL}")

    # Update the novel directory if we have a title now
    if hasattr(actual_result, 'title'):
        _get_or_set_novel_dir(actual_result, output_dir)

    # Convert to JSON-serializable format
    json_data = _to_json_data(actual_result)

    # Save to file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False, default=str)

    # Try to get relative path, otherwise use absolute
    try:
        display_path = file_path.relative_to(Path.cwd())
    except ValueError:
        display_path = file_path

    print(f"{Fore.BLUE}   Saved to: {display_path}{Style.RESET_ALL}")

    # Update metadata to mark step as completed
    from metadata import update_metadata_step
    update_metadata_step(novel_dir, step_description, completed=True)

    return actual_result


def _format_for_display(result: Any) -> str:
    """Format a result for nice console display"""
    if result is None:
        return ""
    
    # Handle Pydantic models
    if isinstance(result, BaseModel):
        # Special handling for common types
        if hasattr(result, 'epub_path') and hasattr(result, 'cover_path'):
            # EpubResult
            return f"EPUB created successfully"
        elif hasattr(result, 'title'):
            return f"'{result.title}'"
        elif hasattr(result, 'plot_type'):
            return f"{result.plot_type.value if hasattr(result.plot_type, 'value') else result.plot_type}"
        elif hasattr(result, 'themes'):
            themes = [t.value if hasattr(t, 'value') else str(t) for t in result.themes]
            return f"{', '.join(themes[:3])}" + ("..." if len(themes) > 3 else "")
        elif hasattr(result, 'characters'):
            return f"{len(result.characters)} characters"
    
    # Handle strings
    if isinstance(result, str):
        return f"'{result[:50]}...'" if len(result) > 50 else f"'{result}'"
    
    # Handle lists
    if isinstance(result, list):
        return f"{len(result)} items"
    
    # Default
    result_str = str(result)
    return result_str[:50] + "..." if len(result_str) > 50 else result_str


def _get_or_set_novel_dir(result: Any, base_dir: Path) -> Path:
    """Get or set the novel directory based on title (stateful)"""
    global _novel_dir
    
    # If we already have a novel directory set, use it
    if _novel_dir is not None:
        return _novel_dir
    
    # Try to extract title from result
    title = None
    if hasattr(result, 'title'):
        title = result.title
    elif isinstance(result, dict) and 'title' in result:
        title = result['title']
    
    if title:
        # Clean title for directory name
        clean_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
        clean_title = clean_title.replace(' ', '_')
        novel_dir = base_dir / clean_title
        # Set the global state so all future calls use this directory
        _novel_dir = novel_dir
    else:
        # Use a temporary directory if no title yet, but don't set global state
        novel_dir = base_dir / "novel_in_progress"
    
    novel_dir.mkdir(parents=True, exist_ok=True)
    return novel_dir


def reset_novel_dir():
    """Reset the novel directory state for a new novel generation"""
    global _novel_dir, _continue_mode
    _novel_dir = None
    _continue_mode = False


def set_continue_mode(enabled: bool = True):
    """Enable or disable continue mode"""
    global _continue_mode
    _continue_mode = enabled


def set_novel_dir(novel_dir: Path):
    """Set the novel directory for continuing a book"""
    global _novel_dir
    _novel_dir = novel_dir


def _to_json_data(data: Any) -> Any:
    """Convert data to JSON-serializable format"""
    if isinstance(data, BaseModel):
        return data.model_dump()
    elif hasattr(data, '__dict__'):
        return data.__dict__
    else:
        return data