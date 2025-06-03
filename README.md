# Altergeist

A philosophical debate simulator that allows you to engage with historical philosophers or watch them debate contemporary topics.

## Features

- **Single Philosopher Q&A**: Ask questions to historical philosophers and get responses based on their philosophical framework
- **Debate Mode**: Watch two philosophers debate a topic, with each responding to the other's arguments
- **Knowledge Graph Integration**: Uses RDF/OWL ontologies to represent philosophical knowledge and beliefs
- **Interactive UI**: Clean Streamlit interface for easy interaction

## Project Structure

```
altergeist/
├── app/
│   └── ui.py              # Streamlit web interface
├── data/
│   └── philosophers.ttl   # OWL ontology of philosophical knowledge
├── engine/
│   ├── kg_parser.py       # Knowledge graph parsing
│   ├── prompt_builder.py  # LLM prompt construction
│   └── llm_generate.py    # LLM interaction
└── requirements.txt
```

## Installation

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit UI:
```bash
streamlit run app/ui.py
```

The UI provides:
- Mode selection (Single Philosopher Q&A or Debate)
- Philosopher selection
- Question/debate topic input
- Response generation

## Knowledge Graph

The system uses an OWL ontology (`data/philosophers.ttl`) that includes:
- Philosopher profiles
- Core beliefs and concepts
- Historical context
- Influence relationships

## License

MIT License
