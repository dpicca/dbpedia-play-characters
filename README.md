# DBpedia Play Characters

This repository contains a collection of scripts and tools designed to extract, analyze, and work with play characters from DBpedia, Gutenberg, and other related sources.

## Overview

The project aims to provide insights into play characters, their relationships, and their occurrences in various plays. It uses a combination of heuristic methods, Natural Language Processing (NLP) techniques, and queries to databases like DBpedia, Gutenberg, and Wikidata.

## Structure

- **Data Extraction**:
  - `01_get_fictioncorpus.py`: Extracts fiction books from Gutenberg.
  - `01_get_playcorpus.py`: Extracts plays from Gutenberg.

- **Data Processing**:
  - `02_play_heuristics.py`: Uses heuristics to segment and analyze the text, extracting potential character names.
  - `03_tagging_spacy.py`: Uses the Spacy NLP library to tag and analyze the text.
  - `04_characters_from_ner.py`: Extracts character names using Named Entity Recognition (NER) from Spacy.

- **DBpedia Queries**: Files like `05_dbpedia_querys.py` and those in the `queries` directory are used to query DBpedia and retrieve relevant data.

- **DHTK**: The `dhtk` directory contains modules related to the Digital Humanities Toolkit.

- **Segmenter**: The `segmenter` directory contains scripts and tools for segmenting texts, classifying segments, and other related tasks.

## Requirements

Before running the scripts, ensure you have the required packages installed:

```
pip install -r requirements.txt
```

## Usage

1. **Extract Data**:
   ```
   python 01_get_fictioncorpus.py
   python 01_get_playcorpus.py
   ```

2. **Process Data**:
   ```
   python 02_play_heuristics.py
   python 03_tagging_spacy.py
   python 04_characters_from_ner.py
   ```

3. **Analyze and Extract Characters**:
   The scripts will generate CSV files with potential character names and their occurrences in the text.

## Contributing

Contributions are welcome! Please create a pull request or open an issue if you have suggestions or improvements.
