from dataclasses import dataclass
from typing import List, Optional
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

    def _get_birth_year(self, uri: URIRef) -> int:
        date = self.graph.value(uri, URIRef("http://purl.org/dc/terms/date"))
        return int(str(date).split("^")[0]) if date else None

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

    def get_all_philosophers(self) -> List[Philosopher]:
        philosophers = []
        for s in self.graph.subjects(RDF.type, URIRef(self.namespace + "Philosopher")):
            name = str(s).split("/")[-1]
            if philosopher := self.get_philosopher(name):
                philosophers.append(philosopher)
        return philosophers 