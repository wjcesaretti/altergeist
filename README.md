# AlterGeist
#Final Project for KRKE @ UNIBO 

A framework for simulating philosophical conversations with historical figures using knowledge graphs and large language models.

## Features

- **Knowledge Graph Integration**: Uses RDF/OWL ontologies to represent philosophical knowledge
- **Symbolic Reasoning**: OWL reasoning to infer new facts and validate responses
- **Contextual Awareness**: Simulates philosophers in different historical contexts
- **Interactive UI**: Streamlit-based interface for easy interaction
- **Response Validation**: Ensures responses align with philosophical beliefs
- **Extensible Architecture**: Modular design for adding new philosophers and capabilities

## Project Structure

```
altergeist/
├── app/
│   ├── ui.py              # Streamlit web interface
│   └── api.py             # FastAPI backend
├── data/
│   └── philosophers.ttl   # OWL ontology of philosophical knowledge
├── engine/
│   ├── kg_parser.py       # Knowledge graph parsing
│   ├── prompt_builder.py  # LLM prompt construction
│   ├── context_transform.py # Historical context modification
│   ├── llm_generate.py    # LLM interaction
│   └── symbolic_reasoner.py # OWL reasoning engine
├── tests/
│   ├── test_kg_parser.py
│   ├── test_prompt_builder.py
│   ├── test_context_transform.py
│   └── test_llm_generate.py
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

### Web Interface

Run the Streamlit UI:
```bash
streamlit run app/ui.py
```

The UI provides:
- Philosopher selection
- Historical context modification
- Question input
- Response generation
- Response validation

### API

Run the FastAPI server:
```bash
uvicorn app.api:app --reload
```

API endpoints:
- `POST /generate`: Generate a response
- `GET /philosophers`: List available philosophers
- `GET /philosopher/{name}`: Get philosopher details

## Knowledge Graph

The system uses an OWL ontology (`data/philosophers.ttl`) that includes:
- Philosopher profiles
- Core beliefs and concepts
- Historical context
- Influence relationships
- Philosophical schools and movements

## Development

### Running Tests

```bash
pytest
```

### Code Style

The project uses:
- Black for code formatting
- isort for import sorting
- mypy for type checking
- ruff for linting

Run all checks:
```bash
black .
isort .
mypy .
ruff check .
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and style checks
5. Submit a pull request

## License

MIT License
