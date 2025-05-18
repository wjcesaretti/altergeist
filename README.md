# Altergeist - a politcal theory simulation

Altergeist simulates how political philosophers' views would change under alternate historical contexts using RDF knowledge graphs and LLMs.

## Overview

This project combines symbolic knowledge representation (RDF) with large language models to simulate how political philosophers might think in different historical contexts. It maintains philosophical consistency while allowing for contextual adaptation.

## Features

- RDF knowledge graph of political philosophers and their beliefs
- Context transformation engine for simulating alternate timelines
- Llama 3.1-powered response generation with ideology preservation
- CLI interface for easy interaction
- Automatic response logging and ideology scoring

## Prerequisites

- Python 3.8+
- Hugging Face account and access token
- RDFLib and other dependencies (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/wjcesaretti/altergeist.git
cd altergeist
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
python3 -m pip install --break-system-packages -r requirements.txt
```

4. Set up your Hugging Face token:
   - Create an account at [huggingface.co](https://huggingface.co)
   - Go to Settings → Access Tokens
   - Create a new token with read access
   - Set the token in your environment:
   ```bash
   export HUGGINGFACE_TOKEN='your-token-here'
   ```
   - For permanent setup, add to your shell profile:
   ```bash
   echo 'export HUGGINGFACE_TOKEN="your-token-here"' >> ~/.zshrc  # or ~/.bashrc
   source ~/.zshrc  # or source ~/.bashrc
   ```

## Usage

Run simulations using the CLI:

```bash
python3 -m app.run simulate Hobbes --year 1946 --region "Germany" --event "PostWWII" --question "What is the role of the state in AI governance?"
```

### Arguments

- `philosopher`: Name of the philosopher (e.g., Hobbes, Locke, Marx)
- `--year`: New birth year (optional)
- `--region`: New region (optional)
- `--event`: Historical event (optional)
- `--question`: Question to ask the philosopher
- `--model`: LLM model to use (default: meta-llama/Llama-3.1-70B-Instruct)
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