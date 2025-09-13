#!/usr/bin/env python3

import pytest
import json
import tempfile
from pathlib import Path
from pydantic import BaseModel
from typing import List
from enum import Enum

from record import record, _format_for_display, _get_novel_dir, _to_json_data


class TestPlotType(Enum):
    COMEDY = "comedy"
    TRAGEDY = "tragedy"


class TitleResult(BaseModel):
    title: str
    subtitle: str = ""


class PlotResult(BaseModel):
    plot_type: TestPlotType
    reasoning: str


class ThemeResult(BaseModel):
    themes: List[str]


def test_record_with_title():
    """Test recording a title generation step"""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        
        # Generate a title
        title_result = TitleResult(title="The Great Adventure", subtitle="A Journey Begins")
        
        # Record it
        result = record("Generate a title", None, title_result, output_dir)
        
        # Check it returns the input
        assert result == title_result
        
        # Check file was created
        novel_dir = output_dir / "The_Great_Adventure"
        assert novel_dir.exists()
        
        file_path = novel_dir / "a_title.json"
        assert file_path.exists()
        
        # Check content
        with open(file_path) as f:
            data = json.load(f)
        assert data['title'] == "The Great Adventure"
        assert data['subtitle'] == "A Journey Begins"


def test_record_with_previous_context():
    """Test recording with context from previous step"""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        
        # Previous result
        title_result = TitleResult(title="Epic Story")
        
        # New result
        plot_result = PlotResult(plot_type=TestPlotType.COMEDY, reasoning="It's funny")
        
        # Record with context
        result = record("Determine plot type", title_result, plot_result, output_dir)
        
        # Check file was created in correct directory
        novel_dir = output_dir / "novel_in_progress"  # No title in plot_result
        file_path = novel_dir / "plot_type.json"
        assert file_path.exists()


def test_format_for_display_with_title():
    """Test formatting title results for display"""
    result = TitleResult(title="My Amazing Novel")
    display = _format_for_display(result)
    assert display == "'My Amazing Novel'"


def test_format_for_display_with_plot_type():
    """Test formatting plot type for display"""
    result = PlotResult(plot_type=TestPlotType.COMEDY, reasoning="test")
    display = _format_for_display(result)
    assert display == "comedy"


def test_format_for_display_with_themes():
    """Test formatting themes for display"""
    result = ThemeResult(themes=["love", "loss", "redemption", "hope", "courage"])
    display = _format_for_display(result)
    assert display == "love, loss, redemption..."


def test_format_for_display_with_string():
    """Test formatting strings for display"""
    short_str = "Hello world"
    assert _format_for_display(short_str) == "'Hello world'"
    
    long_str = "This is a very long string that should be truncated for display purposes to keep the output clean"
    display = _format_for_display(long_str)
    assert display.startswith("'This is a very long string")
    assert display.endswith("...'")
    assert len(display) <= 55  # 50 chars + quotes + ellipsis


def test_get_novel_dir_with_title():
    """Test getting novel directory when title is available"""
    with tempfile.TemporaryDirectory() as tmpdir:
        base_dir = Path(tmpdir)
        
        result = TitleResult(title="Test Novel: The Beginning")
        novel_dir = _get_novel_dir(result, base_dir)
        
        assert novel_dir.name == "Test_Novel_The_Beginning"
        assert novel_dir.exists()


def test_get_novel_dir_without_title():
    """Test getting novel directory when no title is available"""
    with tempfile.TemporaryDirectory() as tmpdir:
        base_dir = Path(tmpdir)
        
        result = {"some": "data"}
        novel_dir = _get_novel_dir(result, base_dir)
        
        assert novel_dir.name == "novel_in_progress"
        assert novel_dir.exists()


def test_to_json_data_with_pydantic():
    """Test converting Pydantic model to JSON data"""
    model = TitleResult(title="Test", subtitle="Sub")
    data = _to_json_data(model)
    
    assert isinstance(data, dict)
    assert data['title'] == "Test"
    assert data['subtitle'] == "Sub"


def test_to_json_data_with_dict():
    """Test converting dict to JSON data"""
    original = {"key": "value"}
    data = _to_json_data(original)
    assert data == original


def test_to_json_data_with_object():
    """Test converting object with __dict__ to JSON data"""
    class TestObj:
        def __init__(self):
            self.attr = "value"
    
    obj = TestObj()
    data = _to_json_data(obj)
    assert data == {"attr": "value"}


def test_record_creates_nested_directories():
    """Test that record creates nested directories if needed"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Use a deep path that doesn't exist
        output_dir = Path(tmpdir) / "deep" / "nested" / "path"
        
        title_result = TitleResult(title="Nested Novel")
        result = record("Generate title", None, title_result, output_dir)
        
        # Check nested structure was created
        novel_dir = output_dir / "Nested_Novel"
        assert novel_dir.exists()
        assert novel_dir.is_dir()