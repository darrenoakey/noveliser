#!/usr/bin/env python3

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from enum import Enum


class BookStatus(Enum):
    """Status of a book generation"""
    ONGOING = "ongoing"
    FINISHED = "finished"
    FAILED = "failed"


class BookMetadata(BaseModel):
    """Metadata for tracking book generation state"""
    title: str
    description: str
    status: BookStatus
    created_at: str
    updated_at: str
    author: str
    model_name: str
    num_chapters: int
    sections_per_chapter: int
    completed_steps: List[str] = []
    current_step: Optional[str] = None
    epub_path: Optional[str] = None
    cover_path: Optional[str] = None


def write_metadata(novel_dir: Path, metadata: BookMetadata):
    """Write metadata to the novel directory"""
    metadata_path = novel_dir / "metadata.json"
    metadata.updated_at = datetime.now().isoformat()

    # Convert to dict and ensure enum values are strings
    data = metadata.model_dump()
    data['status'] = metadata.status.value

    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def read_metadata(novel_dir: Path) -> Optional[BookMetadata]:
    """Read metadata from the novel directory"""
    metadata_path = novel_dir / "metadata.json"

    if not metadata_path.exists():
        return None

    with open(metadata_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return BookMetadata(**data)


def update_metadata_step(novel_dir: Path, step_name: str, completed: bool = False):
    """Update metadata with current/completed step"""
    metadata = read_metadata(novel_dir)
    if not metadata:
        return

    if completed:
        if step_name not in metadata.completed_steps:
            metadata.completed_steps.append(step_name)
        if metadata.current_step == step_name:
            metadata.current_step = None
    else:
        metadata.current_step = step_name

    write_metadata(novel_dir, metadata)


def mark_book_finished(novel_dir: Path, epub_path: str, cover_path: str):
    """Mark a book as finished with final paths"""
    metadata = read_metadata(novel_dir)
    if not metadata:
        return

    metadata.status = BookStatus.FINISHED
    metadata.epub_path = epub_path
    metadata.cover_path = cover_path
    metadata.current_step = None

    write_metadata(novel_dir, metadata)


def list_books_by_status(output_dir: Path, status: BookStatus) -> List[Dict[str, Any]]:
    """List all books with a given status"""
    books = []

    if not output_dir.exists():
        return books

    for novel_dir in output_dir.iterdir():
        if not novel_dir.is_dir():
            continue

        metadata = read_metadata(novel_dir)
        if metadata and metadata.status == status:
            books.append({
                "title": metadata.title,
                "description": metadata.description,
                "created_at": metadata.created_at,
                "updated_at": metadata.updated_at,
                "author": metadata.author,
                "directory": str(novel_dir),
                "current_step": metadata.current_step,
                "completed_steps": len(metadata.completed_steps),
                "epub_path": metadata.epub_path,
                "cover_path": metadata.cover_path
            })

    # Sort by updated_at (most recent first)
    books.sort(key=lambda x: x["updated_at"], reverse=True)

    return books


def find_book_dir_by_title(output_dir: Path, title: str) -> Optional[Path]:
    """Find a book directory by its title"""
    for novel_dir in output_dir.iterdir():
        if not novel_dir.is_dir():
            continue

        metadata = read_metadata(novel_dir)
        if metadata and metadata.title == title:
            return novel_dir

    return None