from setuptools import setup, find_packages

setup(
    name="altergeist",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "rdflib>=7.0.0",
        "SPARQLWrapper>=2.0.0",
        "typer>=0.9.0",
        "pydantic>=2.0.0",
        "langchain>=0.1.0",
        "openai>=1.0.0",
        "anthropic>=0.8.0",
    ],
    python_requires=">=3.9",
) 