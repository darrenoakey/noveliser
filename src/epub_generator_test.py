#!/usr/bin/env python3

import tempfile
import shutil
from pathlib import Path
from epub_generator import create_epub
from generate_cover import generate_cover


def test_cover_generation():
    """Test basic cover image generation (falls back to text cover in test)"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # This will likely fail AI generation and fall back to text cover in test environment
        cover_result = generate_cover(
            "Test Novel Title", 
            "Test Author", 
            temp_path,
            themes=["Adventure", "Romance"],
            plot_type="Quest"
        )
        
        cover_path = Path(cover_result.cover_path)
        assert cover_path.exists()
        assert cover_path.name == "cover.png"
        print(f"✅ Cover generated: {cover_path} ({cover_result.generation_method})")


def test_epub_creation():
    """Test basic EPUB creation"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        title = "Test Novel"
        author = "Test Author"
        chapters = [
            {"number": 1, "title": "The Beginning", "summary": "Our story starts"},
            {"number": 2, "title": "The Middle", "summary": "Things get complicated"}
        ]
        content_by_chapter = {
            1: {1: "This is the first section of the first chapter.\n\nIt has multiple paragraphs."},
            2: {1: "This is the first section of the second chapter.\n\nIt also has content."}
        }
        
        result = create_epub(
            title, author, chapters, content_by_chapter, temp_path,
            themes=["Science Fiction", "Time Travel"],
            plot_type="Voyage and Return"
        )
        
        # Check that files were created
        epub_path = Path(result.epub_path)
        cover_path = Path(result.cover_path)
        
        assert epub_path.exists()
        assert cover_path.exists()
        assert epub_path.suffix == ".epub"
        
        print(f"✅ EPUB created: {epub_path}")
        print(f"✅ Cover created: {cover_path}")


