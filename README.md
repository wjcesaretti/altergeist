# Altergeist - a politcal theory simulation

Altergeist simulates how political philosophers' views would change under alternate historical contexts using RDF knowledge graphs and LLMs.

## Overview

This project combines symbolic knowledge representation (RDF) with large language models to simulate how political philosophers might think in different historical contexts. It maintains philosophical consistency while allowing for contextual adaptation.

## Features

- RDF knowledge graph of political philosophers and their beliefs
- Context transformation engine for simulating alternate timelines
- LLM-powered response generation with ideology preservation
- CLI interface for easy interaction
- Automatic response logging and ideology scoring

## Prerequisites

- Python 3.8+
- OpenAI API key
- RDFLib and other dependencies (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yusufdanis/counterfactual-political-simulator.git
cd counterfactual-political-simulator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Usage

Run simulations using the CLI:

```bash
python app/run.py Hobbes --year 1946 --region Germany --event PostWWII --question "What is the role of the state in AI governance?"
```

### Arguments

- `philosopher`: Name of the philosopher (e.g., Hobbes, Locke, Marx)
- `--year`: New birth year (optional)
- `--region`: New region (optional)
- `--event`: Historical event (optional)
- `--question`: Question to ask the philosopher
- `--model`: LLM model to use (default: gpt-4)
- `--temperature`: LLM temperature (default: 0.7)

## Development

### Project Structure

```
counterfactual-political-simulator/
├── data/                  # RDF knowledge graph & SPARQL utilities
│   └── philosophers.ttl   # Full symbolic dataset
├── engine/               # Core simulator logic
│   ├── kg_parser.py      # RDFLib parser & triple normalization
│   ├── context_transform.py  # Injects counterfactual changes
│   └── prompt_builder.py  # Constructs prompt from symbolic context
├── llm/                  # LLM interaction layer
│   └── generate.py       # Runs LLM prompt & returns structured response
├── app/                  # CLI entry point
│   └── run.py           # Main simulation runner
└── output/              # LLM outputs & logs
```

### Adding New Philosophers

1. Edit `data/philosophers.ttl` to add new philosopher data
2. Follow the existing RDF structure
3. Include beliefs, concepts, and historical context

## Testing

Run tests with pytest:

```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Your Name - [@WilliamCesaretti](https://github.com/wjcesaretti)

Project Link: [https://github.com/wjcesaretti/altergeist](https://github.com/wjcesaretti/altergeist)