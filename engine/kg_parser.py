from dataclasses import dataclass
from typing import List, Optional, Tuple
from rdflib import Graph, URIRef
from rdflib.namespace import RDF, RDFS, XSD

# Here we parse the knowledge graph and return a list of philosophers

# The knowledge graph is a ttl file that contains the following information:
# - Philosophers
# - Beliefs
# - Key concepts
# - Contexts
# - Ideological clusters


@dataclass
class Philosopher:
    name: str
    birth_year: int
    beliefs: List[str]
    key_concepts: List[str]
    contexts: List[str]
    ideological_cluster: str
    influenced_by: List[str]
    influenced: List[str]

@dataclass
class HistoricalContext:
    name: str
    start_year: int
    end_year: int

# The KnowledgeGraphParser class is used to parse the knowledge graph and return a list of philosophers
class KnowledgeGraphParser:
    def __init__(self, ttl_path: str):
        self.graph = Graph()
        self.graph.parse(ttl_path, format="turtle")
        self.namespace = "http://example.org/philosophy/"

    def _get_label(self, uri: URIRef) -> str:
        return str(self.graph.value(uri, RDFS.label))

    def _get_literal_values(self, uri: URIRef, predicate: str) -> List[str]:
        return [str(o) for o in self.graph.objects(uri, URIRef(self.namespace + predicate))]

    def _parse_year(self, year_str: str) -> int:
        """Parse a year string in the format 'YYYY BCE' or 'YYYY CE' into an integer."""
        if not year_str:
            return None
            
        parts = year_str.split()
        year = int(parts[0])
        era = parts[1]
        
        if era == "BCE":
            year = -year
            
        return year

    def _get_birth_year(self, uri: URIRef) -> int:
        birth_year = self.graph.value(uri, URIRef(self.namespace + "birthYear"))
        if not birth_year:
            return None
        return self._parse_year(str(birth_year))

    def _get_context_years(self, uri: URIRef) -> Tuple[int, int]:
        """Get the start and end years for a historical context."""
        start_year = self.graph.value(uri, URIRef(self.namespace + "startYear"))
        end_year = self.graph.value(uri, URIRef(self.namespace + "endYear"))
        
        if not start_year or not end_year:
            return None, None
            
        return self._parse_year(str(start_year)), self._parse_year(str(end_year))

    def get_philosopher(self, name: str) -> Optional[Philosopher]:
        uri = URIRef(self.namespace + name)
        if not (uri, RDF.type, URIRef(self.namespace + "Philosopher")) in self.graph:
            return None

        return Philosopher(
            name=self._get_label(uri),
            birth_year=self._get_birth_year(uri),
            beliefs=self._get_literal_values(uri, "believesIn"),
            key_concepts=self._get_literal_values(uri, "keyConcept"),
            contexts=self._get_literal_values(uri, "context"),
            ideological_cluster=self._get_literal_values(uri, "ideologicalCluster")[0],
            influenced_by=self._get_literal_values(uri, "influencedBy"),
            influenced=self._get_literal_values(uri, "influenced")
        )

    def get_historical_context(self, name: str) -> Optional[HistoricalContext]:
        uri = URIRef(self.namespace + name)
        if not (uri, RDF.type, URIRef(self.namespace + "HistoricalContext")) in self.graph:
            return None

        start_year, end_year = self._get_context_years(uri)
        if start_year is None or end_year is None:
            return None

        return HistoricalContext(
            name=self._get_label(uri),
            start_year=start_year,
            end_year=end_year
        )

    def get_all_philosophers(self) -> List[Philosopher]:
        philosophers = []
        for s in self.graph.subjects(RDF.type, URIRef(self.namespace + "Philosopher")):
            name = str(s).split("/")[-1]
            if philosopher := self.get_philosopher(name):
                philosophers.append(philosopher)
        return philosophers

    def get_all_historical_contexts(self) -> List[HistoricalContext]:
        contexts = []
        for s in self.graph.subjects(RDF.type, URIRef(self.namespace + "HistoricalContext")):
            name = str(s).split("/")[-1]
            if context := self.get_historical_context(name):
                contexts.append(context)
        return contexts 