![](banner.jpg)

# Noveliser

## Purpose

Noveliser is an AI-powered novel generation tool that creates complete novels from simple descriptions. It generates structured books with chapters, sections, characters, and themes, then packages them as EPUB files ready for reading.

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd noveliser

# Install dependencies
pip install -r requirements.txt
```

## Usage

The `run` script provides all functionality:

```bash
./run <command> [options]
```

### Commands

#### Create a Novel

Generate a full novel from a description:

```bash
./run create "description" [options]
```

Options:
- `--chapters`: Number of chapters (default: 10)
- `--sections`: Sections per chapter (default: 10)
- `--model`: LLM model to use (default: ollama:llama3.2:latest)
- `--author`: Author name (default: Darren Oakey)

#### Run Tests

Quick test with minimal novel (1 chapter, 1 section):
```bash
./run test
```

Larger test novel (3 chapters, 2 sections):
```bash
./run test_bigger
```

## Examples

### Create a Mystery Novel
```bash
./run create "A detective investigates a series of art thefts in Victorian London"
```

### Create a Science Fiction Epic
```bash
./run create "Humanity's first colony ship discovers they're not alone in the universe" --chapters 15 --sections 12
```

### Create a Short Story
```bash
./run create "A magical bookshop appears only at midnight" --chapters 3 --sections 5
```

### Custom Author Name
```bash
./run create "A romance blooms during a zombie apocalypse" --author "Jane Smith"
```

## Output

Generated novels are saved as EPUB files in the `output/` directory. Each novel includes:
- Complete chapter structure
- Character development
- Consistent themes and plot
- Professional formatting

The EPUB files can be opened with any e-reader application or device.