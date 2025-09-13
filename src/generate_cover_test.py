#!/usr/bin/env python3

import tempfile
from pathlib import Path
from generate_cover import generate_cover


def test_cover_generation():
    """Test basic cover generation using AI"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        result = generate_cover(
            "Test Novel: A Journey Through Time", 
            "Test Author", 
            temp_path,
            themes=["Adventure", "Science Fiction"],
            plot_type="Quest"
        )
        
        cover_path = Path(result.cover_path)
        assert cover_path.exists()
        assert cover_path.name == "cover_Test_Novel__A_Journey_Through_Time.png"
        assert result.generation_method == "ai"
        assert "Adventure" in result.prompt_used
        assert "TITLE PLACEMENT" in result.prompt_used
        print(f"✅ AI cover generated: {cover_path}")


def test_cover_generation_minimal():
    """Test cover generation with minimal parameters"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        result = generate_cover(
            "Simple Title", 
            "Author Name", 
            temp_path
        )
        
        cover_path = Path(result.cover_path)
        assert cover_path.exists()
        assert cover_path.name == "cover_Simple_Title.png"
        assert "TITLE PLACEMENT" in result.prompt_used
        print(f"✅ Minimal cover generated: {cover_path}")