# RAGA - AI Indian Music Composer

An AI-powered Indian classical music composition tool that generates raga-compliant
melodies with proper phrasing, tala patterns, and structured compositions.

## Features

- **50+ authentic ragas** with correct aroha/avaroha, vadi/samvadi, mood, and time
- **20+ talas** with beats, vibhags, and rhythmic patterns
- **Melody generation** that follows raga grammar rules and characteristic phrases
- **Composition sections**: alap, jor, jhala, gat
- **Rich notation display** with swara notation rendering

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Compose a piece in a raga
raga compose --raga yaman --tala teentaal --sections alap,gat

# Play back a composition (render to notation)
raga play composition.json

# Analyze a raga's properties
raga analyze --raga bhairav
```

## Python API

```python
from raga.music.ragas import RagaDatabase
from raga.composer.melody import MelodyGenerator
from raga.composer.harmonizer import CompositionBuilder

db = RagaDatabase()
yaman = db.get("yaman")
gen = MelodyGenerator(yaman)
melody = gen.generate(num_beats=16)
```

## Author

Mukunda Katta
