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
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "streamlit>=1.32.0",
        "owlrl>=6.0.0",
    ],
    python_requires=">=3.8",
) 