#!/usr/bin/env python3

import json
import tempfile
from pathlib import Path
from datetime import datetime
import pytest

from metadata import (
    BookStatus, BookMetadata, write_metadata, read_metadata,
    update_metadata_step, mark_book_finished, list_books_by_status,
    find_book_dir_by_title
)


def test_book_metadata_creation():
    """Test creating book metadata"""
    metadata = BookMetadata(
        title="Test Novel",
        description="A test novel",
        status=BookStatus.ONGOING,
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat(),
        author="Test Author",
        model_name="test-model",
        num_chapters=10,
        sections_per_chapter=5
    )

    assert metadata.title == "Test Novel"
    assert metadata.status == BookStatus.ONGOING
    assert metadata.completed_steps == []
    assert metadata.current_step is None


def test_write_and_read_metadata():
    """Test writing and reading metadata to/from disk"""
    with tempfile.TemporaryDirectory() as tmpdir:
        novel_dir = Path(tmpdir) / "test_novel"
        novel_dir.mkdir()

        # Create and write metadata
        metadata = BookMetadata(
            title="Test Novel",
            description="A test novel",
            status=BookStatus.ONGOING,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            author="Test Author",
            model_name="test-model",
            num_chapters=10,
            sections_per_chapter=5
        )
        write_metadata(novel_dir, metadata)

        # Read it back
        read_meta = read_metadata(novel_dir)
        assert read_meta is not None
        assert read_meta.title == "Test Novel"
        assert read_meta.status == BookStatus.ONGOING


def test_update_metadata_step():
    """Test updating metadata with step progress"""
    with tempfile.TemporaryDirectory() as tmpdir:
        novel_dir = Path(tmpdir) / "test_novel"
        novel_dir.mkdir()

        # Create initial metadata
        metadata = BookMetadata(
            title="Test Novel",
            description="A test novel",
            status=BookStatus.ONGOING,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            author="Test Author",
            model_name="test-model",
            num_chapters=10,
            sections_per_chapter=5
        )
        write_metadata(novel_dir, metadata)

        # Update with current step
        update_metadata_step(novel_dir, "Generate title", completed=False)
        meta = read_metadata(novel_dir)
        assert meta.current_step == "Generate title"
        assert "Generate title" not in meta.completed_steps

        # Mark step as completed
        update_metadata_step(novel_dir, "Generate title", completed=True)
        meta = read_metadata(novel_dir)
        assert meta.current_step is None
        assert "Generate title" in meta.completed_steps


def test_mark_book_finished():
    """Test marking a book as finished"""
    with tempfile.TemporaryDirectory() as tmpdir:
        novel_dir = Path(tmpdir) / "test_novel"
        novel_dir.mkdir()

        # Create initial metadata
        metadata = BookMetadata(
            title="Test Novel",
            description="A test novel",
            status=BookStatus.ONGOING,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            author="Test Author",
            model_name="test-model",
            num_chapters=10,
            sections_per_chapter=5,
            current_step="Create EPUB"
        )
        write_metadata(novel_dir, metadata)

        # Mark as finished
        mark_book_finished(novel_dir, "/path/to/epub", "/path/to/cover")

        meta = read_metadata(novel_dir)
        assert meta.status == BookStatus.FINISHED
        assert meta.epub_path == "/path/to/epub"
        assert meta.cover_path == "/path/to/cover"
        assert meta.current_step is None


def test_list_books_by_status():
    """Test listing books by status"""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)

        # Create multiple books with different statuses
        for i, status in enumerate([BookStatus.ONGOING, BookStatus.FINISHED, BookStatus.ONGOING]):
            novel_dir = output_dir / f"novel_{i}"
            novel_dir.mkdir()

            metadata = BookMetadata(
                title=f"Novel {i}",
                description=f"Description {i}",
                status=status,
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat(),
                author="Test Author",
                model_name="test-model",
                num_chapters=10,
                sections_per_chapter=5
            )
            write_metadata(novel_dir, metadata)

        # List ongoing books
        ongoing = list_books_by_status(output_dir, BookStatus.ONGOING)
        assert len(ongoing) == 2
        assert all(b["title"] in ["Novel 0", "Novel 2"] for b in ongoing)

        # List finished books
        finished = list_books_by_status(output_dir, BookStatus.FINISHED)
        assert len(finished) == 1
        assert finished[0]["title"] == "Novel 1"


def test_find_book_dir_by_title():
    """Test finding a book directory by title"""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)

        # Create a book
        novel_dir = output_dir / "test_novel"
        novel_dir.mkdir()

        metadata = BookMetadata(
            title="My Special Novel",
            description="A special novel",
            status=BookStatus.ONGOING,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            author="Test Author",
            model_name="test-model",
            num_chapters=10,
            sections_per_chapter=5
        )
        write_metadata(novel_dir, metadata)

        # Find it by title
        found_dir = find_book_dir_by_title(output_dir, "My Special Novel")
        assert found_dir == novel_dir

        # Try to find non-existent book
        not_found = find_book_dir_by_title(output_dir, "Non-existent")
        assert not_found is None