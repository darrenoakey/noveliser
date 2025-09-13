#!/usr/bin/env python3

import pytest
import tempfile
import json
from pathlib import Path
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from noveliser import write_novel


def test_write_novel_creates_all_artifacts():
    """Test that the novel pipeline creates all expected artifacts"""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Override output directory in the function
        import noveliser
        original_path = Path("output")
        noveliser.Path = lambda x: Path(tmpdir) if x == "output" else original_path
        
        # Simple description for fast testing
        description = "A story about a detective solving a mystery"
        
        # Run with minimal chapters/sections for speed
        output_dir = write_novel(description, num_chapters=2, sections_per_chapter=2)
        
        # Check that all expected files were created
        expected_files = [
            "title.json",
            "plot_type.json", 
            "themes.json",
            "characters.json",
            "outline.json",
            "humor_and_romance.json",
            "writing_style.json",
            "chapters.json"
        ]
        
        # Find the novel directory (should be under output_dir)
        novel_dirs = [d for d in Path(tmpdir).iterdir() if d.is_dir()]
        assert len(novel_dirs) > 0, "No novel directory created"
        
        novel_dir = novel_dirs[0]
        
        for filename in expected_files:
            file_path = novel_dir / filename
            assert file_path.exists(), f"Missing file: {filename}"
            
            # Check file is valid JSON and not empty
            with open(file_path) as f:
                data = json.load(f)
                assert data, f"Empty data in {filename}"
        
        print(f"All artifacts created in: {novel_dir}")
        print(f"Files: {list(novel_dir.glob('*.json'))}")


def test_write_novel_pipeline_flow():
    """Test that data flows correctly through the pipeline"""
    
    # This is more of an integration test
    description = "A young wizard discovers their powers"
    
    # We'll use the real function but with minimal settings
    output_dir = write_novel(description, num_chapters=1, sections_per_chapter=1)
    
    # Check the output directory exists
    assert output_dir.exists()
    
    # Find the novel directory
    novel_dirs = [d for d in output_dir.iterdir() if d.is_dir()]
    assert len(novel_dirs) > 0
    
    novel_dir = novel_dirs[0]
    
    # Load and verify the title
    with open(novel_dir / "title.json") as f:
        title_data = json.load(f)
        assert "title" in title_data
        assert title_data["title"]
    
    # Load and verify plot type
    with open(novel_dir / "plot_type.json") as f:
        plot_data = json.load(f)
        assert "plot_type" in plot_data
    
    # Load and verify themes
    with open(novel_dir / "themes.json") as f:
        themes_data = json.load(f)
        assert "themes" in themes_data
        assert len(themes_data["themes"]) > 0
    
    print("Pipeline flow verified")