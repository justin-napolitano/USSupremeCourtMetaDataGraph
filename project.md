---
slug: github-ussupremecourtmetadatagraph
id: github-ussupremecourtmetadatagraph
title: USSupremeCourtMetaDataGraph
repo: justin-napolitano/USSupremeCourtMetaDataGraph
githubUrl: https://github.com/justin-napolitano/USSupremeCourtMetaDataGraph
generatedAt: '2025-11-24T21:36:44.681Z'
source: github-auto
summary: >-
  Code that extracts metadata for every US Supreme Court case from the Library
  of Congress database and organizes it into a graph structure for analysis.
tags: []
seoPrimaryKeyword: ''
seoSecondaryKeywords: []
seoOptimized: false
topicFamily: null
topicFamilyConfidence: null
kind: project
entryLayout: project
showInProjects: true
showInNotes: false
showInWriting: false
showInLogs: false
---

Code that extracts metadata for every US Supreme Court case from the Library of Congress database and organizes it into a graph structure for analysis.

---

## Features

- Retrieves comprehensive metadata on US Supreme Court cases via the Library of Congress API.
- Structures case metadata as graph data suitable for network analysis.
- Includes utilities for cleaning and processing JSON data.
- Contains test modules for validating scraper functionality.

## Tech Stack

- Python 3
- Requests, BeautifulSoup for web scraping
- NetworkX for graph data structures
- Google API client libraries
- YAML for configuration
- JSON for data interchange
- Matplotlib for graph visualization (partial/experimental)

## Getting Started

### Prerequisites

- Python 3.6 or later
- Install dependencies:

```bash
pip install -r requirements.txt
```

*Note: The requirements.txt file is assumed to be created based on imports.*

### Running the scraper

1. Configure API credentials and parameters in `active_code_base/config.yaml`.
2. Run the scraper script (e.g., `loc_scraper_1.py` or `loc_scraper_2.py`) to fetch data.

Example:

```bash
python active_code_base/loc_scraper_1.py
```

### Running tests

Tests are located in the `tests` directory and can be run with pytest:

```bash
pytest tests/
```

## Project Structure

```
USSupremeCourtMetaDataGraph/
├── active_code_base/          # Core scraping and processing code
│   ├── loc_scraper_1.py       # Main scraper classes and functions
│   ├── loc_scraper_2.py       # Alternative or extended scraper
│   ├── loc_scraper_3.py       # Further scraper iteration
│   ├── clean_loc_data.py      # Utilities for cleaning JSON output
│   ├── config.yaml            # Configuration file for API keys and parameters
│   ├── output_2/              # Sample or generated JSON output data
│   └── cleaned_output/        # Processed JSON data
├── tests/                    # Unit tests and test configs
│   ├── conftest.py
│   ├── config.yaml
│   └── test_url/loc_scraper_test.py
├── LICENSE                   # Apache 2.0 License
└── README.md                 # This file
```

## Future Work / Roadmap

- Integrate JanusGraph backend for graph database storage and querying.
- Provide Dockerized environment for easier deployment and reproducibility.
- Expand metadata extraction to include more detailed case relationships.
- Enhance graph visualization capabilities.
- Improve error handling and rate limiting for API requests.


---

*This project is a work in progress and serves as a proof of concept for mining US Supreme Court metadata for political science research.*
